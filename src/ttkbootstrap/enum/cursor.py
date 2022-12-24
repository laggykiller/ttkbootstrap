import enum


class CursorEnum(enum.Enum):
    """Cursors available on all platforms"""
    XCursor = 'X_cursor'
    Arrow = 'arrow',  # mapped to native curso
    BasedArrowDown = 'based_arrow_down'
    BasedArrowUp = 'based_arrow_up'
    Boat = 'boat'
    Bogosity = 'bogosity'
    BottomLeftCorner = 'bottom_left_corner'
    BottomRightCorner = 'bottom_right_corner'
    BottomSide = 'bottom_side'
    BottomTee = 'bottom_tee'
    BoxSpiral = 'box_spiral'
    CenterPtr = 'center_ptr'
    Circle = 'circle'
    Clock = 'clock'
    CoffeeMug = 'coffee_mug'
    Cross = 'cross'
    CrossReverse = 'cross_reverse'
    CrossHair = 'crosshair'
    DiamondCross = 'diamond_cross'
    Dot = 'dot'
    DotBox = 'dotbox'
    DoubleArrow = 'double_arrow'
    DraftLarge = 'draft_large'
    DraftSmall = 'draft_small'
    DrapedBox = 'draped_box'
    Exchange = 'exchange'
    Fleur = 'fleur'
    Gobbler = 'gobbler'
    Gumby = 'gumby'
    Hand1 = 'hand1'
    Hand2 = 'hand2'
    Heart = 'heart'
    IBeam = 'ibeam'
    Icon = 'icon'
    IronCross = 'iron_cross'
    LeftPtr = 'left_ptr'
    LeftSide = 'left_side'
    LeftTee = 'left_tee'
    LeftButton = 'leftbutton'
    LLAngle = 'll_angle'
    LLRAngle = 'lr_angle'
    Man = 'man'
    MiddleButton = 'middlebutton'
    Mouse = 'mouse'
    NONE = 'none'
    Pencil = 'pencil'
    Pirate = 'pirate'
    Plus = 'plus'
    QuestionArrow = 'question_arrow'
    RightPtr = 'right_ptr'
    RightSide = 'right_side'
    RightTee = 'right_tee'
    RightButton = 'rightbutton'
    RTLLogo = 'rtl_logo'
    SailBoat = 'sailboat'
    SbDownArrow = 'sb_down_arrow'
    SbHDoubleArrow = 'sb_h_double_arrow'
    SbLeftArrow = 'sb_left_arrow'
    SbRightArrow = 'sb_right_arrow'
    SbUpArrow = 'sb_up_arrow'
    SbVDoubleArrow = 'sb_v_double_arrow'
    Shuttle = 'shuttle'
    Sizing = 'sizing'
    Spider = 'spider'
    SprayCan = 'spraycan'
    Star = 'star'
    Target = 'target'
    TCross = 'tcross'
    TopLeftArrow = 'top_left_arrow'
    TopLeftCorner = 'top_left_corner'
    TopRightCorner = 'top_right_corner'
    TopSide = 'top_side'
    TopTee = 'top_tee'
    Trek = 'trek'
    UlAngle = 'ul_angle'
    Umbrella = 'umbrella'
    UrAngle = 'ur_angle'
    Watch = 'watch'
    XTerm = 'xterm'

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return other == self.value

    def __str__(self):
        return self.value


class WinCursorEnum(enum.Enum):
    """Cursors only available on the Windows platform"""
    No = 'no'
    Starting = 'starting'
    Size = 'size'
    SizeNeSw = 'size_ne_sw'
    SizeNs = 'size_ns'
    SizeNwSe = 'size_nw_se'
    SizeWe = 'size_we'
    UpArrow = 'uparrow'
    Wait = 'wait'

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return other == self.value

    def __str__(self):
        return self.value


class MacCursorEnum(enum.Enum):
    """Cursors available on Mac OS"""
    CopyArrow = 'copyarrow'
    AliasArrow = 'aliasarrow'
    ContextualMenuArrow = 'contextualmenuarrow'
    MoveArrow = 'movearrow'
    Text = 'text'
    CrossHair = 'cross - hair'
    Hand = 'hand'
    OpenHand = 'openhand'
    ClosedHand = 'closedhand'
    Fist = 'fist'
    PointingHand = 'pointinghand'
    Resize = 'resize'
    ResizeLeft = 'resizeleft'
    ResizeRight = 'resizeright'
    ResizeLeftRight = 'resizeleftright'
    ResizeUp = 'resizeup'
    ResizeDown = 'resizedown'
    ResizeUpDown = 'resizeupdown'
    ResizeBottomLeft = 'resizebottomleft'
    ResizeTopLeft = 'resizetopleft'
    ResizeBottomRight = 'resizebottomright'
    ResizeTopRight = 'resizetopright'
    NotAllowed = 'notallowed'
    Poof = 'poof'
    Wait = 'wait'
    CountingUpHand = 'countinguphand'
    CountingDownHand = 'countingdownhand'
    CountingUpAndDownHand = 'countingupanddownhand'
    Spinning = 'spinning'
    Help = 'help'
    Bucket = 'bucket'
    Cancel = 'cancel'
    EyeDrop = 'eyedrop'
    EyeDropFull = 'eyedrop - full'
    ZoomIn = 'zoom - in'
    ZoomOut = 'zoom - out'

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return other == self.value

    def __str__(self):
        return self.value
