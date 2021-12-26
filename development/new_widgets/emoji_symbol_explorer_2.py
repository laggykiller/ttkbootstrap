import ttkbootstrap as ttk
from ttkbootstrap.icons import Emoji
from ttkbootstrap.constants import *
from tkinter import font

"""
    
    OVERVIEW:
    This application is a gui explorer for unicode emojis and symbols.
    -------------------------------------------------------------
    |                                                           |
    -------------------------------------------------------------
    -----------------------     ---------------------------------
    |                   |v|     |                               |
    -----------------------     |                               |     
    -----------------------     |                               |
    |                     |     |                               |
    |                     |     |                               |
    |                     |     |                               |
    |                     |     ---------------------------------
    |                     |     ------------------O--------------
    |                     |     Name:   
    |                     |     Category:
    |                     |     Family:
    |                     |     Unicode:
    |                     |     Point:
    |                     |     ---------------------------------
    |                     |     |  Export details               |
    -----------------------     ---------------------------------

    DEVELOPMENT NOTES:
    [ ] the combobox should have a list of all available fonts with the 
        'symbol' and 'emoji' named fonts at the top of the list.
    [x] The treeview should contain the list of emojis grouped by
        category [+]
    [ ] The treeview column containing the emoji should be updated
        with the font selected in the combobox.
    [ ] When an emoji is selected, the preview on the right should be
        updated as well as the summary information below that.
    [ ] When a font is selected, the emoji font will be updated as well
        as the 'family' option in the summary area.
    [ ] Adjusting the scale widget will increase or decrease the font
        size of the preview emoji. Default size will be large enough
        to fill up the diplay, but can go back down to 10 or 12 and up
        to about 64 or so
    [ ] Click the 'export details' button will export the summary
        information to a text file.
    [ ] searchbar at the top will filter the treeview
    [ ] if text is entered into the search bar, then all items are automatically
        shown with a tag-configure.

    ISSUES:
    [ ] The font must apply to the entire row, so that means the text
        will be unreadable with some fonts such as Symbol. One idea is to use
        checkboxes to filter the data with tags. Another idea is to use listboxes
        and have multi-selection turned on. This might be more economical.
        - When a category checkbox or range in a list is selected, the category 
            The treeview is filtered by that list, configuring the tags for that
            item, which correspond to the filter.
"""


class Explorer:
    def __init__(self, master):
        self.master = master
        self.name_var = ttk.StringVar()
        self.category_var = ttk.StringVar()
        self.family_var = ttk.StringVar()
        self.size_var = ttk.IntVar()
        self.unicode_var = ttk.StringVar()
        self.point_var = ttk.StringVar()

        # setup
        self.font_family = self.setup_fontfamily_combobox(self.master)
        self.font_family.pack(fill=X, expand=YES, padx=10)

        self.symbol_treeview = self.setup_symbol_treeview(self.master)
        self.symbol_treeview.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # variable traces
        self.family_var.trace_add("write", self._update_treeview_font)

    def setup_fontfamily_combobox(self, master):
        """Create the font family combobox"""
        families = []
        priority = []

        for f in font.families():
            if f and not f.startswith("@"):
                if any(["symbol" in f.lower(), "emoji" in f.lower()]):
                    priority.append(f)
                else:
                    families.append(f)

        self._families = [*sorted(priority), *sorted(families)]
        combo = ttk.Combobox(
            master, values=self._families, textvariable=self.family_var
        )
        combo.current(0)
        return combo

    def setup_symbol_treeview(self, master):
        """Create the symbol treeview"""
        tv = ttk.Treeview(master, columns=[0], bootstyle=DARK)
        tv.heading("#0", text="Category", anchor=W)
        tv.heading(0, text="Value")
        tv.column("#0", width=250, stretch=True)
        tv.column(0, anchor=CENTER, stretch=False, minwidth=50)

        g = groupby(Emoji.iter(), lambda x: (x.category, x.subcategory))
        for (category, subcategory), items in g:
            try:
                tv.insert(
                    parent="",
                    index="end",
                    iid=category,
                    text=category.lower(),
                    tags=["emoji-category", "row"],
                )
            except:
                pass
            try:
                tv.insert(
                    parent=category,
                    index="end",
                    iid=subcategory,
                    text=subcategory.lower(),
                    tags=["emoji-subcategory", "row"],
                )
            except:
                pass
            for i in items:
                tv.insert(
                    parent=subcategory,
                    index="end",
                    text=i.name.lower(),
                    values=[i.char],
                    tags=["emoji-font", "row"],
                )
        tv.tag_configure("row", font="Symbola 10")
        tv.tag_configure(
            "emoji-subcategory",
            background=app.style.colors.primary,
            foreground=app.style.colors.light,
        )
        return tv

    def _update_treeview_font(self, *_):
        family = self.family_var.get()
        self.symbol_treeview.tag_configure("row", font=(family, 10))


if __name__ == "__main__":

    from itertools import groupby

    def setup_symbol_treeview(master):
        """Create the symbol treeview"""
        tv = ttk.Treeview(master, columns=[0], show=HEADINGS)
        tv.column(0, anchor=CENTER, stretch=False, width=100)
        rowfont = font.Font(family="Segoe UI Emoji", size=20)
        tv.tag_configure("row", font=rowfont)

        g = groupby(Emoji.iter(), lambda x: (x.category, x.subcategory))
        for (category, subcategory), items in g:
            for i in items:
                tv.insert(
                    parent="",
                    index=END,
                    values=[i.char],
                    tags=["emoji-font", "row", category, subcategory],
                )
        return tv

    def setup_fontfamily_combobox(master):
        """Create the font family combobox"""
        families = []
        priority = []

        for f in font.families():
            if f and not f.startswith("@"):
                if any(["symbol" in f.lower(), "emoji" in f.lower()]):
                    priority.append(f)
                else:
                    families.append(f)

        _families = [*sorted(priority), *sorted(families)]
        combo = ttk.Combobox(master, values=_families)
        combo.current(0)
        return combo

    app = ttk.Window(themename="darkly")
    app.style.configure("symbol.Treeview", rowheight=60)
    setup_fontfamily_combobox(app).pack(fill=X, padx=10, pady=10)
    tv = setup_symbol_treeview(app)
    tv.configure(style="symbol.Treeview")
    tv.pack(fill=X, padx=10)
    app.mainloop()
