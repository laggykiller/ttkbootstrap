from tkinter.ttk import Frame as TTKFrame
from .widget import TTKWidget, capture_custom_kwargs


class Frame(TTKWidget, TTKFrame):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKFrame.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
        self.update_widget_style()
