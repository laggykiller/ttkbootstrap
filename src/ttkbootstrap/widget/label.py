from tkinter.ttk import Label as TTKLabel
from widget import TTKWidget, capture_custom_kwargs


class Label(TTKWidget, TTKLabel):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKLabel.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
