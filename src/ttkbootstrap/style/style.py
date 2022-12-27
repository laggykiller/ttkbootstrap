from collections import namedtuple
from tkinter.ttk import Style as ttkStyle
from typing import Iterable

from ttkbootstrap.style.scheme import std_schemes, Scheme
from ttkbootstrap.publisher import Publisher
from ttkbootstrap.theme import ChromatkEngine, BootstyleEngine
from ttkbootstrap.style.element import ElementLayoutBuilder
from ttkbootstrap.style.element import ElementImageBuilder

Theme = namedtuple('Theme', 'name scheme engine')

THEME_ENGINES = [ChromatkEngine, BootstyleEngine]
DEFAULT_SCHEME_NAME = 'flatly'
DEFAULT_ENGINE_NAME = 'chromatk'


class Style(ttkStyle):

    _instance = None
    _engines = dict()
    _themes = dict()
    _current_theme: Theme = None
    _schemes = std_schemes.copy()

    def __init__(self, master):
        if Style._instance is not None:
            raise Exception("Use `Style.get_instance`")
        Style._instance = self
        super().__init__(master)

        # initialize built-in theme engines
        self.theme_engine_add(*THEME_ENGINES)
        Publisher.add('route-style-handler', self._route_style_handler)

    @staticmethod
    def instance(master=None):
        if Style._instance is None:
            Style._instance = Style(master)
        return Style._instance

    def theme_engine_add(self, *engine):
        for e in engine:
            theme_engine = e(self)
            self._engines[theme_engine.name] = theme_engine

    def theme_names(self):
        return super().theme_names()

    def theme_use(self, themename=None):
        if themename is None:
            return super().theme_use()

        # existing theme (long name)
        if themename in self.theme_names():
            self._current_theme = self._themes[themename]
            super().theme_use(themename)
            return Publisher.dispatch('theme-changed')

        theme = self._find_theme_scheme_engine(themename)

        # existing theme (short name)
        if theme.name in self.theme_names():
            self._current_theme = self._themes[theme.name]
            super().theme_use(theme.name)
            return Publisher.dispatch('theme-changed')

        # new theme
        self.theme_create(theme)
        self._current_theme = theme
        super().theme_use(theme.name)
        return Publisher.dispatch('theme-changed')

    def theme_current(self):
        return self._current_theme

    def theme_create(self, theme: Theme, parent=None, settings=None):
        self._themes[theme.name] = theme
        parent = parent or theme.engine.base
        return super().theme_create(theme.name, parent, settings)

    def element_clone(self, elementname, themename):
        super().element_create(elementname, 'from', themename)

    def element_layout_builder(self, style: str):
        return ElementLayoutBuilder(self, style)

    def element_image_builder(self, name, image, **kw):
        return ElementImageBuilder(self, name, image, **kw)

    def state_map(self, style: str, option: str, statespec: Iterable):
        self.map(style, **{option: statespec})

    def scheme_create(self, name, mode, **colors):
        self._schemes[name] = Scheme(name, mode, **colors)

    def scheme_get(self, name):
        return self._schemes.get(name)

    def scheme_names(self):
        return tuple(self._schemes.keys())

    def scheme_objects(self):
        return self._schemes.copy()

    def _route_style_handler(self, kw):
        theme = self._current_theme
        handler = kw.get('handler')
        hybrid = kw.get('hybrid')
        ttkstyle = kw.get('ttkstyle')
        event = f'{theme.engine.name}-{handler}'

        # attach scheme to handler message
        kw['scheme'] = theme.scheme

        # hybrid widgets
        if hybrid:
            for style_name in kw['hybrid_styles']:
                sub_event = f'{theme.engine.name}-{style_name}'
                Publisher.dispatch(sub_event, kw)

        # TK widgets
        if ttkstyle == '':
            return Publisher.dispatch(event, kw)

        # TTK widgets
        if not theme.engine.style_exists(ttkstyle, theme.scheme):
            return Publisher.dispatch(event, kw)

    def _find_theme_scheme_engine(self, themename):
        result = themename.split('-')
        if len(result) == 2:
            scheme_name, engine_name = result
            if scheme_name not in self._schemes:
                raise Exception(scheme_name, 'is not a valid color scheme')
            if engine_name not in self._engines:
                raise Exception(engine_name, 'is not a valid theme engine')
            theme_name = f'{scheme_name}-{engine_name}'
            scheme = self._schemes.get(scheme_name)
            engine = self._engines.get(engine_name)
            return Theme(theme_name, scheme, engine)
        elif themename in self._schemes:
            theme_name = f'{themename}-{DEFAULT_ENGINE_NAME}'
            scheme = self._schemes.get(themename)
            engine = self._engines.get(DEFAULT_ENGINE_NAME)
            return Theme(theme_name, scheme, engine)
        elif themename in self._engines:
            theme_name = f'{DEFAULT_SCHEME_NAME}-{themename}'
            scheme = self._schemes.get(DEFAULT_SCHEME_NAME)
            engine = self._engines.get(theme_name)
            return Theme(theme_name, scheme, engine)
        else:
            raise Exception(themename, 'is not a valid scheme or engine')
