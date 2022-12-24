from PIL.ImageDraw import ImageDraw
from PIL.ImageTk import PhotoImage
from PIL import Image
from ttkbootstrap.theme.engine import ThemeEngine, image_draw, image_resize
from ttkbootstrap.constants import *
from ttkbootstrap.style.element import ElementLayout
from tkinter.font import Font


class BootstyleEngine(ThemeEngine):

    def __init__(self, style):
        super().__init__('bootstyle', 'clam', style)
        self.register_keywords()

    def register_keywords(self):
        self.handler_set('button', self.create_button_style)
        self.handler_set('outline-button', self.create_outline_button_style)
        self.handler_set('link-button', self.create_link_button_style)
        self.handler_set('checkbutton', self.create_checkbutton_style)
        self.handler_set('radiobutton', self.create_radiobutton_style)
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

    def create_button_style(self, options):
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

        # normal state
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
            padding='10 5',
            anchor=CENTER)

        # state mapping
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled)])
        self.style.state_map(ttkstyle, 'background', [
            ('pressed !disabled', pressed),
            ('hover !disabled', hover)])
        self.style.state_map(ttkstyle, 'darkcolor', [
            ('pressed !disabled', pressed),
            ('hover !disabled', hover)])
        self.style.state_map(ttkstyle, 'lightcolor', [
            ('pressed !disabled', pressed),
            ('hover !disabled', hover)])

    def create_outline_button_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades = scheme.get_shades(colorname)
        shades_lt = scheme.get_shades('light')
        shades_bg = scheme.get_shades('background')
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        bordercolor = foreground = shades.base
        hover_fg = scheme.get_foreground(colorname)
        hover_bg = bordercolor

        # normal state
        self.style.configure(ttkstyle,
                             font='TkBody',
                             foreground=foreground,
                             focuscolor=foreground,
                             background=shades_bg.base,
                             darkcolor=shades_bg.base,
                             lightcolor=shades_bg.base,
                             bordercolor=bordercolor,
                             anchor=CENTER,
                             relief=RAISED,
                             focusthickness=0,
                             padding='10 5')

        # state mapping
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled),
            ('hover !disabled', hover_fg)])
        self.style.state_map(ttkstyle, 'focuscolor', [
            ('hover !disabled', hover_fg)])
        self.style.state_map(ttkstyle, 'shiftrelief', [
            ('pressed !disabled', -1)])
        self.style.state_map(ttkstyle, 'background', [
            ('hover !disabled', hover_bg)])
        self.style.state_map(ttkstyle, 'darkcolor', [
            ('hover !disabled', hover_bg)])
        self.style.state_map(ttkstyle, 'lightcolor', [
            ('hover !disabled', hover_bg)])

    def create_link_button_style(self, options):
        scheme = options['scheme']
        ttkstyle = options['ttkstyle']
        colorname = options['color'] or PRIMARY
        self.style_register(options['ttkstyle'], scheme)

        # style colors
        shades_lt = scheme.get_shades('light')
        disabled = shades_lt.d2 if scheme.mode == LIGHT else shades_lt.d4
        foreground = scheme.get_color(colorname)
        background = scheme.background
        hover = scheme.info

        # normal state
        self.style.configure(
            ttkstyle,
            font='TkBody',
            relief=RAISED,
            foreground=foreground,
            focuscolor=foreground,
            background=background,
            bordercolor=background,
            lightcolor=background,
            darkcolor=background,
            anchor=CENTER,
            focusthickness=0,
            padding='10 5')

        # state mapping
        self.style.state_map(ttkstyle, 'foreground', [
            ('disabled', disabled),
            ('hover', hover)])
        self.style.state_map(ttkstyle, 'shiftrelief', [
            ('pressed !disabled', -2)])
        self.style.state_map(ttkstyle, 'focuscolor', [
            ('hover !disabled', hover)])

        for state in ('background', 'bordercolor', 'lightcolor', 'darkcolor'):
            self.style.state_map(ttkstyle, state, [
                ('disabled', background),
                ('pressed', background),
                ('hover', background)])

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
        draw.rounded_rectangle(**common, outline=outline, fill=app_bg,
                               width=ss(24))
        img_off = image_resize(im, final_size)

        # off/hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=outline, fill=hover_off,
                               width=ss(24))
        img_off_hover = image_resize(im, final_size)

        # off/pressed
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=outline, fill=pressed_off,
                               width=ss(24))
        img_off_pressed = image_resize(im, final_size)

        # on
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=background,
                               width=ss(3))
        draw.line(ss(190, 330, 293, 433, 516, 210), width=ss(40),
                  fill=foreground, joint='curve')
        img_on = image_resize(im, final_size)

        # on/hover
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=hover_on,
                               width=ss(3))
        draw.line(ss(190, 330, 293, 433, 516, 210), width=ss(40),
                  fill=foreground, joint='curve')
        img_on_hover = image_resize(im, final_size)

        # on/pressed
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=pressed_on,
                               width=ss(3))
        draw.line(ss(190, 330, 293, 433, 516, 210), width=ss(40),
                  fill=foreground, joint='curve')
        img_on_pressed = image_resize(im, final_size)

        # on/disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled, fill=background,
                               width=ss(3))
        draw.line(ss(190, 330, 293, 433, 516, 210), width=ss(40),
                  fill=disabled, joint='curve')
        img_on_dis = image_resize(im, final_size)

        # alt
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=background,
                               width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=foreground)
        img_alt = image_resize(im, final_size)

        # alt
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=pressed_on,
                               width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=foreground)
        img_alt_pressed = image_resize(im, final_size)

        # alt
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=shades_bg.d2, fill=hover_on,
                               width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=foreground)
        img_alt_hover = image_resize(im, final_size)

        # alt/disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled, fill=background,
                               width=ss(3))
        draw.line(ss(213, 320, 427, 320), width=ss(40), fill=disabled)
        img_alt_dis = image_resize(im, final_size)

        # disabled
        im, draw = image_draw(img_size)
        draw.rounded_rectangle(**common, outline=disabled, fill=foreground,
                               width=ss(12))
        img_dis = image_resize(im, final_size)

        # create image element
        element = ttkstyle.replace('.TC', '.C')

        elem = self.style.element_image_builder(
            name=f'{element}.indicator',
            image=img_on,
            border=ss(24, 0),
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
