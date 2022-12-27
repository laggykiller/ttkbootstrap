from tkinter.ttk import Menubutton as TTKMenubutton
from .widget import TTKWidget, capture_custom_kwargs


class Menubutton(TTKWidget, TTKMenubutton):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKMenubutton.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
