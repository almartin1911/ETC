import pt_model as m
import pt_view as v
import pt_controller as c


if __name__ == '__main__':
    c.Controller(m.Model(), v.View())
    v.Gtk.main()
