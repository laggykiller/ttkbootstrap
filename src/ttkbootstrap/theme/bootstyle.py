from PIL.ImageDraw import ImageDraw
from PIL.ImageTk import PhotoImage
from PIL import Image
from ttkbootstrap.theme.engine import ThemeEngine, image_draw, image_resize
from ttkbootstrap.constants import *
from tkinter.font import Font



class BootstyleEngine(ThemeEngine):

    def __init__(self, style):
        super().__init__('bootstyle', 'clam', style)
        self.register_keywords()

    def register_keywords(self):
        self.handler_set('button', self.style_default_button)
        self.handler_set('tk-tk', self.style_app_window)

    def create_named_fonts(self):
        """Create the named fonts used by this theme engine
        The font size is measured in pixels and is scaled to fit the
        screen so that the proportions are similar from computer to computer.
        https://learn.microsoft.com/en-us/windows/apps/design/style/xaml-theme-resources#the-xaml-type-ramp
        """
        scaling_factor = 1.4
        s = lambda x: self.scale_size(-x * scaling_factor)
        Font(name='TkCaption', family='Segoe UI', size=s(12))
        Font(name='TkBody', family='Segoe UI', size=s(14))
        Font(name='TkBodyStrong', family='Segoe UI Semibold', size=s(14))
        Font(name='TkBodyLarge', family='Segoe UI', size=s(18))
        Font(name='TkSubtitle', family='Segoe UI Semibold', size=s(20))
        Font(name='TkTitle', family='Segoe UI Semibold', size=s(28))
        Font(name='TkTitleLarge', family='Segoe UI Semibold', size=s(40))
        Font(name='TkDisplay', family='Segoe UI Semibold', size=s(68))

    def style_app_window(self, options):
        """Style the application main window"""
        scheme = options['scheme']
        colorname = 'background'
        background = scheme.get_color(colorname)

        # set the application window style
        window = options['widget']
        window.configure(background=background)

        # default global ttk styles for theme
        self.style.configure('.',
                             font='TkBody',
                             background=scheme.background,
                             darkcolor=scheme.background,
                             foreground=scheme.foreground,
                             troughcolor=scheme.background,
                             selectbg=scheme.info,
                             selectfg=scheme.background,
                             fieldbg=scheme.background,
                             borderwidth=1)

    def style_default_button(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        foreground = scheme.get_foreground(colorname)
        background = shades.base
        hover = shades.l1 if scheme.mode == LIGHT else shades.d1
        pressed = shades.l2 if scheme.mode == LIGHT else shades.d2
        disabled = shades.l2

        self.style.configure(
            ttkstyle,
            font='TkBody',
            foreground=foreground,
            background=background,
            bordercolor=background,
            darkcolor=background,
            lightcolor=background,
            relief=RAISED,
            focusthickness=0,
            focuscolor=foreground,
            padding=(10, 5),
            anchor=CENTER,
        )
        self.style.map(
            ttkstyle,
            foreground=[("disabled", disabled)],
            background=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            darkcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)],
            lightcolor=[
                ("pressed !disabled", pressed),
                ("hover !disabled", hover)])
