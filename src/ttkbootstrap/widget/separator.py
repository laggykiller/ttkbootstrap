from tkinter.ttk import Separator as TTKSeparator
from .widget import TTKWidget, capture_custom_kwargs


class Separator(TTKWidget, TTKSeparator):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKSeparator.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
