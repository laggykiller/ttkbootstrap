from tkinter.ttk import Checkbutton as TTKCheckbutton
from .widget import TTKWidget, capture_custom_kwargs


class Checkbutton(TTKWidget, TTKCheckbutton):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKCheckbutton.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
        self.update_widget_style()
