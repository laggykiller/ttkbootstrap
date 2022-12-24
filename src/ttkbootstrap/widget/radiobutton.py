from tkinter.ttk import Radiobutton as TTKRadiobutton
from .widget import TTKWidget, capture_custom_kwargs


class Radiobutton(TTKWidget, TTKRadiobutton):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKRadiobutton.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
        self.update_widget_style()
