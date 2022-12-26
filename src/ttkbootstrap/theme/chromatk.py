from PIL import Image
from PIL.ImageTk import PhotoImage
from ttkbootstrap.theme.engine import ThemeEngine, image_draw, image_resize
from ttkbootstrap.constants import *
from ttkbootstrap.style.element import ElementLayout
from tkinter.font import Font


class ChromatkEngine(ThemeEngine):

    def __init__(self, style):
        super().__init__('chromatk', 'clam', style)
        self.register_keywords()

    def register_keywords(self):
        self.handler_set('button', self.create_button_style)
        self.handler_set('outline-button', self.create_outline_button_style)
        self.handler_set('link-button', self.create_link_button_style)
        self.handler_set('checkbutton', self.create_checkbutton_style)
        self.handler_set('radiobutton', self.create_radiobutton_style)
        self.handler_set('switch', self.create_switch_style)
        self.handler_set('scrollbar', self.create_scrollbar_style)
        self.handler_set('spinbox', self.create_spinbox_style)
        self.handler_set('tk-tk', self.create_window_style)

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

        # pressed image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, fill=pressed)
        img_pressed = image_resize(im, final_size)

        # button image element
        elem = self.style.element_image_builder(
            f'{ttkstyle}.button', img_norm, sticky=NSEW, border=ss(6),
            width=ss(200), height=ss(50))
        elem.map('pressed !disabled', img_pressed)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # button layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            ElementLayout(f'{ttkstyle}.button', expand=True), [
                ElementLayout('Button.padding'), [
                    ElementLayout('Button.label', expand=True)]]])

        self.register_assets(scheme.name, img_norm, img_hover, img_pressed)

        # normal state
        self.style.configure(
            style=ttkstyle, foreground=foreground, focuscolor=foreground,
            relief=RAISED, anchor=CENTER, padding='8 4')

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
        img_size = ss(800, 400)
        final_size = ss(200, 100)
        common = {'xy': ss(10, 10, 790, 390), 'radius': ss(16)}

        # normal image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=background, width=ss(4))
        img_norm = image_resize(im, final_size)

        # hover image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=background, width=ss(4), fill=hover_bg)
        img_hover = image_resize(im, final_size)

        # pressed image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=background, width=ss(4), fill=hover_bg)
        img_pressed = image_resize(im, final_size)

        # disable image
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled, width=ss(2))
        img_disabled = image_resize(im, final_size)

        self.register_assets(scheme.name, img_norm, img_hover, img_pressed,
                             img_disabled)

        # button image element
        el_name = f'{ttkstyle}.button'
        elem = self.style.element_image_builder(
            name=el_name, image=img_norm, sticky=NSEW, border=ss(6),
            width=ss(200), height=ss(50))
        elem.map('disabled', img_disabled)
        elem.map('pressed !disabled', img_pressed)
        elem.map('hover !disabled', img_hover)
        elem.build()

        # button layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            ElementLayout(el_name, sticky=NSEW), [
                ElementLayout('Button.padding'), [
                    ElementLayout('Button.label', side=LEFT, expand=True)]]])

        # normal state
        self.style.configure(
            style=ttkstyle, foreground=foreground, relief=RAISED,
            focuscolor=foreground, anchor=CENTER, padding='8 4')

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
            padding='8 4', anchor=CENTER)

        # normal image
        im = PhotoImage(Image.new('RGBA', ss(200, 100)))

        # button image element
        elem = self.style.element_image_builder(
            name=f'{ttkstyle}.button', image=im, sticky=NSEW, border=ss(6),
            width=ss(200), height=ss(50)).build()

        self.register_assets(scheme.name, im)

        # button layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            ElementLayout(f'{ttkstyle}.button', expand=True), [
                ElementLayout('Button.padding'), [
                    ElementLayout('Button.label', expand=True)]]])

        # state style maps
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled),
            ('hover !disabled', hover)])
        self.style.state_map(ttkstyle, 'shiftrelief', [
            ('pressed !disabled', '-2')])
        self.style.state_map(ttkstyle, 'focuscolor', [
            ('hover', hover)])

    def create_checkbutton_style(self, options):
        ss = self.scale_size
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
        img_size = ss(640, 640)
        final_size = ss(32, 32)
        rect_size = ss(10, 10, 630, 630)
        radius = img_size[0] * 0.12
        common = {'xy': rect_size, 'radius': radius}

        # off
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=outline, fill=app_bg, width=ss(24))
        img_off = image_resize(im, final_size)

        # off/hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=outline, fill=hover_off, width=ss(24))
        img_off_hover = image_resize(im, final_size)

        # off/pressed
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=outline, fill=pressed_off, width=ss(24))
        img_off_pressed = image_resize(im, final_size)

        # on
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=background, width=ss(3))
        draw.line(ss(190, 330, 293, 433, 516, 210), width=ss(40),
                  fill=foreground, joint='curve')
        img_on = image_resize(im, final_size)

        # on/hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=hover_on, width=ss(3))
        draw.line(ss(190, 330, 293, 433, 516, 210), width=ss(40),
                  fill=foreground, joint='curve')
        img_on_hover = image_resize(im, final_size)

        # on/pressed
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=pressed_on, width=ss(3))
        draw.line(ss(190, 330, 293, 433, 516, 210), width=ss(40),
                  fill=foreground, joint='curve')
        img_on_pressed = image_resize(im, final_size)

        # on/disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=disabled, fill=background, width=ss(3))
        draw.line(ss(190, 330, 293, 433, 516, 210), width=ss(40),
                  fill=disabled, joint='curve')
        img_on_dis = image_resize(im, final_size)

        # alt
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=background, width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=foreground)
        img_alt = image_resize(im, final_size)

        # alt
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=pressed_on, width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=foreground)
        img_alt_pressed = image_resize(im, final_size)

        # alt
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=shades_bg.d2, fill=hover_on, width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=foreground)
        img_alt_hover = image_resize(im, final_size)

        # alt/disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=disabled, fill=background, width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=disabled)
        img_alt_dis = image_resize(im, final_size)

        # disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(
            **common, outline=disabled, fill=foreground, width=ss(12))
        img_dis = image_resize(im, final_size)

        # create image element
        element = ttkstyle.replace('.TC', '.C')

        elem = self.style.element_image_builder(
            name=f'{element}.indicator', image=img_on, border=ss(24, 0),
            sticky=NS)

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
                             font='TKBody')

        # state mapping
        self.style.state_map(style=ttkstyle, option='foreground', statespec=[
            ('disabled', disabled)])

        # style layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            ElementLayout('Checkbutton.padding', sticky=NSEW), [
                ElementLayout(f'{element}.indicator', side=LEFT, sticky=''),
                ElementLayout('Checkbutton.focus', side=LEFT, sticky='')], [
                    ElementLayout('Checkbutton.label', sticky=NSEW)]])

    def create_radiobutton_style(self, options):
        ss = self.scale_size
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
        final_size = ss(32, 32)
        ellipse_size = ss(10, 10, 630, 630)

        # off
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=outline, fill=app_bg,
                     width=ss(24))
        img_off = image_resize(im, final_size)

        # off/hover
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=outline, fill=hover_off,
                     width=ss(24))
        img_off_hover = image_resize(im, final_size)

        # off/pressed
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=outline, fill=app_bg,
                     width=ss(140))
        draw.ellipse(ellipse_size, outline=outline, width=ss(24))  # outer
        img_off_pressed = image_resize(im, final_size)

        # on
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=background, fill=app_bg,
                     width=ss(140))
        draw.ellipse(ellipse_size, outline=shades.d2, width=ss(3))  # outer
        img_on = image_resize(im, final_size)

        # on/hover
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=hover_on, fill=app_bg,
                     width=ss(110))
        draw.ellipse(ellipse_size, outline=shades.d2, width=ss(3))  # outer
        img_on_hover = image_resize(im, final_size)

        # on/pressed
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=pressed_on, fill=app_bg,
                     width=ss(140))
        draw.ellipse(ellipse_size, outline=shades.d2, width=ss(3))  # outer
        img_on_pressed = image_resize(im, final_size)

        # radio on/disabled
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=disabled, fill=app_bg,
                     width=ss(140))
        draw.ellipse(ellipse_size, outline=outline, width=ss(3))  # outer
        img_on_dis = image_resize(im, final_size)

        # radio disabled
        im, draw = image_draw(img_size)
        draw.ellipse(ellipse_size, outline=disabled, fill=app_bg,
                     width=ss(24))
        img_dis = image_resize(im, final_size)

        # create image elements
        borderpad = ss(24, 0)

        elem = self.style.element_image_builder(
            f'{ttkstyle}.indicator', img_on, border=borderpad, sticky=NS)
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
            background=scheme.background, focuscolor='')

        # state mapping
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])

        # style layout
        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            ElementLayout('Radiobutton.padding', sticky=NSEW), [
                ElementLayout(f'{ttkstyle}.indicator', side=LEFT),
                ElementLayout('Radiobutton.focus', side=LEFT, sticky=NSEW)], [
                    ElementLayout('Radiobutton.label', side=LEFT)]])

    def create_switch_style(self, options):
        ss = self.scale_size
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
        final_size = ss(60, 30)
        img_size = ss(1200, 600)
        outer_rect = ss(10, 10, 1190, 590)
        inner_rect = ss(622, 34, 1166, 566)

        # off - normal
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=outline, width=ss(24),
                               fill=app_bg, radius=ss(300))
        draw.rounded_rectangle(inner_rect, outline=app_bg, width=ss(80),
                               fill=outline, radius=ss(290))
        img_off = image_resize(im.rotate(180), final_size)

        # off - hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=outline, width=ss(24),
                               fill=app_bg, radius=ss(300))
        draw.rounded_rectangle(inner_rect, outline=app_bg, width=ss(60),
                               fill=outline, radius=ss(290))
        img_off_hover = image_resize(im.rotate(180), final_size)

        # off - pressed
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=outline, width=ss(24),
                               fill=app_bg, radius=ss(300))
        draw.rounded_rectangle(ss(500, 34, 1100, 566), outline=app_bg,
                               width=ss(60), fill=outline, radius=ss(290))
        img_off_pressed = image_resize(im.rotate(180), final_size)

        # on - normal
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=shades.d2, width=ss(6),
                               fill=background, radius=ss(300))
        draw.rounded_rectangle(inner_rect, outline=background, width=ss(80),
                               fill=app_bg, radius=ss(290))
        img_on = image_resize(im, final_size)

        # on - hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=shades.d2, width=ss(6),
                               fill=hover_on, radius=ss(300))
        draw.rounded_rectangle(inner_rect, outline=hover_on, width=ss(60),
                               fill=app_bg, radius=ss(290))
        img_on_hover = image_resize(im, final_size)

        # on - pressed
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, fill=pressed_on, radius=ss(300))
        draw.rounded_rectangle(ss(500, 34, 1100, 566), outline=pressed_on,
                               width=ss(60), fill=app_bg, radius=ss(290))
        img_on_pressed = image_resize(im, final_size)

        # off - disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=disabled, width=ss(24),
                               fill=app_bg, radius=ss(300))
        draw.rounded_rectangle(inner_rect, outline=app_bg, width=ss(80),
                               fill=disabled, radius=ss(290))
        img_off_dis = image_resize(im.rotate(180), final_size)

        # on - disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(outer_rect, outline=outline, width=ss(6),
                               fill=disabled, radius=ss(300))
        draw.rounded_rectangle(inner_rect, outline=disabled, width=ss(80),
                               fill=app_bg, radius=ss(290))
        img_on_dis = image_resize(im, final_size)

        # style element
        elem = self.style.element_image_builder(
            f'{ttkstyle}.indicator', img_on, width=60, height=30,
            padding='0 0 75 0', sticky='')
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
            ElementLayout('Toolbutton.border', sticky=NSEW), [
                ElementLayout('Toolbutton.padding', sticky=NSEW), [
                    ElementLayout(f'{ttkstyle}.indicator', side=LEFT),
                    ElementLayout('Toolbutton.label', side=RIGHT, expand=True)]]])

        # normal style
        self.style.configure(
            ttkstyle, relief=FLAT, borderwidth=0, foreground=scheme.foreground,
            background=scheme.background)

        # state map
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])

    def create_scrollbar_style(self, options):
        ss = self.scale_size
        scheme = options['scheme']
        orient = str(options['orient']) or VERTICAL
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or 'light'
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades_lt = scheme.get_shades(colorname)
        background = shades_lt.d3

        # create scrollbar assets
        pad = ss(25)

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
                ElementLayout(f'{e_name}.trough', sticky=EW), [
                    ElementLayout(f'{e_name}.thumb', sticky=NSEW)]])
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
                ElementLayout(f'{e_name}.trough', sticky=NS), [
                    ElementLayout(f'{e_name}.thumb', sticky=NSEW)]])

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
            el_chev_dw, img_chev_dw, sticky='', padding='16 4')
        elem.map('disabled', img_chev_dw_dis)
        elem.map('pressed !disabled', img_chev_dwp)
        elem.build()

        layout = self.style.element_layout_builder(ttkstyle)
        layout.build([
            ElementLayout(f'{ttkstyle}.field', expand=True), [
                ElementLayout(f'{ttkstyle}.downarrow', side=RIGHT, sticky=NS),
                ElementLayout(f'{ttkstyle}.uparrow', side=RIGHT, sticky=NS)],
                ElementLayout('Spinbox.padding'), [
                    ElementLayout('Spinbox.textarea')]])

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
