import re
from typing import Callable
from abc import abstractmethod
from tkinter import TclError

from ..publisher import Publisher

CUSTOM_KWARGS = ['bootstyle', 'style', 'autostyle']
COLORS = r'primary|secondary|success|info|warning|danger|dark|light'
COLOR_PATTERN = re.compile(COLORS)


def capture_custom_kwargs(kw):
    # extract style information
    custom = dict()
    for k in CUSTOM_KWARGS:
        if k in kw:
            custom[k] = kw.pop(k)
    return custom, kw


class StyledWidget:

    def __init__(self, **kw):
        self._bootstyle = kw.get('bootstyle', '')
        self._is_ttk = kw.get('is_ttk', True)
        self._is_hybrid = kw.get('is_hybrid', False)
        self._hybrid_styles = set()

    @abstractmethod
    def update_widget_style(self, **kw):
        raise NotImplemented

    def _handler_message(self):

        # widget orientation
        try:
            orient = self.cget('orient')
        except TclError:
            orient = None

        # widget color, type, class
        color = kind = klass = ''
        match = re.search(COLOR_PATTERN, self._bootstyle.lower() or '')
        keywords = (self._bootstyle.lower() or '').split('-')
        if match:
            # style has a color
            if len(keywords) == 1:
                color = match.group(0)
            elif len(keywords) == 2:
                color, klass = keywords
            elif len(keywords) == 3:
                color, kind, klass = keywords
        else:
            if len(keywords) == 2:
                kind, klass = keywords
            else:
                klass = self._bootstyle

        if klass in (None, ''):
            temp = self.winfo_class().split('.')[-1]
            if temp[:2].isupper():
                klass = temp[1:].lower()
            else:
                klass = temp.lower()

        if isinstance(klass, Callable):
            klass = klass()

        # the new ttk style
        handler = ''
        ttkstyle = ''
        if self._is_ttk:
            ttkstyle += color + '.' if color else ''
            ttkstyle += kind + '.' if kind else ''
            ttkstyle += str(orient).title() + '.' if orient else ''
            if klass.lower().startswith('t'):
                ttkstyle += klass.title()
            else:
                ttkstyle += 'T' + klass.title()
        else:
            handler = 'tk-'

        handler_kw = [klass]
        if kind:
            handler_kw.insert(0, kind)

        handler = handler + '-'.join(handler_kw)

        kwargs = {
            'ttkstyle': ttkstyle, 'color': color, 'type': kind, 'class': klass,
            'bootstyle': self._bootstyle, 'handler': handler, 'widget': self,
            'hybrid': self._is_hybrid, 'hybrid_styles': self._hybrid_styles
        }
        if orient:
            kwargs['orient'] = orient
        return kwargs


class TTKWidget(StyledWidget):

    def __init__(self, **kw):
        super().__init__(**kw)
        Publisher.add('theme-changed', self.update_widget_style)

    def ttkstyle(self, value=None):
        if value is None:
            ttkstyle = self.cget('style')
            if ttkstyle == '':
                return self.winfo_class()
            else:
                return ttkstyle
        else:
            super().configure(style=value)

    def update_widget_style(self):
        message = self._handler_message()
        Publisher.dispatch('route-style-handler', message)
        self.ttkstyle(message['ttkstyle'])

    def configure(self, cnf=None, **kw):
        # get configuration
        if cnf == 'bootstyle':
            return self._bootstyle

        if cnf is not None:
            return super().configure(cnf)

        # set configuration
        if 'bootstyle' in kw:
            self._bootstyle = kw.pop('bootstyle')

        super().configure(**kw)
        if 'style' in kw or 'bootstyle' in kw:
            self.update_widget_style()


class TKWidget(StyledWidget):

    def __init__(self, **kw):
        super().__init__(is_ttk=False, **kw)
        Publisher.add('theme-changed', self.update_widget_style)

    def update_widget_style(self):
        message = self._handler_message()
        Publisher.dispatch('route-style-handler', message)

    def configure(self, cnf=None, **kw):
        # get configuration
        if cnf == 'bootstyle':
            return self._bootstyle

        if cnf is not None:
            return super().configure(cnf)

        # set configuration
        if 'bootstyle' in kw:
            self._bootstyle = kw.pop('bootstyle')
            self.update_widget_style()

        super().configure(**kw)
