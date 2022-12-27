from tkinter.ttk import Notebook as TTKNotebook
from .widget import TTKWidget, capture_custom_kwargs


class Notebook(TTKWidget, TTKNotebook):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKNotebook.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
