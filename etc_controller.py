import etc_serial
import etc_plotcanvas

from color_constants import colors
import sys
import bitstring
import threading
import ctypes
import random

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('OsmGpsMap', '1.0')
from gi.repository import Gtk, GLib
from gi.repository import OsmGpsMap as ogm


class Controller(object):
    def __init__(self, model, view):
        self._model = model

        # VIEW
        self._view = view
        # Left pane
        self._lpane = self._view._lpane
        self._frame_serial = self._lpane._frame_serial
        self._frame_parameters = self._lpane._frame_parameters
        self._frame_commands = self._lpane._frame_commands
        # Right pane
        self._rpane = self._view._rpane
        self._fboxplotcanvas = self._rpane._fboxplotcanvas
        self._mapbox = self._rpane._mapbox

        # SERIAL
        # self._frame_serial._progress_bar.set_text('Pulso de paquetes')
        t = None
        self._arduino = etc_serial.Serial(timeout=t)
        self._load_ports()
        self.is_connected = threading.Event()
        self.is_run = True
        self.read_thread = None
        # self.read_serial_start()

        self.raw_data = bytearray(1)
        # TODO: Dinamically generate headers trough DB
        self.headers = [b'\xd1', b'\xd2']
        self.head1 = int.from_bytes(self.headers[0], byteorder=sys.byteorder)
        self.head2 = int.from_bytes(self.headers[1], byteorder=sys.byteorder)
        # self.header = b'\xd1'
        self.package_size = 45
        # self.package = numpy.empty(dtype=numpy.uint8,
        #                            shape=self.package_size)
        self.package = bytearray(self.package_size)
        self.package_counter = 0
        self.package_pointer = 0

        self.is_header = False
        self.first_time_header = False

        self.bad_package_counter = 0
        self.pck1_ok = 0
        self.pck2_ok = 0

        # DATABASE
        # False parameter: no debug
        self._db_session = self._model.connect_to_database(False)
        self._parameters = self._get_parameters()
        # i = 0
        # print("Parameters", len(self._parameters))
        # for item in self._parameters:
        #     print(i, item)
        #     i += 1

        # TODO: Remove this patch after DB refactor
        self._parameters_1 = self._parameters[:16] + self._parameters[19:28]
        # i = 0
        # print("Parameters package_1", len(self._parameters_1))
        # for item in self._parameters_1:
        #     print(i, item)
        #     i += 1

        # TODO: Remove this patch after DB refactor
        self._parameters_2 = self._parameters[:10] + [self._parameters[13]] + \
            self._parameters[16:19] + [self._parameters[28]] + \
            self._parameters[19:28]
        # i = 0
        # print("Parameters package_2", len(self._parameters_2))
        # for item in self._parameters_2:
        #     print(i, item)
        #     i += 1

        # TODO: Real management of commands and users
        self._command = self._db_session.query(self._model.Command).first()
        self._user_exec = self._db_session.query(self._model.User).first()
        self._setup_load_parameters()
        self._load_commands()

        # VIEW EVENTS
        self._frame_serial.connect('btn-refresh-clicked',
                                   self._on_btn_refresh_clicked)
        self._frame_serial.connect('cbox-ports-changed',
                                   self._on_cbox_ports_changed)
        self._frame_serial.connect('switch-serial-toggled',
                                   self._on_switch_serial_toggled)
        self._mapbox.connect('btn_launch_site_clicked',
                             self._on_btn_launch_site_clicked)

        # C LIBRARY INTERACTION
        # TODO: Relative path
        self._lib = ctypes.CDLL(
            './lib/c_library.so')

        # Draw empty canvases
        self._plotcanvas_list = []
        self.load_canvases()

        # Setup map
        self.launch_site = [-16.538275, -68.069592]
        self.map = self._mapbox.map
        self.setup_map()
        # Just for testing
        self.lat = self.launch_site[0]
        self.lon = self.launch_site[1]

        # SETUP INFOBAR
        self._infobar = self._view._infobar
        self.update_infobar(0)

        self._view.show_all()

    def update_infobar(self, val):
        state = "INFO: "
        if val == 0:
            message_type = Gtk.MessageType.ERROR
            state += "No hay conexión con la Estación Terrena"
        elif val == 1:
            message_type = Gtk.MessageType.WARNING
            state += "Conexión establecida. Esperando tramas..."
        elif val == 2:
            message_type = Gtk.MessageType.INFO
            state += "Recibiendo tramas..."

        self._infobar.set_message_type(message_type)
        content = self._infobar.get_content_area()
        label = content.get_children()[0]
        label.set_text(state)

    # /////////////// Serial ///////////////
    def _on_btn_refresh_clicked(self, button):
        # TODO: How to get the name of the button?
        print('Refresh clicked')
        self._load_ports()

    def _on_cbox_ports_changed(self, cbox):
        print('Cbox ports changed')
        self._set_port()

    def _on_switch_serial_toggled(self, widget, active):
            if active is True:
                print('Switch ON')
                self.start_operations()
            else:
                print('Switch OFF')
                self.stop_operations()

    def start_operations(self):
        # self._db_session = self._model.connect_to_database(False)
        # self.thread = None
        self.is_run = True
        try:
            self.read_serial_start()
            self._arduino.open_port()
            self.is_connected.set()
            self.update_infobar(1)
            # print(self.thread)
        except Exception as e:
            print(e)
        # self.read_serial_start()

    def stop_operations(self):
        # Thread close
        self.is_run = False
        # print(self.read_thread)
        # # try:
        # #     self.read_thread.join()
        # # except Exception as e:
        # #     print(e)
        # # # self.read_thread.join()
        # print('OK')
        # Arduino close
        self._arduino.close()
        # Clear is_connected event (for reading) value
        self.is_connected.clear()
        self.update_infobar(0)

        # self.thread = None
        # SQLAlchemy session commiting and closing
        try:
            self._db_session.commit()
        except Exception as e:
            self._db_session.rollback()
            print(e)
        # finally:
        #     self._db_session.close()
        #     print(self._db_session)

        print('Disconnected...')

    def _get_available_serial_ports(self):
        ports = self._arduino.list_serial_ports()
        ports_store = Gtk.ListStore(str)

        for port in ports:
            ports_store.append([port])

        return ports_store

    def _load_ports(self):
        # Loading and setting a data model for cbox_ports
        ports_store = self._get_available_serial_ports()
        cbox_ports = self._frame_serial._cbox_ports
        cbox_ports.set_model(ports_store)
        cbox_ports.set_active(0)

        self._set_port()

    def _set_port(self):
        cbox_ports = self._frame_serial._cbox_ports

        try:
            treeiter = cbox_ports.get_active_iter()
            model = cbox_ports.get_model()
            # Setting the port for the serial device
            self._arduino.port = model[treeiter][0]
        except TypeError:
            print("No connected devices")

    def _update_progress_bar(self):
        self._frame_serial._progress_bar.pulse()
        s = f"T1: {self.pck1_ok}, T2: {self.pck2_ok}"
        s += f"\nTOTAL: {self.package_counter} \u2714"
        self._frame_serial._progress_bar.set_text(s)
        # self._frame_serial._progress_bar.set_text(str(ok) + u'\u2714' + ' '
        #                                           + str(bad) + u'\u2716')
        return False

    # /////////////// Parameters ///////////////
    def _get_parameters(self):
        return self._db_session.query(self._model.Parameter).all()

    def _get_parameters_store(self):
        # Querying the db trough db_session
        # parameters = self._db_session.query(self._model.Parameter).all()
        parameters_store = Gtk.ListStore(str, str, str)

        # Populating parameters_store
        default_value = "0.000"
        for i in range(len(self._parameters_1)-9):
            symbol = self._parameters_1[i].symbol
            unit = self._parameters_1[i].unit
            parameters_store.append([symbol, default_value, unit])

        return parameters_store

    def _setup_load_parameters(self):
        tv_parameters = self._frame_parameters._tv_parameters
        # Setting headings and a text renderer for each column
        columns = ["Simbolo", "Valor", "Unidad"]
        for i, column_title in enumerate(columns):
            renderer_text = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer_text, text=i)
            tv_parameters.append_column(column)

        # Loading and setting a model for the treeview
        parameters_store = self._get_parameters_store()
        tv_parameters.set_model(parameters_store)

    # /////////////// Commands ///////////////
    def _get_commands(self):
        return self._db_session.query(self._model.Command).all()

    def _load_commands(self):
        flowbox = self._frame_commands._flowbox
        commands_list = self._get_commands()

        for command in commands_list:
            button = Gtk.Button()
            button.set_label(command.name)
            button.connect("clicked",
                           self._on_btn_command_clicked,
                           command)
            flowbox.add(button)

    def _on_btn_command_clicked(self, button, command):
        print(command)  # command is an object!

        str_command = command.command
        bytes_str_command = bytes.fromhex(str_command)

        self._arduino.write(bytes_str_command)
        print("Command sent:", bytes_str_command)

    # /////////////// Read data ///////////////
    def background_thread(self):
        # self._arduino.reset_input_buffer()
        print('Waiting for connection...')
        # print(self.thread)
        self.is_connected.wait()
        print('Connected!')

        while self.is_run:
            try:
                self._arduino.readinto(self.raw_data)
                # print(self.raw_data)
                self.package_builder()
            except Exception as e:
                print(e)
                break
            # print(self.raw_data)

    def read_serial_start(self):
        # print("THREAD:", self.thread)
        # if self.thread is None:
        self.read_thread = threading.Thread(target=self.background_thread)
        self.read_thread.daemon = True
        self.read_thread.start()

    def package_builder(self):
        received_byte = self.raw_data
        # print(self.package_pointer, received_byte, end=", ")

        # if received_byte == self.header:
        if received_byte in self.headers:
            if not self.first_time_header:
                self.is_header = True
                self.package_pointer = 0
                self.first_time_header = True

        int_received_byte = int.from_bytes(received_byte,
                                           byteorder=sys.byteorder)
        self.package[self.package_pointer] = int_received_byte
        self.package_pointer += 1

        if self.package_pointer >= self.package_size:
            self.package_pointer = 0

            if self.is_header:
                self.package_counter += 1
                self.handle_package()
                # checksum_value = bytes([self.package[self.package_size - 1]])
                #
                # if self.verify_checksum(checksum_value):
                #     self.package_counter += 1
                #     self.handle_package()
                # else:
                #     self.bad_package_counter += 1
                GLib.idle_add(self._update_progress_bar)
                self.is_header = False
                self.first_time_header = False

    def verify_checksum(self, orig_result):
        result = b''
        mask = b'\xff'
        sum = 0

        for i in range(self.package_size - 1):
            # num = int.from_bytes(self.package[i], byteorder=sys.byteorder)
            sum += self.package[i]

        result = bytes([sum.to_bytes(4, sys.byteorder)[0] & mask[0]])
        # print(result, orig_result)

        if orig_result == result:
            return True
        else:
            return False

    def handle_package(self):
        bitstream_package = bitstring.BitStream(self.package)
        # bitstream_package = bitstring.BitStream(self.package.tobytes())
        print('#', self.package_counter, ':', bitstream_package,
              len(bitstream_package))
        # print("Lost packages:", self.bad_package_counter)
        for value in self.package:
            print(value, end=' ')

        # Add raw record
        record = self._model.add_record(self._db_session,
                                        bitstream_package.hex,
                                        self._command, self._user_exec)

        # Parse package
        # Package_woh is package without the header
        package_woh = self.package[1:]
        GLib.idle_add(self.update_infobar, 2)

        if self.package[0] == self.head1:
            self.package_1(record, package_woh)
            self.pck1_ok += 1
        elif self.package[0] == self.head2:
            self.package_2(record, package_woh)
            self.pck2_ok += 1

    def package_1(self, record, package_woh):
        # print(len(package_woh))
        c_chr_array_package = (ctypes.c_char
                               * len(package_woh))(*package_woh)
        # size = 16
        c_float_array_parsed = (ctypes.c_float * len(self._parameters_1))()
        # print(c_chr_array_package, len(c_chr_array_package), c_float_array_parsed, len(c_float_array_parsed))
        self.c_parse_package_1(c_chr_array_package,
                               len(c_chr_array_package),
                               c_float_array_parsed,
                               len(c_float_array_parsed))
        print()
        self.print_array(c_float_array_parsed)
        print()

        parsed_str_parameters = []
        for i in range(len(self._parameters_1)):
            parsed_str_parameters.append(f'{c_float_array_parsed[i]:.3f}')
            self._model.add_parameter_record(self._db_session,
                                             parsed_str_parameters[i],
                                             self._parameters_1[i],
                                             record)

        # Refresh tv_parameters
        GLib.idle_add(self.refresh_tv_parameters, parsed_str_parameters)
        # Plot data
        GLib.idle_add(self.refresh_plots, c_float_array_parsed)
        # Refresh mapbox grid
        GLib.idle_add(self.refresh_mapbox_grid, parsed_str_parameters)
        # Draw GPS point
        GLib.idle_add(self.add_gps_point, c_float_array_parsed[23],
                      c_float_array_parsed[24])

    def package_2(self, record, package_woh):
        c_chr_array_package = (ctypes.c_char
                               * len(package_woh))(*package_woh)
        c_float_array_parsed = (ctypes.c_float * len(self._parameters_2))()
        self.c_parse_package_2(c_chr_array_package,
                               len(c_chr_array_package),
                               c_float_array_parsed,
                               len(c_float_array_parsed))
        print()
        self.print_array(c_float_array_parsed)
        print()

        parsed_str_parameters = []
        for i in range(len(self._parameters_2)):
            parsed_str_parameters.append(f'{c_float_array_parsed[i]:.3f}')
            self._model.add_parameter_record(self._db_session,
                                             parsed_str_parameters[i],
                                             self._parameters_2[i],
                                             record)

        # Refresh tv_parameters
        GLib.idle_add(self.refresh_tv_parameters_2, parsed_str_parameters)
        # GLib.idle_add(self.refresh_grid_2nd_package, parsed_str_parameters)
        # Plot data
        GLib.idle_add(self.refresh_plots_2, c_float_array_parsed)
        # Refresh mapbox grid
        GLib.idle_add(self.refresh_mapbox_grid_2, parsed_str_parameters)
        # Draw GPS point
        GLib.idle_add(self.add_gps_point, c_float_array_parsed[22],
                      c_float_array_parsed[23])
        #
        # # Just for testing
        # # Draw gps point
        # GLib.idle_add(self.add_gps_point, self.lat, self.lon)
        # self.lat += 0.00002
        # self.lon += 0.00002

    def refresh_tv_parameters(self, parsed_str_parameters):
        tv_parameters = self._frame_parameters._tv_parameters
        store_parameters = tv_parameters.get_model()

        rootiter = store_parameters.get_iter_first()
        store_parameters[rootiter][1] = parsed_str_parameters[0]

        treeiter = store_parameters.iter_next(rootiter)
        store_parameters[treeiter][1] = parsed_str_parameters[1]

        for i in range(2, len(self._parameters_1)-9):
                treeiter = store_parameters.iter_next(treeiter)
                store_parameters[treeiter][1] = parsed_str_parameters[i]

        tv_parameters.set_model(store_parameters)

        return False

    def refresh_tv_parameters_2(self, parsed_str_parameters):
        tv_parameters = self._frame_parameters._tv_parameters
        store_parameters = tv_parameters.get_model()

        rootiter = store_parameters.get_iter_first()
        store_parameters[rootiter][1] = parsed_str_parameters[0]

        treeiter = store_parameters.iter_next(rootiter)
        store_parameters[treeiter][1] = parsed_str_parameters[1]

        # Iterate up to BAR
        for i in range(2, len(self._parameters_2)-14):
                treeiter = store_parameters.iter_next(treeiter)
                store_parameters[treeiter][1] = parsed_str_parameters[i]
        # Skip TEMP1, TEMP2, TEMP3
        treeiter = store_parameters.iter_next(treeiter)
        treeiter = store_parameters.iter_next(treeiter)
        treeiter = store_parameters.iter_next(treeiter)
        treeiter = store_parameters.iter_next(treeiter)
        store_parameters[treeiter][1] = parsed_str_parameters[10]

        tv_parameters.set_model(store_parameters)

        return False

    def c_parse_package_1(self, input, size_in, output, size_out):
        self._lib.parse_package_1.restype = ctypes.c_void_p
        self._lib.parse_package_1(input, size_in, output, size_out)

    def c_parse_package_2(self, input, size_in, output, size_out):
        self._lib.parse_package_2.restype = ctypes.c_void_p
        self._lib.parse_package_2(input, size_in, output, size_out)

    def print_array(self, array):
        print(len(array), end=' | ')
        for value in array:
            print(format(value, '.3f'), end=', ')
        print()

    def refresh_mapbox_grid(self, parsed_str_parameters):
        lbl_vgpsdia = self._mapbox.lbl_vgpsdia
        lbl_vgpsmes = self._mapbox.lbl_vgpsmes
        lbl_vgpsanio = self._mapbox.lbl_vgpsanio
        lbl_vgpsdia.set_text(parsed_str_parameters[19])
        lbl_vgpsmes.set_text(parsed_str_parameters[20])
        lbl_vgpsanio.set_text(parsed_str_parameters[21])

        lbl_vgpshor = self._mapbox.lbl_vgpshor
        lbl_vgpsmin = self._mapbox.lbl_vgpsmin
        lbl_vgpsseg = self._mapbox.lbl_vgpsseg
        lbl_vgpshor.set_text(parsed_str_parameters[16])
        lbl_vgpsmin.set_text(parsed_str_parameters[17])
        lbl_vgpsseg.set_text(parsed_str_parameters[18])

        lbl_vgpsalt = self._mapbox.lbl_vgpsalt
        lbl_vgpsalt.set_text(parsed_str_parameters[22])

    def refresh_mapbox_grid_2(self, parsed_str_parameters):
        lbl_vtimer = self._mapbox.lbl_vtimer
        lbl_vtimer.set_text(parsed_str_parameters[13])

        lbl_vgpsdia = self._mapbox.lbl_vgpsdia
        lbl_vgpsmes = self._mapbox.lbl_vgpsmes
        lbl_vgpsanio = self._mapbox.lbl_vgpsanio
        lbl_vgpsdia.set_text(parsed_str_parameters[18])
        lbl_vgpsmes.set_text(parsed_str_parameters[19])
        lbl_vgpsanio.set_text(parsed_str_parameters[20])

        lbl_vgpshor = self._mapbox.lbl_vgpshor
        lbl_vgpsmin = self._mapbox.lbl_vgpsmin
        lbl_vgpsseg = self._mapbox.lbl_vgpsseg
        lbl_vgpshor.set_text(parsed_str_parameters[15])
        lbl_vgpsmin.set_text(parsed_str_parameters[16])
        lbl_vgpsseg.set_text(parsed_str_parameters[17])

        lbl_valt1 = self._mapbox.lbl_valt1
        lbl_valt1.set_text(parsed_str_parameters[11])
        lbl_valt2 = self._mapbox.lbl_valt2
        lbl_valt2.set_text(parsed_str_parameters[12])
        lbl_vgpsalt = self._mapbox.lbl_vgpsalt
        lbl_vgpsalt.set_text(parsed_str_parameters[21])

    # /////////////// Plotting ///////////////
    def load_canvases(self):
        flowbox = self._fboxplotcanvas._fb
        c = 0
        colors_list = [colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey'],
                       colors['cobalt'],
                       colors['cobaltgreen'],
                       colors['coldgrey']
                       ]

        # print(len(colors_list))

        for i in range(len(self._parameters)-11):
            plotcanvas = etc_plotcanvas.PlotCanvas(self._parameters[i].name,
                                                   self._parameters[i].symbol,
                                                   self._parameters[i].unit,
                                                   colors_list[c].hex_format())
            self._plotcanvas_list.append(plotcanvas)
            flowbox.add(plotcanvas.canvas)
            c += 1

        plotcanvas = etc_plotcanvas.PlotCanvas(self._parameters[25].name,
                                               self._parameters[25].symbol,
                                               self._parameters[25].unit,
                                               colors_list[c].hex_format())
        self._plotcanvas_list.append(plotcanvas)
        flowbox.add(plotcanvas.canvas)

        # print(len(self._plotcanvas_list))
        # c = 0
        # for item in self._plotcanvas_list:
        #     print(c, item.ax.get_title())
        #     c += 1

    def refresh_plots(self, c_float_array_parsed):
        for i in range(len(self._plotcanvas_list)-3):
            self._plotcanvas_list[i].update_draw(c_float_array_parsed[i])

        # GPSALT
            self._plotcanvas_list[18].update_draw(c_float_array_parsed[22])

    def refresh_plots_2(self, c_float_array_parsed):
        for i in range(len(self._plotcanvas_list)-9):
            self._plotcanvas_list[i].update_draw(c_float_array_parsed[i])

        # SC
        self._plotcanvas_list[13].update_draw(c_float_array_parsed[10])
        # ALT1
        self._plotcanvas_list[16].update_draw(c_float_array_parsed[11])
        # ALT2
        self._plotcanvas_list[17].update_draw(c_float_array_parsed[12])
        # GPSALT
        self._plotcanvas_list[18].update_draw(c_float_array_parsed[21])

    # /////////////// Map track ///////////////
    def setup_map(self):
        # map = self._mapbox.map
        self.layer_osd = ogm.MapOsd(show_dpad=True,
                                    show_zoom=True,
                                    show_crosshair=True,
                                    show_coordinates=True,
                                    show_scale=True)
        self.map.layer_add(self.layer_osd)
        max_zoom = self.map.props.max_zoom
        self.map.set_center_and_zoom(self.launch_site[0], self.launch_site[1],
                                     max_zoom)
        # map.props.record_trip_history = True
        # map.props.show_trip_history = True
        self.map.connect('button_press_event', self.on_button_press)
        # self.map.connect('button_release_event', self.on_button_release)

    def update_lbl_coords(self, lat, lon):
        lbl_coords = self._mapbox.lbl_coords
        lbl_coords.set_text('Latitud: %s \nLongitud: %s' % (lat, lon))

    def on_button_press(self, osm, event):
        if event.button == 1:  # LEFT
            pass
        elif event.button == 3:  # RIGHT
            lat, lon = self.map.get_event_location(event).get_degrees()
            self.update_lbl_coords(lat, lon)

    def _on_btn_launch_site_clicked(self, button):
        max_zoom = self.map.props.max_zoom
        self.map.set_center_and_zoom(self.launch_site[0], self.launch_site[1],
                                     max_zoom)

    def add_gps_point(self, lat, lon):
        mpoint = ogm.MapPoint()
        mpoint.set_degrees(lat, lon)
        self.map.gps_add(lat, lon, heading=ogm.MAP_INVALID)

        self.update_lbl_coords(lat, lon)

        return False
