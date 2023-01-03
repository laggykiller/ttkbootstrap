from abc import abstractmethod
from typing import TYPE_CHECKING
from PIL.ImageDraw import ImageDraw
from PIL.ImageTk import PhotoImage
from PIL import Image
from ttkbootstrap.publisher import Publisher
from ttkbootstrap.style.scheme import Scheme
from platform import system
from math import ceil


if system() == 'DARWIN':
    BASELINE = 1.000492368291482
else:
    BASELINE = 2.000984736582964  # 3840x2160

if TYPE_CHECKING:
    from ttkbootstrap.style.style import Style


def image_resize(img, size, orient=None):
    if orient is None or orient == 'horizontal':
        return PhotoImage(image=img.resize(size, Image.BICUBIC))
    else:
        return PhotoImage(image=img.rotate(180).resize(size, Image.BICUBIC))


def image_draw(size, mode=None, *args):
    im = Image.new(mode or 'RGBA', size, *args)
    dr = ImageDraw(im)
    return im, dr


class ThemeEngine:

    def __init__(self, name, base, style):
        self._theme_assets = {'fonts': list()}
        self._handlers = dict()
        self._styles = dict()
        self._name = name
        self._base = base
        self._style: 'Style' = style

    @property
    def name(self):
        return self._name

    @property
    def base(self):
        return self._base

    @property
    def style(self):
        return self._style

    def styles(self):
        return self._styles

    def style_exists(self, name, scheme):
        if not self._styles.get(scheme):
            return False
        return name in self._styles.get(scheme)

    def register_style(self, name, scheme):
        if scheme not in self._styles:
            self._styles[scheme] = set()
        self._styles[scheme].add(name)

    def handler_set(self, keyword, callback):
        self._handlers[keyword] = callback
        handler_name = f'{self.name}-{keyword}'
        Publisher.add(handler_name, callback)

    def handler_get(self, keyword):
        return self._handlers.get(keyword)

    def keywords(self):
        return sorted(self._handlers.keys(), key=len, reverse=True)

    @staticmethod
    def parse_scheme(string):
        data = eval(string)
        return Scheme(**data)

    def scale_size(self, *size):
        scaling = self._style.tk.call('tk', 'scaling')
        factor = scaling / BASELINE
        sizes = tuple([ceil(s * factor) for s in size])
        if len(sizes) == 1:
            return sizes[0]
        return sizes

    @abstractmethod
    def register_keywords(self):
        raise NotImplemented

    @abstractmethod
    def create_named_fonts(self):
        raise NotImplemented

    def register_assets(self, key, *asset):
        if key not in self._theme_assets:
            self._theme_assets[key] = set()
        if isinstance(self._theme_assets[key], list):
            self._theme_assets[key].extend(asset)
        else:
            self._theme_assets[key].update(asset)

    def element_builder(self, name, image, **kw):
        return self.style.element_image_builder(name, image, **kw)

    def layout_builder(self, style):
        return self.style.element_layout_builder(style)

    def element_create(self, name, etype, *args, **kw):
        return self.style.element_create(name, etype, *args, **kw)

    def configure(self, style, **kw):
        return self.style.configure(style, **kw)

    def map(self, style, option, statespec):
        return self.style.state_map(style, option, statespec)
