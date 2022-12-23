from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ttkbootstrap.style.style import Style
    from PIL.ImageTk import PhotoImage


class ElementImageBuilder:

    def __init__(self, style: 'Style', name: str, image: 'PhotoImage', **kw):
        self._style = style
        self._name = name
        self._image = image
        self._kwargs = kw
        self._state_spec = list()

    def map(self, state: str, image: 'PhotoImage'):
        self._state_spec.append((state, str(image)))

    def build(self):
        self._style.element_create(self._name, 'image', self._image,
                                   *self._state_spec, **self._kwargs)


class ElementLayout:

    def __init__(self, name, **kw):
        self.name = name
        self.kwargs = kw
        self.children = list()

    def build(self):
        if self.children:
            self.kwargs['children'] = [c.build() for c in self.children]
        return tuple([self.name, self.kwargs])


class ElementLayoutBuilder:

    def __init__(self, style: 'Style', ttkstyle: str):
        self._style = style
        self._ttkstyle = ttkstyle

    def build(self, layout):
        def assign_parent(obj_layout, parent=None):
            for i, obj in enumerate(obj_layout):
                if isinstance(obj, ElementLayout):
                    if parent is not None:
                        parent.children.append(obj)
                elif isinstance(obj, (list, tuple)):
                    assign_parent(obj, obj_layout[0])
        assign_parent(layout)
        self._style.layout(self._ttkstyle, [layout[0].build()])

