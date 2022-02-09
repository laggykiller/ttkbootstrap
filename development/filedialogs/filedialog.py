import pathlib
from math import ceil
from datetime import datetime
from PIL import Image, ImageTk

import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Dialog
from ttkbootstrap.constants import *
from ttkbootstrap.localization import MessageCatalog as MC

"""
    - get filename
    - get filenames
    - open file
    - open files
    - get directory
    - save filename
    - save filenames

"""

IMAGES = {
    "File": "icons8_folder_40px.png",
    "Dir": "icons8_file_40px.png",
    "Home": "icons8_home_40px.png",
    "User": "icons8_user_folder_40px.png",
    "Desktop": "icons8_desktop_40px.png",
    "Videos": "icons8_movies_folder_40px.png",
    "Music": "icons8_music_folder_40px.png",
    "Pictures": "icons8_pictures_folder_40px.png",
    "Photos": "icons8_pictures_folder_40px.png",
    "Documents": "icons8_documents_folder_40px.png",
    "Downloads": "icons8_downloads_folder_40px.png",
}

SB_IMG_SIZE = (36, 36)  # sidebar
TV_IMG_SIZE = (24, 24)  # treeview


class FileDialog(Dialog):
    def __init__(
        self,
        parent,
        command=None,
        confirmoverwrite=True,
        defaultextension="",
        filetypes=[],
        initialdir=None,
        initialfile=None,
        message="",
        multiple=False,
        title="",
        okbuttontext="Ok",
        cancelbuttontext="Cancel",
    ):
        super().__init__(parent=parent, title=title)
        self.initialdir = initialdir
        self.initialfile = initialfile
        self.multiple = multiple
        self.message = message
        self.filetypes = filetypes
        self.okbuttontext = okbuttontext
        self.cancelbuttontext = cancelbuttontext
        self.command = command
        self.confirmoverwrite = confirmoverwrite
        self.defaultextension = defaultextension
        self.images = self.load_dialog_images()

    def get_folder_contents(self, pathname):
        """Return a list of Path items"""
        ...

    def load_dialog_images(self):
        """Load all images that will be used in the dialog sidebar and
        treeview"""
        images = {}
        imgpath = (
            pathlib.Path(__file__).parent / "assets"
        )  # replace with importlib.resources
        for name, filename in IMAGES.items():
            size = TV_IMG_SIZE if name in ["File", "Dir"] else SB_IMG_SIZE
            img_ = Image.open(imgpath / filename).resize(size, Image.ANTIALIAS)
            images[name] = ImageTk.PhotoImage(img_)
        return images

    def load_treeview_items(self, pathname):
        ...

    def on_click_sidebar_button(self, event):
        ...

    def on_click_parent_dir(self, event):
        ...

    def on_click_treeview_dir(self, event):
        ...

    def create_body(self, master):
        container = ttk.Frame(master)
        
        sidebar = self.create_sidebar_menu(container)
        sidebar.pack(side=LEFT, fill=X, anchor=N)
        self.treeview = self.create_treeview(container)
        self.treeview.pack(side=RIGHT, fill=BOTH)
        
        container.pack(fill=X, expand=YES)

    def create_buttonbox(self, master):
        ...

    def create_treeview(self, master):
        tv = ttk.Treeview(master, show=TREEHEADINGS, columns=[0, 1, 2])
        tv.pack(fill=BOTH, expand=YES)
        tv.column("#0", width=500)
        tv.column(0, stretch=False)
        tv.column(1, stretch=False, width=125)  # TODO calculate size
        tv.column(2, stretch=False, width=125, anchor=E)  # TODO calculate size
        tv.heading("#0", text=MC.translate("Name"), anchor=W)
        tv.heading(0, text=MC.translate("Date modified"), anchor=W)
        tv.heading(1, text=MC.translate("Type"), anchor=W)
        tv.heading(2, text=MC.translate("Size"), anchor=E)

        # configure item tags
        tv.tag_configure("dir", image=self.images["File"])
        tv.tag_configure("file", image=self.images["Dir"])
        return tv

    def create_sidebar_menu(self, master):
        # TODO how are these translated in other langauges?
        frame = ttk.Frame(master, name="sidebar")
        folders = [
            "Desktop",
            "Documents",
            "Music",
            "Pictures",
            "Videos",
            "Downloads",
        ]
        if self._winsys == "x11":
            path = pathlib.Path.home().parent
            btn_ = ttk.Button(
                master=frame,
                text=path.name,
                image=self.images["Home"],
                compound=LEFT,
                bootstyle=LINK,
                command=lambda x=path: self.load_treeview_items(x),
            )
            btn_.pack(anchor=W)

            path = pathlib.Path.home()
            btn_ = ttk.Button(
                master=frame,
                text=path.name,
                image=self.images["User"],
                compound=LEFT,
                bootstyle=LINK,
                command=lambda x=path: self.load_treeview_items(x),
            )
            btn_.pack(anchor=W)
        else:
            path = pathlib.Path.home()
            btn_ = ttk.Button(
                master=frame,
                text=path.name,
                image=self.images["Home"],
                compound=LEFT,
                bootstyle=LINK,
                command=lambda x=path: self.load_treeview_items(x),
            )
            btn_.pack(anchor=W)

        home = pathlib.Path.home()
        for folder in folders:
            path = home / folder
            if path.exists():
                btn_ = ttk.Button(
                    master=frame,
                    text=path.name,
                    image=self.images[folder],
                    compound=LEFT,
                    bootstyle=LINK,
                    command=lambda x=path: self.load_treeview_items(x),
                )
                btn_.pack(anchor=W)

        return frame

    def update_breadcrumbs(self):
        ...


class FilePathItem:
    def __init__(self, path: pathlib.Path):
        self.path = path
        self.name = path.name
        self.uri = path.absolute()
        self.tag = ["file", "dir"][path.is_dir()]
        self.size: int = None
        self.type: str = None
        self.modified: str = None

    @property
    def values(self):
        return self.modified, self.type, self.size

    def item_stats(self):
        stats = self.path.stat()
        # file size & type
        if self.tag == "dir":
            self.size = ""
            self.type = "File Folder"
        else:
            self.size = f"{ceil(stats.st_size * 0.001):,d} KB"
            self.type = f"{self.path.suffix[1:].upper()} File".strip()
        # last modified
        timestamp = datetime.fromtimestamp(stats.st_mtime)
        self.modified = timestamp.strftime("%z")


if __name__ == "__main__":

    app = ttk.Window()

    fd = FileDialog(app)
    fd.show()

    app.mainloop()
