from tkinter.ttk import Progressbar as TTKProgressbar
from .widget import TTKWidget, capture_custom_kwargs


class Progressbar(TTKWidget, TTKProgressbar):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKProgressbar.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
