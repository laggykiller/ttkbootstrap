from tkinter.ttk import Sizegrip as TTKSizegrip
from .widget import TTKWidget, capture_custom_kwargs


class Sizegrip(TTKWidget, TTKSizegrip):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKSizegrip.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
