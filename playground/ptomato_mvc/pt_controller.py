class Controller(object):
    def __init__(self, model, view):
        self._model = model
        self._view = view

        self._view.connect('button-clicked', self._on_button_clicked)

        self._view.show_all()

    def _on_button_clicked(self, button, *args):
        greetee = self._model.greetee
        self._view.set_text('Hello, {}'.format(greetee))
        self._view.change_page(self._view.GREETING_PAGE)
