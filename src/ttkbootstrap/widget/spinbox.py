from tkinter.ttk import Spinbox as TTKSpinbox
from .widget import TTKWidget, capture_custom_kwargs


class Spinbox(TTKWidget, TTKSpinbox):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKSpinbox.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
        self.update_widget_style()
