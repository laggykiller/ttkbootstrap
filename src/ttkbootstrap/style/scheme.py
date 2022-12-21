from ttkbootstrap.utils import colorutils
from collections import namedtuple

DEFAULT1 = '#ddd'
DEFAULT2 = '#111'
LIGHT = 'light'
DARK = 'dark'
SHADES = [1.4, 1.3, 1.2, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6]
Shades = namedtuple('Shades', 'l4 l3 l2 l1 base d1 d2 d3 d4')


class Scheme:

    def __init__(self, name, mode, **colors: str):
        """A class that defines a color scheme for a theme.

        Parameters
        ----------
        name : str
            The scheme name.

        mode: Literal['light', 'dark']
            Specifies a light or dark scheme.

        **colors : str
            The key-value pairs that define the scheme colors.
        """
        self.name = name
        self.mode = mode

        # colors
        self.primary = colors.get('primary', DEFAULT1)
        self.secondary = colors.get('secondary', DEFAULT1)
        self.success = colors.get('success', DEFAULT1)
        self.info = colors.get('info', DEFAULT1)
        self.warning = colors.get('warning', DEFAULT1)
        self.danger = colors.get('danger', DEFAULT1)
        self.light = colors.get('light', DEFAULT1)
        self.dark = colors.get('dark', DEFAULT1)
        self.background = colors.get('background', DEFAULT1)
        self.foreground = colors.get('foreground', DEFAULT2)

    def get_foreground(self, color_name):
        """Return the foreground color appropriate for the color name.

        Parameters
        ----------
        color_name : str
            The color scheme name.

        Returns
        -------
        str
            A hexadecimal color value.
        """
        if color_name == 'light':
            return self.dark
        elif color_name == 'dark':
            return self.light
        elif color_name == 'background':
            return self.foreground
        elif self.mode == 'dark':
            return self.foreground
        else:
            return self.background

    def get_color(self, colorname):
        """Get the value of the specified color.

        Parameters
        ----------
        colorname : str
            The name of the color.

        Returns
        -------
        str
            A hexadecimal color value.
        """
        if colorname in ['name', 'mode']:
            return
        return self.__dict__.get(colorname)

    def get_shades(self, colorname):
        """Get a list of shades for this color.
        The list will include a range of colors with a factor between 1.4 and
        0.6 of the luminosity of the original color, which is at index 4.

        Parameters
        ----------
        colorname : str
            The name of the primary scheme color.

        Returns
        -------
        Shades
            A list of hexadecimal color values.
        """
        colors = []
        value = self.get_color(colorname)
        red, grn, blu = colorutils.color_to_rgb(value, 'hex')
        for shade in SHADES:
            color = f'#{int(max(0, min(red * shade, 255))):02x}'
            color += f'{int(max(0, min(grn * shade, 255))):02x}'
            color += f'{int(max(0, min(blu * shade, 255))):02x}'
            colors.append(color)
        return Shades(*colors)

    def __iter__(self):
        colors = self.__dict__.copy()
        del colors['name']
        del colors['mode']
        return iter(colors)

    def __repr__(self):
        return str(self.__dict__)


# -----------------------------------------------------------------------------
# Standard built-in color schemes
# -----------------------------------------------------------------------------

std_schemes = dict()

std_schemes['cosmo'] = Scheme(
    name='cosmo',
    mode='light',
    primary='#2780e3',
    secondary='#7E8081',
    success='#3fb618',
    info='#9954bb',
    warning='#ff7518',
    danger='#ff0039',
    light='#F8F9FA',
    dark='#373A3C',
    background='#fff',
    foreground='#373a3c')

std_schemes['flatly'] = Scheme(
    name='flatly',
    mode='light',
    primary='#2c3e50',
    secondary='#95a5a6',
    success='#18bc9c',
    info='#3498db',
    warning='#f39c12',
    danger='#e74c3c',
    light='#ecf0f1',
    dark='#7b8a8b',
    background='#fff',
    foreground='#212529')

std_schemes['minty'] = Scheme(
    name='minty',
    mode='light',
    primary='#78c2ad',
    secondary='#f3969a',
    success='#56cc9d',
    info='#6cc3d5',
    warning='#ffce67',
    danger='#ff7851',
    light='#f8f9fa',
    dark='#343a40',
    background='#fff',
    foreground='#5a5a5a')

std_schemes['superhero'] = Scheme(
    name='superhero',
    mode='dark',
    primary='#4c9be8',
    secondary='#4e5d6c',
    success='#5cb85c',
    info='#5bc0de',
    warning='#f0ad4e',
    danger='#d9534f',
    light='#aab6c2',
    dark='#20374c',
    background='#2b3e50',
    foreground='#fff')
