from tkinter.ttk import Entry as TTKEntry
from .widget import TTKWidget, capture_custom_kwargs


class Entry(TTKWidget, TTKEntry):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKEntry.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
        self.update_widget_style()
