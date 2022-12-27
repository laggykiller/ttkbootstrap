from tkinter.ttk import Labelframe as TTKLabelframe
from .widget import TTKWidget, capture_custom_kwargs


class Labelframe(TTKWidget, TTKLabelframe):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKLabelframe.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
