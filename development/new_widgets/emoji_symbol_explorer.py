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

        self.list_cat = set()
        self.set_subcat = set()

        self.symbol_font = font.Font(size=20)
        self.preview_font = font.Font(size=60)

        # setup
        self.font_family = self.setup_fontfamily_combobox(self.master)
        self.font_family.pack(fill=X, expand=YES, padx=10)

        frame = ttk.Frame(self.master)
        frame.pack(fill=BOTH, expand=YES)
        self.sym_list = self.setup_symbol_list(frame)
        self.cat_list = self.setup_categories_list(frame)
        self.subcat_list = self.setup_subcategories_list(frame)
        self.cat_list.pack(side=LEFT, fill=BOTH, expand=YES, padx=10, pady=10)
        self.subcat_list.pack(side=LEFT, fill=BOTH, expand=YES, pady=10)
        self.sym_list.pack(side=LEFT, fill=BOTH, pady=10, padx=10)

        # variable traces
        self.family_var.trace_add("write", self._update_treeview_font)

    def setup_categories_list(self, master):
        """Create category treeview"""

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

        self.symbol_font["family"] = families[0]
        self.master.style.configure(
            "symbol.Treeview",
            rowheight=self.symbol_font.metrics()["linespace"],
        )

        return combo

    def setup_symbol_list(self, master):
        """Create the symbol treeview"""
        tv = ttk.Treeview(master, columns=[0], show="")
        tv.tag_configure("row", font=self.symbol_font)
        tv.configure(style="symbol.Treeview")
        width = self.symbol_font.measure("🪢") + 10
        tv.column(0, anchor=CENTER, stretch=False, width=width)

        g = groupby(Emoji.iter(), lambda x: (x.category, x.subcategory))
        for (category, subcategory), items in g:
            self.list_cat.add(category)
            self.set_subcat.add((category, subcategory))
            for i in items:
                tv.insert(
                    parent="",
                    index=END,
                    values=[i.char],
                    tags=["emoji-font", "row", category, subcategory],
                )
        return tv

    def setup_categories_list(self, master):
        """Create the category treeview"""
        tv = ttk.Treeview(master, bootstyle=DARK)
        tv.heading("#0", text="Category", anchor=W)
        tv.tag_configure("row", font=self.symbol_font)

        for cat in self.list_cat:
            tv.insert(
                parent="",
                index=END,
                text=cat,
                tags=[cat],
            )
        return tv

    def setup_subcategories_list(self, master):
        """Create the subcategory treeview"""
        tv = ttk.Treeview(master, bootstyle=DARK)
        tv.heading("#0", text="Subcategory", anchor=W)
        tv.tag_configure("row", font=self.symbol_font)

        for cat, sub in self.set_subcat:
            print(sub)
            tv.insert(
                parent="",
                index=END,
                text=sub,
                tags=[cat, sub],
            )
        return tv

    def _update_treeview_font(self, *_):
        self.symbol_font["family"] = self.family_var.get()
        self.preview_font["family"] = self.family_var.get()
        self.master.style.configure("symbol.Treeview")


if __name__ == "__main__":

    from itertools import groupby

    app = ttk.Window()

    e = Explorer(app)

    app.mainloop()
