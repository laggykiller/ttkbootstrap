from tkinter.ttk import Scrollbar as TTKScrollbar
from .widget import TTKWidget, capture_custom_kwargs


class Scrollbar(TTKWidget, TTKScrollbar):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKScrollbar.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
        self.update_widget_style()
