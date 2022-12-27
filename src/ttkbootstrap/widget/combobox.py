from tkinter.ttk import Combobox as TTKCombobox
from .widget import TTKWidget, capture_custom_kwargs


class Combobox(TTKWidget, TTKCombobox):

    def __init__(self, *args, **kw):
        custom, kwargs = capture_custom_kwargs(kw)
        TTKCombobox.__init__(self, *args, **kwargs)
        TTKWidget.__init__(self, **custom, **kwargs)
        self.update_widget_style()
