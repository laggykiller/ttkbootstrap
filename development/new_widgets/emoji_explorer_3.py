"""
    MENU
    - reset
        * reset selectors
        * reset preview font size
        * DO NOT reset the selected font
    - export details
        * open saveas dialog
        * save details in text file

    TOP
    - search bar (entry)
        * reset category selector filters
        * search category, subcategory, and emoji name
        * update is called after every keystroke with validation function
    
    SELECTORS
    - categories filter (treeview)
        * multi selection enabled
        * filter subcategory list by tag name
        * filter emoji list by tag name
    - subcategories filter (treeview)
        * multi selection enabled
        * filter subcategory by tag name
        * filter emoji list by tag name
    - font family selector (combobox)
        * update preview font
        * update emoji selector font
    - emoji selector (treeview)
        * update emoji preview
        * update summary values
    
    EMOJI PREVIEW
    - preview window (label)
        * connected to preview font
    - preview scale (scale)
        * connected to preview font
        * update preview font size

    SUMMARY
    - name label / value (label)
        * value connected to emoji name variable
    - category label / value (label)
        * value connected to emoji category variable
    - subcategory label / value (label)
        * value connected to emoji subcategory variable
    - font family label value (label)
        * value connected to preview font family variable
    - emoji unicode label / value (label)
        * value connected to unicode variable
    - emoji point label / value (label)
        * value connected to emoji point variable

"""

import ttkbootstrap as ttk
from ttkbootstrap.icons import Emoji
from ttkbootstrap.constants import *
from tkinter import font


def run_program():
    """Runs the emoji explorer application"""
    app = ttk.Window(title="Emoji Explorer")

    # setup application variables and fonts
    _app_vars = setup_app_variables(app)
    _app_fonts = setup_app_fonts()

    # create application components
    create_menu(app)
    create_searchbar(app).pack()
    create_selectors(app).pack()
    create_preview(app).pack()

    app.mainloop()


def create_menu(master):
    """Create the application menu"""
    ...


def create_searchbar(master):
    """Create the emoji search bar"""
    container = ttk.Frame(master, bootstyle="info")
    searchbar = ttk.Entry(container, textvariable="search-text")
    searchbar.pack(fill=X, expand=YES)
    searchbar.bind(
        sequence="<KeyRelease>",
        func=lambda *_, w=searchbar: on_search_entry_keyrelease(w),
    )
    return container


def create_selectors(master):
    """Create the frame containing the emoji selectors and filters"""
    container = ttk.Frame(master)
    create_emoji_font_selector(container).pack()
    return container


def create_preview(master):
    """Create the frame containing the emoji preview and summary info"""
    container = ttk.Frame(master, bootstyle="success")
    return container


def create_emoji_font_selector(master):
    """Create the combobox for selecting the emoji font family"""
    families = master.getvar("font-families")
    combo = ttk.Combobox(values=families, textvariable="emoji-family")
    combo.set(families[0])
    return combo


def find_font_families():
    """Find and return a list of all font families, sorted by symbol
    and emoji families first, and then the remaining"""
    families = font.families()
    return families


def on_search_entry_keyrelease(widget):
    """Callback for when the user releases a key in the search entry box"""
    text = widget.getvar("search-text")
    print(text)


def trace_emoji_family(*_):
    """Callback for when the emoji-family variable is changed"""
    family = ttk.Variable(name="emoji-family").get()
    font.nametofont("preview-font")["family"] = family
    font.nametofont("emoji-font")["family"] = family


def setup_app_variables(master):
    """Sets the variable traces for font changes"""
    families = find_font_families()
    font_families = ttk.Variable(name="font-families", value=families)
    emoji_name = ttk.StringVar(name="emoji-name", value="")
    emoji_family = ttk.StringVar(name="emoji-family", value="")
    emoji_family.trace_add(
        mode="write", 
        callback=lambda *_, m=master: trace_emoji_family(m)
    )
    emoji_cat = ttk.StringVar(name="emoji-cat", value="")
    emoji_subcat = ttk.StringVar(name="emoji-subcat", value="")
    unicode = ttk.StringVar(name="unicode", value="")
    codepoint = ttk.StringVar(name="codepoint", value="")
    preview_font_size = ttk.StringVar(name="preview-font-size", value=60)
    search_text = ttk.StringVar(name="search-text", value="")
    # variables must be returned and assigned to variable to prevent
    # garbage collection
    return [
        font_families,
        emoji_name,
        emoji_family,
        emoji_cat,
        emoji_subcat,
        unicode,
        codepoint,
        preview_font_size,
        search_text,
    ]


def setup_app_fonts():
    """Create and return the named fonts to be used in the application"""
    return [
        font.Font(name="preview-font", size=60),
        font.Font(name="emoji-font", size=20),
    ]


if __name__ == "__main__":

    run_program()
