from PIL import Image
from PIL.ImageTk import PhotoImage
from ttkbootstrap.theme.engine import ThemeEngine, image_draw, image_resize
from ttkbootstrap.constants import *
from ttkbootstrap.style.element import ElementLayout as Element
from tkinter.font import Font


class ChromatkEngine(ThemeEngine):

    def __init__(self, style):
        super().__init__('chromatk', 'clam', style)
        self.create_named_fonts()
        self.register_keywords()

    def register_keywords(self):
        self.handler_set('button', self.create_button_style)
        self.handler_set('outline-button', self.create_outline_button_style)
        self.handler_set('link-button', self.create_link_button_style)
        self.handler_set('frame', self.create_frame_style)
        self.handler_set('label', self.create_label_style)
        self.handler_set('inverse-label', self.create_inverse_label_style)
        self.handler_set('labelframe', self.create_labelframe_style)
        self.handler_set('separator', self.create_separator_style)
        self.handler_set('entry', self.create_entry_style)
        self.handler_set('combobox', self.create_combobox_style)
        self.handler_set('menubutton', self.create_menubutton_style)
        self.handler_set('notebook', self.create_notebook_style)
        self.handler_set('panedwindow', self.create_panedwindow_style)
        self.handler_set('progressbar', self.create_progressbar_style)
        self.handler_set('scale', self.create_scale_style)
        self.handler_set('sizegrip', self.create_sizegrip_style)
        self.handler_set('checkbutton', self.create_checkbutton_style)
        self.handler_set('radiobutton', self.create_radiobutton_style)
        self.handler_set('switch', self.create_switch_style)
        self.handler_set('scrollbar', self.create_scrollbar_style)
        self.handler_set('spinbox', self.create_spinbox_style)
        self.handler_set('tk-tk', self.create_window_style)
        self.handler_set('tk-combobox-popdown',
                         self.create_combobox_popdown_style)
        self.handler_set('outline-menubutton',
                         self.create_outline_menubutton_style)

    def create_named_fonts(self):
        """Create the named fonts used by this theme engine
        The font size is measured in pixels and is scaled to fit the
        screen so that the proportions are similar from computer to computer.
        https://learn.microsoft.com/en-us/windows/apps/design/style/xaml-theme-resources#the-xaml-type-ramp
        """
        scaling_factor = 1.4

        def s(x):
            return self.scale_size(-x * scaling_factor)

        self.register_assets('fonts',
            Font(name='TkCaption', family='Segoe UI', size=s(12)),
            Font(name='TkBody', family='Segoe UI', size=s(14)),
            Font(name='TkBodyStrong', family='Segoe UI Semibold', size=s(14)),
            Font(name='TkBodyLarge', family='Segoe UI', size=s(18)),
            Font(name='TkSubtitle', family='Segoe UI Semibold', size=s(20)),
            Font(name='TkTitle', family='Segoe UI Semibold', size=s(28)),
            Font(name='TkTitleLarge', family='Segoe UI Semibold', size=s(40)),
            Font(name='TkDisplay', family='Segoe UI Semibold', size=s(68)))

    def create_window_style(self, options):
        """Style the application main window"""
        scheme = options['scheme']
        colorname = 'background'
        background = scheme.get_color(colorname)

        # set the application window style
        window = options['widget']
        window.configure(background=background)

        # default global ttk styles for theme
        self.style.configure(
            style='.', font='TkBody', background=background,
            darkcolor=background, foreground=scheme.foreground,
            troughcolor=background, selectbg=scheme.info, selectfg=background,
            fieldbg=background, borderwidth=1)

    def create_button_style(self, options):
        """Create the default button style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'primary'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        foreground = scheme.get_foreground(colorname)
        background = shades.base
        hover = shades.l1 if scheme.mode == LIGHT else shades.d1
        pressed = shades.l2 if scheme.mode == LIGHT else shades.d2
        disabled = shades.l2

        img_size = 800, 800
        final_size = 36, 36
        common = {'xy': (10, 10, 790, 790), 'radius': 96, 'outline': shades.d2,
                  'width': 4}

        # normal image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, fill=background)
        img_norm = image_resize(im, final_size)

        # hover image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, fill=hover)
        img_hover = image_resize(im, final_size)

        # pressed image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, fill=pressed)
        img_pressed = image_resize(im, final_size)

        self.register_assets(scheme.name, img_norm, img_hover, img_pressed)

        # button image element
        elem = self.style.element_image_builder(
            f'{ttkstyle}.button', img_norm, sticky=NSEW, border=5)
        elem.map('pressed !disabled', img_pressed)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # button layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{ttkstyle}.button'), [
                Element('Button.padding'), [
                    Element('Button.label', side=LEFT, expand=True)]]])

        # normal state
        self.style.configure(
            style=ttkstyle, foreground=foreground, focuscolor=foreground,
            relief=RAISED, anchor=CENTER, font='TkBody', padding='8 2',
            width=12)

        # state map
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])
        self.style.state_map(ttkstyle, 'shiftrelief', [
            ('pressed !disabled', -1)])

    def create_outline_button_style(self, options):
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'primary'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_lt = scheme.get_shades('light')
        shades_bg = scheme.get_shades('background')
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        background = foreground = shades.base
        hover_bg = shades_bg.l1 if scheme.mode == DARK else shades_lt.base

        # create style assets
        img_size = 800, 800
        final_size = 36, 36
        common = {'xy': (10, 10, 790, 790), 'radius': 96}

        # normal image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background, width=6)
        img_norm = image_resize(im, final_size)

        # hover image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background, width=4,
                               fill=hover_bg)
        img_hover = image_resize(im, final_size)

        # pressed image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background, width=4,
                               fill=hover_bg)
        img_pressed = image_resize(im, final_size)

        # disable image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled, width=2)
        img_disabled = image_resize(im, final_size)

        self.register_assets(scheme.name, img_norm, img_hover, img_pressed,
                             img_disabled)

        # button image element
        el_name = f'{ttkstyle}.button'
        elem = self.style.element_image_builder(
            el_name, image=img_norm, sticky=NSEW, border=5)
        elem.map('disabled', img_disabled)
        elem.map('pressed !disabled', img_pressed)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # button layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(el_name, sticky=NSEW), [
                Element('Button.padding'), [
                    Element('Button.label', side=LEFT, expand=True)]]])

        # normal state
        self.style.configure(ttkstyle, foreground=foreground, relief=RAISED,
                             focuscolor=foreground, anchor=CENTER, width=12,
                             padding='8 2')

        # state map
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])
        self.style.state_map(ttkstyle, 'shiftrelief', [
            ('pressed !disabled', -1)])

    def create_link_button_style(self, options):
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'primary'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades_lt = scheme.get_shades('light')
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        foreground = scheme.get_color(colorname)
        hover = scheme.info

        # normal state
        self.style.configure(
            style=ttkstyle, relief=RAISED, foreground=foreground,
            anchor=CENTER, font='TkBody', padding='8 2', width=12)

        # normal image
        im = PhotoImage(Image.new('RGBA', (36, 36)))
        self.register_assets(scheme.name, im)

        # button image element
        self.style.element_create(f'{ttkstyle}.button', 'image', im,
                                  sticky=NSEW)

        # button layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{ttkstyle}.button'), [
                Element('Button.padding'), [
                    Element('Button.label', side=LEFT, expand=True)]]])

        # state style maps
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled),
            ('hover !disabled', hover)])
        self.style.state_map(ttkstyle, 'shiftrelief', [
            ('pressed !disabled', '-2')])
        self.style.state_map(ttkstyle, 'focuscolor', [
            ('hover', hover)])

    def create_checkbutton_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'primary'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_lt = scheme.get_shades('light')
        shades_bg = scheme.get_shades('background')
        foreground = scheme.background
        background = shades.base
        app_bg = scheme.background
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        outline = shades_lt.d3 if scheme.mode == DARK else shades_lt.d3
        hover_on = shades.l1 if scheme.mode == LIGHT else shades.d1
        hover_off = shades_bg.l1 if scheme.mode == DARK else shades_lt.base
        pressed_off = shades_bg.l2 if scheme.mode == DARK else shades_lt.d1
        pressed_on = shades.l2 if scheme.mode == LIGHT else shades.d2

        # create checkbutton assets
        img_size = 640, 640
        final_size = 28, 28
        rect_size = 10, 10, 630, 630
        radius = 76
        common = {'xy': rect_size, 'radius': radius}

        # off
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=outline, fill=app_bg,
                               width=24)
        img_off = image_resize(im, final_size)
        im.resize(final_size, Image.LANCZOS).save('checkbutton_off.png')

        # off/hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=outline, fill=hover_off,
                               width=24)
        img_off_hover = image_resize(im, final_size)

        # off/pressed
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=outline, fill=pressed_off,
                               width=24)
        img_off_pressed = image_resize(im, final_size)

        # on
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=background,
                               width=3)
        draw.line((190, 330, 293, 433, 516, 210), width=40, fill=foreground,
                  joint='curve')
        img_on = image_resize(im, final_size)

        # on/hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=hover_on,
                               width=3)
        draw.line((190, 330, 293, 433, 516, 210), width=40, fill=foreground,
                  joint='curve')
        img_on_hover = image_resize(im, final_size)

        # on/pressed
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=pressed_on,
                               width=3)
        draw.line((190, 330, 293, 433, 516, 210), width=40, fill=foreground,
                  joint='curve')
        img_on_pressed = image_resize(im, final_size)

        # on/disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled, fill=background,
                               width=3)
        draw.line((190, 330, 293, 433, 516, 210), width=40, fill=disabled,
                  joint='curve')
        img_on_dis = image_resize(im, final_size)

        # alt
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=background,
                               width=3)
        draw.line((213, 320, 427, 320), width=40, fill=foreground)
        img_alt = image_resize(im, final_size)

        # alt
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=pressed_on,
                               width=3)
        draw.line((213, 320, 427, 320), width=40, fill=foreground)
        img_alt_pressed = image_resize(im, final_size)

        # alt
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=hover_on,
                               width=3)
        draw.line((213, 320, 427, 320), width=40, fill=foreground)
        img_alt_hover = image_resize(im, final_size)

        # alt/disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled, fill=background,
                               width=3)
        draw.line((213, 320, 427, 320), width=40, fill=disabled)
        img_alt_dis = image_resize(im, final_size)

        # disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled, fill=foreground,
                               width=12)
        img_dis = image_resize(im, final_size)

        # create image element
        indicator = ttkstyle.replace('.TC', '.C') + '.indicator'
        elem = self.style.element_image_builder(
            indicator, img_on, width=34, sticky=W)
        elem.map('disabled selected', img_on_dis)
        elem.map('disabled alternate', img_alt_dis)
        elem.map('disabled', img_dis)
        elem.map('pressed alternate !disabled', img_alt_pressed)
        elem.map('pressed !selected !disabled', img_off_pressed)
        elem.map('pressed selected !disabled', img_on_pressed)
        elem.map('hover alternate !disabled', img_alt_hover)
        elem.map('hover !selected !disabled', img_off_hover)
        elem.map('hover selected !disabled', img_on_hover)
        elem.map('alternate', img_alt)
        elem.map('!selected', img_off)
        elem.build()

        # register theme assets to prevent GC
        self.register_assets(scheme.name, img_on, img_on_dis, img_alt_dis,
                             img_dis, img_alt_pressed, img_off_pressed,
                             img_on_pressed, img_alt_hover, img_off_hover,
                             img_on_hover, img_alt, img_off)

        # normal state style
        self.style.configure(style=ttkstyle, foreground=scheme.foreground,
                             background=scheme.background, focuscolor='',
                             font='TkBody', padding=4)

        # state mapping
        self.style.state_map(ttkstyle, 'foreground', [('disabled', disabled)])

        # style layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element('Checkbutton.button'), [
                Element('Checkbutton.padding'), [
                    Element(indicator, side=LEFT, sticky=''),
                    Element('Checkbutton.label', side=RIGHT, expand=True)]]])

    def create_radiobutton_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'primary'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_lt = scheme.get_shades('light')
        shades_bg = scheme.get_shades('background')
        app_bg = scheme.background
        background = shades.base
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        outline = shades_lt.d3
        hover_on = shades.l1 if scheme.mode == LIGHT else shades.d1
        hover_off = shades_bg.l1 if scheme.mode == DARK else shades_lt.base
        pressed_on = shades.l2 if scheme.mode == LIGHT else shades.d2

        # create radiobutton assets
        img_size = 640, 640
        final_size = 28, 28
        ellipse_size = 10, 10, 630, 630

        # off
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=outline, fill=app_bg, width=24)
        img_off = image_resize(im, final_size)

        # off/hover
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=outline, fill=hover_off, width=24)
        img_off_hover = image_resize(im, final_size)

        # off/pressed
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=outline, fill=app_bg, width=140)
        draw.ellipse(ellipse_size, outline=outline, width=24)  # outer
        img_off_pressed = image_resize(im, final_size)

        # on
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=background, fill=app_bg, width=140)
        draw.ellipse(ellipse_size, outline=shades.d2, width=3)  # outer
        img_on = image_resize(im, final_size)

        # on/hover
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=hover_on, fill=app_bg, width=110)
        draw.ellipse(ellipse_size, outline=shades.d2, width=3)  # outer
        img_on_hover = image_resize(im, final_size)

        # on/pressed
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=pressed_on, fill=app_bg,
                     width=140)
        draw.ellipse(ellipse_size, outline=shades.d2, width=3)  # outer
        img_on_pressed = image_resize(im, final_size)

        # radio on/disabled
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=disabled, fill=app_bg, width=140)
        draw.ellipse(ellipse_size, outline=outline, width=3)  # outer
        img_on_dis = image_resize(im, final_size)

        # radio disabled
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=disabled, fill=app_bg, width=24)
        img_dis = image_resize(im, final_size)

        # create image elements
        elem = self.style.element_image_builder(
            f'{ttkstyle}.indicator', img_on, width=34, sticky=W)
        elem.map('disabled selected', img_on_dis)
        elem.map('disabled', img_dis)
        elem.map('pressed !selected !disabled', img_off_pressed)
        elem.map('pressed selected !disabled', img_on_pressed)
        elem.map('hover !selected !disabled', img_off_hover)
        elem.map('hover selected !disabled', img_on_hover)
        elem.map('!selected', img_off)
        elem.build()

        # register assets to prevent GC
        self.register_assets(scheme.name, img_on, img_on_dis, img_dis,
                             img_off_pressed, img_on_pressed, img_off_hover,
                             img_on_hover, img_off)

        # normal style
        self.style.configure(
            ttkstyle, font='TkBody', foreground=scheme.foreground,
            background=scheme.background, focuscolor='', padding=4)

        # state mapping
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])

        # style layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element('Radiobutton.padding'), [
                Element(f'{ttkstyle}.indicator', side=LEFT),
                Element('Radiobutton.label', side=RIGHT, expand=True)]])

    def create_switch_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'primary'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_lt = scheme.get_shades('light')
        background = shades.base
        app_bg = scheme.background
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        outline = shades_lt.d3
        hover_on = shades.l1 if scheme.mode == LIGHT else shades[5]
        pressed_on = shades[2] if scheme.mode == LIGHT else shades.d2

        # create radiobutton assets
        final_size = 56, 28
        img_size = 1200, 600
        outer_rect = 10, 10, 1190, 590
        inner_rect = 622, 34, 1166, 566

        # off - normal
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=outline, width=24,
                               fill=app_bg, radius=300)
        draw.rounded_rectangle(inner_rect, outline=app_bg, width=80,
                               fill=outline, radius=290)
        img_off = image_resize(im.rotate(180), final_size)

        # off - hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=outline, width=24,
                               fill=app_bg, radius=300)
        draw.rounded_rectangle(inner_rect, outline=app_bg, width=60,
                               fill=outline, radius=290)
        img_off_hover = image_resize(im.rotate(180), final_size)

        # off - pressed
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=outline, width=24,
                               fill=app_bg, radius=300)
        draw.rounded_rectangle((500, 34, 1100, 566), outline=app_bg,
                               width=60, fill=outline, radius=290)
        img_off_pressed = image_resize(im.rotate(180), final_size)

        # on - normal
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=shades.d2, width=6,
                               fill=background, radius=300)
        draw.rounded_rectangle(inner_rect, outline=background, width=80,
                               fill=app_bg, radius=290)
        img_on = image_resize(im, final_size)

        # on - hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=shades.d2, width=6,
                               fill=hover_on, radius=300)
        draw.rounded_rectangle(inner_rect, outline=hover_on, width=60,
                               fill=app_bg, radius=290)
        img_on_hover = image_resize(im, final_size)

        # on - pressed
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, fill=pressed_on, radius=300)
        draw.rounded_rectangle((500, 34, 1100, 566), outline=pressed_on,
                               width=60, fill=app_bg, radius=290)
        img_on_pressed = image_resize(im, final_size)

        # off - disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=disabled, width=24,
                               fill=app_bg, radius=300)
        draw.rounded_rectangle(inner_rect, outline=app_bg, width=80,
                               fill=disabled, radius=290)
        img_off_dis = image_resize(im.rotate(180), final_size)

        # on - disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=outline, width=6,
                               fill=disabled, radius=300)
        draw.rounded_rectangle(inner_rect, outline=disabled, width=80,
                               fill=app_bg, radius=290)
        img_on_dis = image_resize(im, final_size)

        # style element
        elem = self.style.element_image_builder(f'{ttkstyle}.indicator',
                                                img_on, width=62, sticky=W)
        elem.map('disabled !selected', img_off_dis)
        elem.map('disabled selected', img_on_dis)
        elem.map('!selected pressed', img_off_pressed)
        elem.map('!selected hover', img_off_hover)
        elem.map('!selected', img_off)
        elem.map('selected pressed', img_on_pressed)
        elem.map('selected hover', img_on_hover)
        elem.build()

        # register assets to prevent GC
        self.register_assets(scheme.name, img_on, img_off_dis, img_on_dis,
                             img_off_pressed, img_off_hover, img_off,
                             img_on_pressed, img_on_hover)

        # style layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element('Toolbutton.border'), [
                Element('Toolbutton.padding'), [
                    Element(f'{ttkstyle}.indicator', side=LEFT),
                    Element('Toolbutton.label', side=RIGHT, expand=True)]]])

        # normal style
        self.style.configure(ttkstyle, foreground=scheme.foreground,
                             background=scheme.background, padding='8 2')

        # state map
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])

    def create_scrollbar_style(self, options):
        ss = self.scale_size
        scheme = options['scheme']
        orient = options['orient'] or VERTICAL
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'light'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades_lt = scheme.get_shades(colorname)
        background = shades_lt.d3

        # create scrollbar assets
        if orient == VERTICAL:
            thumb_fs = ss(10, 40)
            trough_fs = ss(18, 72)
            img_size = 500, 2000
            round_rect = ss(10, 10, 490, 1990)
        else:
            thumb_fs = ss(40, 10)
            trough_fs = ss(72, 18)
            img_size = 2000, 500
            round_rect = ss(10, 10, 1990, 490)

        # thumb image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(round_rect, radius=ss(250), fill=background)
        img_thumb_norm = image_resize(im, thumb_fs)

        # trough image
        # --- Will use an empty image for now instead of adding a border to
        #   the trough. I think it looks better in this case.
        im = Image.new('RGBA', img_size)  # empty image
        img_trough = image_resize(im, trough_fs)

        # register style assets
        self.register_assets(scheme.name, img_trough, img_thumb_norm)

        # element image
        e_name = ttkstyle.replace('.TS', '.S')
        if orient == HORIZONTAL:
            self.style.element_image_builder(
                f'{e_name}.trough', img_trough, sticky=EW, border='8 0',
                padding=6).build()
            self.style.element_image_builder(
                f'{e_name}.thumb', img_thumb_norm, sticky=EW, border='10 0',
                padding=12).build()

            # layout
            layout = self.style.element_layout_builder(ttkstyle)
            layout.build([
                Element(f'{e_name}.trough', sticky=EW), [
                    Element(f'{e_name}.thumb', sticky=NSEW)]])
        else:
            self.style.element_create(
                f'{e_name}.trough', 'image', img_trough, sticky=NS,
                border='0 8')
            self.style.element_create(
                f'{e_name}.thumb', 'image', img_thumb_norm, sticky=NS,
                border='0 10')

            # layout
            layout = self.style.element_layout_builder(ttkstyle)
            layout.build([
                Element(f'{e_name}.trough', sticky=NS), [
                    Element(f'{e_name}.thumb', sticky=NSEW)]])

    def create_spinbox_style(self, options):
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'light'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_bg = scheme.get_shades('background')
        shades_lt = scheme.get_shades('light')
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        background = shades.d2
        foreground = scheme.foreground
        focus_color = scheme.primary if colorname == 'light' else shades.base
        hover_bg = shades_bg.l1 if scheme.mode == DARK else shades_lt.base

        img_size = ss(800, 400)
        final_size = ss(200, 100)
        common = {'xy': ss(10, 10, 790, 390), 'radius': ss(16), 'width': ss(2)}

        # field
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ss(12, 388, 788, 388), fill=shades.d3, width=ss(4))
        img_field = image_resize(im, final_size)

        # field hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background, fill=hover_bg)
        draw.line(ss(12, 388, 788, 388), fill=shades.d3, width=ss(4))
        img_hover = image_resize(im, final_size)

        # field focus
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ss(12, 387, 788, 387), fill=focus_color, width=ss(5))
        img_focus = image_resize(im, final_size)

        # field disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled)
        img_disabled = image_resize(im, final_size)

        # field element
        el_field = f'{ttkstyle}.field'
        elem = self.style.element_image_builder(
            el_field, img_field, sticky=NSEW, border=ss(6), width=ss(200),
            height=ss(50))
        elem.map('disabled', img_disabled)
        elem.map('focus !readonly', img_focus)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # chevron normal
        im, draw = image_draw(ss(1400, 755))
        draw.line([ss(20, 20), ss(735, 735), ss(700, 700), ss(1380, 20)],
                  fill=foreground, width=ss(100))
        img_chev_dw = image_resize(im, ss(14, 8))
        img_chev_up = image_resize(im.rotate(180), ss(14, 8))

        # chevron pressed
        im, draw = image_draw(ss(1400, 755))
        draw.line([ss(20, 20), ss(735, 735), ss(700, 700), ss(1380, 20)],
                  fill=foreground, width=ss(200))
        img_chev_dwp = image_resize(im, ss(14, 8))
        img_chev_upp = image_resize(im.rotate(180), ss(14, 8))

        # chevron disabled
        im, draw = image_draw(ss(1400, 755))
        draw.line([ss(20, 20), ss(735, 735), ss(700, 700), ss(1380, 20)],
                  fill=disabled, width=ss(100))
        img_chev_dw_dis = image_resize(im, ss(14, 8))
        img_chev_up_dis = image_resize(im.rotate(180), ss(14, 8))

        self.register_assets(scheme.name, img_chev_dw, img_chev_up,
                             img_chev_dwp, img_chev_upp, img_chev_dw_dis,
                             img_chev_up_dis, img_field, img_hover, img_focus,
                             img_disabled)

        el_chev_up = f'{ttkstyle}.uparrow'
        elem = self.style.element_image_builder(
            el_chev_up, img_chev_up, sticky='', padding='16 4')
        elem.map('disabled', img_chev_up_dis)
        elem.map('pressed !disabled', img_chev_upp)
        elem.build()

        el_chev_dw = f'{ttkstyle}.downarrow'
        elem = self.style.element_image_builder(
            el_chev_dw, img_chev_dw, sticky='', padding='8 4')
        elem.map('disabled', img_chev_dw_dis)
        elem.map('pressed !disabled', img_chev_dwp)
        elem.build()

        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{ttkstyle}.field', expand=True), [
                Element('Spinbox.padding', sticky=NSEW), [
                    Element(f'{ttkstyle}.downarrow', side=RIGHT, sticky=NS),
                    Element(f'{ttkstyle}.uparrow', side=RIGHT, sticky=NS),
                    Element('Spinbox.textarea', side=LEFT)]]])

        # normal style
        self.style.configure(
            ttkstyle, foreground=foreground, insertcolor=foreground,
            selectbackground=shades_bg.base,  selectforeground=foreground,
            padding='8 4')

        # state style map
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])
        self.style.state_map(ttkstyle, 'selectbackground', [
            ('hover !disabled', hover_bg)])

    def create_frame_style(self, options):
        """Create a frame style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'background'
        self.style_register(options['ttkstyle'], scheme)

        # normal state
        background = scheme.get_color(colorname)
        self.style.configure(style=ttkstyle, background=background)

    def create_outline_frame_style(self, options):
        # TODO
        pass

    def create_label_style(self, options):
        """Create a label style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'foreground'
        self.style_register(options['ttkstyle'], scheme)

        # normal state
        foreground = scheme.get_color(colorname)
        self.style.configure(style=ttkstyle, foreground=foreground,
                             background=scheme.background)

    def create_inverse_label_style(self, options):
        """Create an inverse label style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'background'
        self.style_register(options['ttkstyle'], scheme)

        # normal state
        background = scheme.get_color(colorname)
        self.style.configure(style=ttkstyle, foreground=scheme.background,
                             background=background)

    def create_labelframe_style(self, options):
        """Create an labelframe style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'light'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        background = scheme.background
        foreground = scheme.foreground
        bordercolor = shades.d3

        im_size = ss(1600, 1600)
        final_size = ss(64, 64)
        im, draw = image_draw(im_size)
        draw.rounded_rectangle((10, 10, 1590, 1590), radius=ss(1600 * 0.12),
                               outline=bordercolor, width=ss(24))
        img = image_resize(im, final_size)
        self.register_assets(scheme.name, img)

        self.style.element_image_builder(
            f'{ttkstyle}.border', img, sticky=NSEW, border=12).build()

        self.style.element_layout_builder(ttkstyle).build([
            Element(f'{ttkstyle}.border')])

        # widget label
        self.style.configure(style=f'{ttkstyle}.Label', foreground=foreground,
                             background=background)

        # widget frame
        self.style.configure(style=ttkstyle, borderwidth=2, relief=RAISED,
                             bordercolor=bordercolor, lightcolor=background,
                             darkcolor=background, background=background)

    def create_separator_style(self, options):
        """Create a separator style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'light'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        background = shades.d3 if colorname == LIGHT else shades.base

        if options['orient'] == HORIZONTAL:
            size = ss(40, 1)
            sticky = EW
        else:
            size = ss(1, 40)
            sticky = NS

        img = PhotoImage(image=Image.new('RGB', size, background))
        self.register_assets(scheme.name, img)

        name = scheme.name + '.' + ttkstyle.replace('.TS', '.S') + '.separator'
        if name in self.style.element_names():
            return

        # style elements and layout
        self.style.element_create(name, 'image', str(img))
        self.style.element_layout_builder(name).build([
            Element('separator', sticky=sticky)])

    def create_entry_style(self, options):
        """Create an entry style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'light'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_bg = scheme.get_shades('background')
        shades_lt = scheme.get_shades('light')
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        background = shades.d2
        foreground = scheme.foreground
        select_fg = scheme.get_foreground('primary')
        focus_color = scheme.primary if colorname == 'light' else shades.base
        hover_bg = shades_bg.l1 if scheme.mode == DARK else shades_lt.base

        img_size = ss(800, 400)
        final_size = ss(200, 100)
        common = {'xy': ss(10, 10, 790, 390), 'radius': ss(16), 'width': ss(2)}

        # entry field
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ss(12, 388, 788, 388), fill=shades.d3, width=ss(4))
        img_field = image_resize(im, final_size)

        # entry hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background, fill=hover_bg)
        draw.line(ss(12, 388, 788, 388), fill=shades.d3, width=ss(4))
        img_hover = image_resize(im, final_size)

        # entry field focus
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ss(12, 387, 788, 387), fill=focus_color, width=ss(5))
        img_focus = image_resize(im, final_size)

        # entry field disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled)
        draw.line(ss(12, 387, 788, 387), fill=disabled, width=ss(2))
        img_disabled = image_resize(im, final_size)

        self.register_assets(scheme.name, img_field, img_hover, img_focus,
                             img_disabled)

        el_name = f'{ttkstyle}.field'
        elem = self.style.element_image_builder(
            el_name, img_field, sticky=NSEW, border=ss(6), width=ss(200),
            height=ss(50))
        elem.map('disabled', img_disabled)
        elem.map('focus', img_focus)
        elem.map('hover', img_hover)
        elem.build()

        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(el_name), [
                Element('Entry.padding', sticky=NSEW), [
                    Element('Entry.textarea', sticky=NSEW)]]])

        # normal style
        self.style.configure(
            style=ttkstyle, foreground=foreground, insertcolor=foreground,
            selectbackground=scheme.primary, selectforeground=select_fg,
            font='TkDefaultFont', padding=4)

        # state style map
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])

    def create_combobox_style(self, options):
        """Create a combobox style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'light'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_bg = scheme.get_shades('background')
        shades_lt = scheme.get_shades('light')
        disabled = shades_lt.d3 if scheme.mode == LIGHT else shades_lt.d4
        background = shades.d2
        foreground = scheme.foreground
        focus_color = scheme.primary if colorname == 'light' else shades.base
        hover_bg = shades_bg.l1 if scheme.mode == DARK else shades_lt.base

        img_size = ss(800, 400)
        final_size = ss(200, 100)
        common = {'xy': ss(10, 10, 790, 390), 'radius': ss(16), 'width': ss(2)}

        # combo field
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ss(12, 388, 788, 388), fill=shades.d3, width=ss(4))
        img_field = image_resize(im, final_size)

        # combo hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background, fill=hover_bg)
        draw.line(ss(12, 388, 788, 388), fill=shades.d3, width=ss(4))
        img_hover = image_resize(im, final_size)

        # combo focus
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background)
        draw.line(ss(12, 387, 788, 387), fill=focus_color, width=ss(5))
        img_focus = image_resize(im, final_size)

        # combo disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled)
        img_disabled = image_resize(im, final_size)

        # create field element
        el_field = f'{ttkstyle}.field'
        elem = self.style.element_image_builder(
            el_field, img_field, sticky=NSEW, border=ss(6), width=ss(200),
            height=ss(50))
        elem.map('disabled', img_disabled)
        elem.map('focus !readonly', img_focus)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # chevron normal
        im, draw = image_draw(ss(1400, 755))
        draw.line([ss(20, 20), ss(735, 735), ss(700, 700), ss(1380, 20)],
                  fill=foreground, width=ss(100))
        img_chevron = image_resize(im, ss(14, 8))

        # chevron disabled
        im, draw = image_draw(ss(1400, 755))
        draw.line([ss(20, 20), ss(735, 735), ss(700, 700), ss(1380, 20)],
                  fill=disabled, width=ss(100))
        img_chev_dis = image_resize(im, ss(14, 8))

        el_chev = f'{ttkstyle}.chevron'
        elem = self.style.element_image_builder(
            el_chev, img_chevron, sticky='', padding='8 4')
        elem.map('disabled', img_chev_dis)
        elem.build()

        self.register_assets(scheme.name, img_field, img_hover, img_focus,
                             img_disabled, img_chevron, img_chev_dis)

        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{ttkstyle}.field', expand=True), [
                Element('Combobox.padding', sticky=NSEW), [
                    Element(f'{ttkstyle}.chevron', side=RIGHT, sticky=''),
                    Element('Combobox.textarea', side=LEFT, sticky='')]]])

        # normal style
        self.style.configure(style=ttkstyle, foreground=foreground,
                             insertcolor=foreground,
                             selectbackground=shades_bg.base,
                             selectforeground=foreground, padding='8 4')

        # state style map
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])
        self.style.state_map(ttkstyle, 'selectbackground', [
            ('hover !disabled', hover_bg)])

        # setup options for scrollbar
        opt = options.copy()
        opt['orient'] = VERTICAL
        opt['ttkstyle'] = 'TCombobox.Vertical.TScrollbar'
        self.create_scrollbar_style(opt)

    @staticmethod
    def create_combobox_popdown_style(options):
        """Style the embedded popdown window within the combobox"""
        scheme = options['scheme']

        # style colors
        shades_bg = scheme.get_shades('background')
        shades_lt = scheme.get_shades('light')
        foreground = scheme.foreground
        selectbackground = scheme.info
        selectforeground = scheme.get_foreground('info')
        background = shades_bg.l1 if scheme.mode == DARK else shades_lt.base

        # set the application window style
        widget = options['widget']

        tk_settings = []
        tk_settings.extend(["-borderwidth", 0])
        tk_settings.extend(["-background", background])
        tk_settings.extend(["-foreground", foreground])
        tk_settings.extend(["-selectbackground", selectbackground])
        tk_settings.extend(["-selectforeground", selectforeground])

        # set popdown style
        popdown = widget.tk.eval(f"ttk::combobox::PopdownWindow {str(widget)}")
        widget.tk.call(f"{popdown}.f.l", "configure", *tk_settings)

        # set scrollbar style
        sb_style = "TCombobox.Vertical.TScrollbar"
        widget.tk.call(f"{popdown}.f.sb", "configure", "-style", sb_style)

    def create_menubutton_style(self, options):
        """Create the default menubutton style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'primary'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        foreground = scheme.get_foreground(colorname)
        background = shades.base
        hover = shades.l1 if scheme.mode == LIGHT else shades.d1
        disabled = shades.l2
        img_size = ss(800, 400)
        final_size = ss(200, 100)
        common = {'xy': ss(10, 10, 790, 390), 'radius': ss(16),
                  'outline': shades.d2, 'width': ss(3)}

        # normal image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, fill=background)
        img_norm = image_resize(im, final_size)

        # hover image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, fill=hover)
        img_hover = image_resize(im, final_size)

        # button image element
        elem = self.style.element_image_builder(
            f'{ttkstyle}.button', img_norm, sticky=NSEW, border=ss(6),
            width=ss(200), height=ss(50))
        elem.map('hover !disabled', img_hover)
        elem.build()

        # chevron normal
        im, draw = image_draw(ss(1400, 755))
        draw.line([ss(20, 20), ss(735, 735), ss(700, 700), ss(1380, 20)],
                  fill=foreground, width=ss(100))
        img_chev_norm = image_resize(im, ss(14, 8))

        # chevron disabled
        im, draw = image_draw(ss(1400, 755))
        draw.line([ss(20, 20), ss(735, 735), ss(700, 700), ss(1380, 20)],
                  fill=disabled, width=ss(100))
        img_chev_dis = image_resize(im, ss(14, 8))

        # chevron element
        el_chev = f'{ttkstyle}.chevron'
        elem = self.style.element_image_builder(el_chev, img_chev_norm,
                                                sticky='')
        elem.map('disabled', img_chev_dis)
        elem.build()

        self.register_assets(scheme.name, img_norm, img_hover, img_chev_norm,
                             img_chev_dis)

        # button layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{ttkstyle}.button', sticky=NSEW), [
                Element('Menubutton.focus', sticky=NSEW), [
                    Element('Menubutton.padding', sticky=EW), [
                        Element(f'{ttkstyle}.chevron', side=RIGHT, sticky=''),
                        Element('Menubutton.label', side=LEFT, sticky='')]]]])

        # normal state
        self.style.configure(style=ttkstyle, foreground=foreground,
                             anchor=CENTER, padding='8 4')

        # state map
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])

    def create_outline_menubutton_style(self, options):
        """Create an outline menubutton style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'primary'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_lt = scheme.get_shades('light')
        shades_bg = scheme.get_shades('background')
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        background = foreground = shades.base
        hover_bg = shades_bg.l2 if scheme.mode == DARK else shades_lt.base

        # create style assets
        img_size = ss(800, 400)
        final_size = ss(200, 100)
        common = {'xy': ss(10, 10, 790, 390), 'radius': ss(16)}

        # normal image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background, width=ss(4))
        img_norm = image_resize(im, final_size)

        # hover image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background, width=ss(4),
                               fill=hover_bg)
        img_hover = image_resize(im, final_size)

        # pressed image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background, width=ss(4),
                               fill=hover_bg)
        img_pressed = image_resize(im, final_size)

        # disable image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled, width=ss(2))
        img_disabled = image_resize(im, final_size)

        # button image element
        el_name = f'{ttkstyle}.button'
        elem = self.style.element_image_builder(
            el_name, image=img_norm, sticky=NSEW, border=ss(6), width=ss(200),
            height=ss(50))
        elem.map('disabled', img_disabled)
        elem.map('pressed !disabled', img_pressed)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # chevron normal
        im, draw = image_draw(ss(1400, 755))
        draw.line([ss(20, 20), ss(735, 735), ss(700, 700), ss(1380, 20)],
                  fill=foreground, width=ss(100))
        img_chev_norm = image_resize(im, ss(14, 8))

        # chevron disabled
        im, draw = image_draw(ss(1400, 755))
        draw.line([ss(20, 20), ss(735, 735), ss(700, 700), ss(1380, 20)],
                  fill=disabled, width=ss(100))
        img_chev_dis = image_resize(im, ss(14, 8))

        # chevron element
        el_chev = f'{ttkstyle}.chevron'
        elem = self.style.element_image_builder(el_chev, img_chev_norm,
                                                sticky='')
        elem.map('disabled', img_chev_dis)
        elem.build()

        self.register_assets(scheme.name, img_norm, img_hover, img_pressed,
                             img_disabled, img_chev_norm, img_chev_dis)

        # button layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{ttkstyle}.button', sticky=NSEW), [
                Element('Menubutton.focus', sticky=NSEW), [
                    Element('Menubutton.padding', sticky=EW), [
                        Element(f'{ttkstyle}.chevron', side=RIGHT, sticky=''),
                        Element('Menubutton.label', side=LEFT, sticky='')]]]])

        # normal state
        self.style.configure(style=ttkstyle, foreground=foreground,
                             focuscolor=foreground, anchor=CENTER,
                             padding='8 4')

        # state map
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])

    def create_notebook_style(self, options):
        """Create the notebook style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        colorname = options['color'] or 'light'
        shades = scheme.get_shades(colorname)
        background = scheme.background
        inactive_bg = shades.d1 if scheme.mode == LIGHT else shades.d4
        bordercolor = shades.d2 if scheme.mode == LIGHT else shades.d4

        # notebook tab
        img_size = ss(64, 64)
        end_size = ss(32, 32)
        common = {'xy': ss(1, 1, 63, 80), 'radius': ss(12), 'width': ss(1)}

        # notebook tab active
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=bordercolor, fill=background)
        img_tab_on = image_resize(im, end_size)

        # notebook tab inactive
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=inactive_bg, fill=inactive_bg)
        img_tab_off = image_resize(im, end_size)

        # notebook tab element
        e_name = ttkstyle.replace('TN', 'N')
        elem = self.style.element_image_builder(
            f'{e_name}.tab', image=img_tab_on, border=ss(6, 6, 6, 0),
            padding=ss(16, 14, 14, 6), height=ss(end_size[0]))
        elem.map('!selected', img_tab_off)
        elem.build()

        # notebook border
        im_size = ss(1600, 1600)
        final_size = ss(64, 64)
        im, draw = image_draw(im_size)
        draw.rounded_rectangle((10, 10, 1590, 1800), radius=ss(1600 * 0.12),
                               outline=bordercolor, width=ss(24),
                               fill=inactive_bg)
        img_border = image_resize(im, final_size)
        im.resize(end_size, Image.LANCZOS).save('.notebook-border.png')

        self.register_assets(scheme.name, img_tab_on, img_tab_off, img_border)

        # notebook border element
        self.style.element_create(f'{e_name}.border', 'image', img_border,
                                  sticky=NSEW, border=ss(6, 6, 6, 0),
                                  width=ss(64), height=ss(64))

        # notebook layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{e_name}.border'), [
                Element(f'{ttkstyle}.Tab', expand=True)]])

        self.style.configure(ttkstyle, padding='1')
        self.style.configure(f'{ttkstyle}.Tab', focuscolor='')
        self.style.state_map(f'{ttkstyle}.Tab', 'background', [
            ('selected', background)])

    def create_panedwindow_style(self, options):
        """Create a panedwindow style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'light'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        background = shades.d3 if colorname == LIGHT else shades.base

        # normal state
        self.style.configure(ttkstyle, background=background)
        st = self.scale_size(1)
        self.style.configure('Sash', gripcount=0, sashthickness=st)

    def create_progressbar_style(self, options):
        """Create a progressbar style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'primary'
        orient = options['orient']
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_bg = scheme.get_shades('background')
        shades_lt = scheme.get_shades('light')
        background = shades.base
        outline = shades_bg.d2
        troughcolor = shades_lt.d3 if scheme.mode == DARK else shades_bg.d1

        if orient == VERTICAL:
            final_size = ss(10, 40)
            img_size = ss(500, 2000)
            common = {'xy': ss(10, 10, 490, 1990), 'radius': ss(250)}
        else:
            final_size = ss(40, 10)
            img_size = ss(2000, 500)
            common = {'xy': ss(10, 10, 1990, 490), 'radius': ss(250)}

        # progressbar
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, fill=background)
        img_pbar = image_resize(im, final_size)

        # trough
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, fill=troughcolor, outline=outline,
                               width=ss(12))
        img_trough = image_resize(im, final_size)

        self.register_assets(scheme.name, img_pbar, img_trough)

        # create elements
        self.style.element_create(f'{ttkstyle}.pbar', 'image', img_pbar,
                                  border=ss(4))
        self.style.element_create(f'{ttkstyle}.trough', 'image', img_trough,
                                  border=ss(4), padding=0)

        # create progressbar layout
        sticky = EW if orient == HORIZONTAL else NS
        side = LEFT if orient == HORIZONTAL else BOTTOM
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{ttkstyle}.trough', sticky=EW), [
                Element(f'{ttkstyle}.pbar', side=side, sticky=sticky)]])

    def create_scale_style(self, options):
        """Create a scale style"""
        ss = self.scale_size
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        orient = options['orient']
        colorname = options['color'] or 'primary'
        shades = scheme.get_shades(colorname)
        shades_bg = scheme.get_shades('background')
        shades_lt = scheme.get_shades('light')
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        background = shades.base
        app_bg = scheme.background
        outline = shades_lt.d3
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        pressed = shades.d2 if scheme.mode == DARK else shades.l2
        hover = shades.d1 if scheme.mode == DARK else shades.l1
        troughcolor = shades_lt.d3 if scheme.mode == DARK else shades_bg.d1
        hover_bg = shades_bg.l1 if scheme.mode == DARK else shades_lt.base

        # create scale assets
        size = ss(32)
        img_size = ss(640, 640)
        rect = ss(20, 20, 620, 620)
        radius = ss(310)
        common = {'xy': rect, 'radius': radius}

        # handle normal
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, width=150, outline=app_bg,
                               fill=background)
        draw.rounded_rectangle(**common, width=20, outline=outline)
        img_normal = PhotoImage(image=im.resize((size, size), Image.LANCZOS))

        # pressed state image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, width=180, outline=hover_bg,
                               fill=pressed)
        draw.rounded_rectangle(**common, width=20, outline=outline)
        img_pressed = image_resize(im, (size, size))

        # hover state image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, width=120, outline=hover_bg,
                               fill=hover)
        draw.rounded_rectangle(**common, width=20, outline=outline)
        img_hover = image_resize(im, (size, size))

        # disabled state image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, width=150, outline=app_bg,
                               fill=disabled)
        draw.rounded_rectangle(**common, width=20, outline=disabled)
        img_disabled = image_resize(im, (size, size))

        # create slider element
        slider_name = f'{ttkstyle}.slider'
        elem = self.style.element_image_builder(slider_name, img_normal)
        elem.map('disabled', img_disabled)
        elem.map('pressed !disabled', img_pressed)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # track image
        if orient == VERTICAL:
            track_size = self.scale_size(5, 40)
        else:
            track_size = self.scale_size(40, 5)

        img_track = PhotoImage(image=Image.new('RGB', track_size, troughcolor))

        self.register_assets(scheme.name, img_normal, img_pressed, img_hover,
                             img_disabled, img_track)

        # create track element
        track_name = f'{ttkstyle}.track'
        self.style.element_create(track_name, 'image', img_track)

        # slider layout
        side = LEFT if orient == HORIZONTAL else TOP
        sticky = EW if orient == HORIZONTAL else NS

        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            Element(f'{ttkstyle}.focus', expand=True, sticky=NSEW), [
                Element(track_name, sticky=sticky),
                Element(slider_name, side=side)]])

    def create_sizegrip_style(self, options):
        """Create a sizegrip style"""
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or LIGHT
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_bg = scheme.get_shades('background')

        if colorname == LIGHT:
            fill = shades.d3 if scheme.mode == DARK else shades_bg.d2
        else:
            fill = shades.base

        # create sizegrip assets
        box = self.scale_size(1)
        pad = box * 1
        chunk = box + pad  # 4
        w = chunk * 3 + pad  # 14
        h = chunk * 3 + pad  # 14
        size = w, h

        im, draw = image_draw(size)
        draw.rectangle((chunk * 2 + pad, pad, chunk * 3, chunk), fill=fill)
        draw.rectangle((chunk * 2 + pad, chunk + pad, chunk * 3, chunk * 2),
                       fill=fill)
        draw.rectangle(
            (chunk * 2 + pad, chunk * 2 + pad, chunk * 3, chunk * 3),
            fill=fill)
        draw.rectangle((chunk + pad, chunk + pad, chunk * 2, chunk * 2),
                       fill=fill)
        draw.rectangle((chunk + pad, chunk * 2 + pad, chunk * 2, chunk * 3),
                       fill=fill)
        draw.rectangle((pad, chunk * 2 + pad, chunk, chunk * 3), fill=fill)

        img_grip = PhotoImage(image=im)
        self.register_assets(scheme.name, img_grip)

        # widget element
        element_name = f'{ttkstyle}.sizegrip'
        self.style.element_create(element_name, 'image', img_grip)

        # widget layout
        self.style.element_layout_builder(ttkstyle).build([
            Element(element_name, side=BOTTOM, sticky=SE)])
