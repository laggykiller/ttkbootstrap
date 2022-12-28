from tkinter.ttk import Panedwindow as TTKPanedwindow
from .widget import TTKWidget, capture_custom_kwargs


class Panedwindow(TTKWidget, TTKPanedwindow):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKPanedwindow.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
