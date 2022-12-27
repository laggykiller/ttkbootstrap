from tkinter.ttk import Treeview as TTKTreeview
from .widget import TTKWidget, capture_custom_kwargs


class Treeview(TTKWidget, TTKTreeview):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKTreeview.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
