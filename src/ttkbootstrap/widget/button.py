from tkinter.ttk import Button as TTKButton
from .widget import TTKWidget, capture_custom_kwargs


class Button(TTKWidget, TTKButton):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKButton.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
        self.update_widget_style()
