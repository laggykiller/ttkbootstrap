from tkinter.ttk import Scale as TTKScale
from .widget import TTKWidget, capture_custom_kwargs


class Scale(TTKWidget, TTKScale):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKScale.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
