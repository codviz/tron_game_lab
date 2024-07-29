"""
========================================
  Introduction to Computer Programming
========================================

-------------------------------------------------
  support for grid graphics
  version 0.3 (2018-12-07)
  what's new:
      set_bgcolor
      larger MAX_COLUMNS, MAX_ROWS 
-------------------------------------------------
"""


from heapq import heappush, heappop
import time
import tkinter as Tk
import warnings


MIN_ROWS = 1
DEFAULT_ROWS = 40
MIN_COLUMNS = MIN_ROWS
DEFAULT_COLUMNS = 60
MIN_SCALE = 3
MAX_SCALE = 200
DEFAULT_SCALE = 10
MAX_ROWS = int(1000 / MIN_SCALE)
MAX_COLUMNS = MAX_ROWS

DEFAULT_BGCOLOR = 'black'
PAD = 3

FRAME_RATE = 60
FRAME_DELAY = 1000 // FRAME_RATE

assert MIN_ROWS <= DEFAULT_ROWS < MAX_ROWS
assert MIN_COLUMNS <= DEFAULT_COLUMNS < MAX_COLUMNS
assert MIN_SCALE <= DEFAULT_SCALE < MAX_SCALE

# -----------------------------------------------------------------


def open_window(columns=DEFAULT_COLUMNS,
                rows=DEFAULT_ROWS,
                scale=DEFAULT_SCALE,
                bgcolor=DEFAULT_BGCOLOR,
                show_cell_borders=False,
                title=''):
    """Constructs a window that represents a columns-by-rows grid of "cells"
    where each cell is a scale-by-scale pixels.  If show_cell_borders is
    set then cells will be visually separated by 1-pixel thick black
    borders. bgcolor is the background color for the graphics
    window. title is displayed at the top of the graphics window on its
    title bar.
    """
    global _g
    if _g is None:
        _g = _Graphics()
        _g.root = Tk.Tk()

        _g.rows = rows
        _g.columns = columns
        _g.scale = scale

        if _g.rows >= MAX_ROWS or _g.rows < MIN_ROWS:
            _g.rows = DEFAULT_ROWS
            warnings.warn('rows out of range, using default')
        if _g.columns >= MAX_COLUMNS or _g.columns < MIN_COLUMNS:
            _g.columns = DEFAULT_COLUMNS
            warnings.warn('columns out of range, using default')
        if _g.scale < MIN_SCALE:
            _g.scale = DEFAULT_SCALE
            warnings.warn('scale out of range, using default')
        width = _g.scale * _g.columns
        if _g.root.winfo_screenwidth() <= width:
            _g.scale = _g.root.winfo_screenwidth() // _g.columns
            width = _g.scale * _g.columns
            warnings.warn('scale too large for width, adjusting')
        height = _g.scale * _g.rows
        if _g.root.winfo_screenheight() <= height:
            _g.scale = _g.root.winfo_screenheight() // _g.rows
            height = _g.scale * _g.rows
            warnings.warn('scale too large for height, adjusting')

        if show_cell_borders:
            _g.border = 1
        else:
            _g.border = 0

        _g.d = {}          # pos->color state  (the "board")
        _g.r = {}          # pos->id already drawn rectangles
        _g.to_remove = {}  # pos->id to remove upon update
        _g.to_draw = {}    # pos->color to create as new rectangles

        _g.events = Pq()
        _g.click_handler = None
        _g.release_handler = None
        _g.uses_key_press = False

        _g.bgcolor = bgcolor
        _g.root.title(title)
        _g.root.wm_protocol('WM_DELETE_WINDOW', close_window)
        frame = Tk.Frame(_g.root)
        frame.pack()
        _g.canvas = Tk.Canvas(frame,
                              width=width + PAD,
                              height=height + PAD,
                              bg=_g.bgcolor)
        _g.canvas.pack()
        _g.root.update()

    else:
        warnings.warn('window already open')


def paint(p, color):
    """Paints cell at position p (a column-row pair) to be specified color.
    """
    _verify()
    if color == _g.bgcolor:
        unpaint(p)
    else:
        # if already painted, schedule removal
        id = _g.r.get(p)
        if id:
            _g.to_remove[p] = id
        _g.d[p] = color
        _g.to_draw[p] = color   # will replace if already scheduled for drawing


def unpaint(p):
    """Clears cell at position p (a column-row pair) - equivalent to painting
    cell with background color.
    """
    _verify()
    if p in _g.d:   # only act if p currently non empty on board
        # if already painted, schedule removal
        id = _g.r.get(p)
        if id:
            _g.to_remove[p] = id
        # if scheduled to be drawn, remove
        if p in _g.to_draw:
            del _g.to_draw[p]
        del _g.d[p]


def update():
    """Forces underlying graphics system to make recent changes (paints,
    unpaints) visible now.
    """

    _verify()

    # after this is called, draw/removal queues are empty,
    # and .r and .d should be in sync

    # remove scheduled removals
    for p, id in _g.to_remove.items():
        _g.canvas.delete(id)
        del _g.r[p]
    _g.to_remove.clear()
    # create new rectangles
    for p, color in _g.to_draw.items():
        l = p[0] * _g.scale + PAD
        t = p[1] * _g.scale + PAD
        r = l + _g.scale
        b = t + _g.scale
        _g.r[p] = _g.canvas.create_rectangle(l, t, r, b, fill=color,
                                             width=_g.border)
    _g.to_draw.clear()
    _g.root.update()


def clear():
    """Clears graphics window. (All cells reset to background color.)"""
    _verify()
    _g.d.clear()
    _g.r.clear()
    _g.to_remove.clear()
    _g.to_draw.clear()
    _g.canvas.delete('all')
    _g.root.update()


def close_window():
    """Closes graphics window."""
    _verify()
    global _g
    _g.root.quit()
    _g.root.destroy()
    _g = None


def get_dimensions():
    """Return dimensions of opened graphics windows columns by rows."""
    _verify()
    return (_g.columns, _g.rows)


def set_bgcolor(color):
    _verify()
    _g.bgcolor = color
    _g.canvas.config(bg=_g.bgcolor)
    update()


def set_click_handler(handler):
    """Tell graphics systems to call function handler when mouse clicks
    made upon graphics window. handler assumed to be a function that takes
    as input a single coordinate pair (a two-element tuple) such that the
    first value in the pair corresponds to the column and the second to the
    row that has been clicked.
    """
    _verify()
    _g.click_handler = handler


def set_key_handler(handler):
    """Tell graphics systems to call function handler when a key has been
    pressed (and released) while the graphics window has the "focus."
    handler assumed to be a function that takes as input a string
    corresponding the key that has been pressed (and released).
    """
    _verify()
    _g.release_handler = handler


def set_timer(action, delay):
    """Tell graphics systems to call function action at delay miliseconds in
    the future. action assumed to be a function that takes no arguments.
    """
    _verify()
    _g.events.push(_TimeEvent(action, delay))


def event_loop():
    """Enter event-handling loop."""
    _verify()
    _g.canvas.bind('<Button>', _click_handler)
    _g.canvas.bind('<KeyRelease>', _release_handler)
    _g.canvas.focus_force()   # listen for key events
    _g.canvas.after_idle(_event_loop)
    _g.root.mainloop()


# -----------------------------------------------------------------


def _event_loop():
    if _g:
        if not _g.events.is_empty():
            e = _g.events.peek()
            if e.times_up():
                _g.events.pop()
                e.action()
        if _g:
            update()
        if _g:
            _g.canvas.after(FRAME_DELAY, _event_loop)


# -----------------------------------------------------------------

class _Event:
    def __init__(self, f):
        self.action = f
        self.t = time.time()

    def times_up(self):
        return True

    def __lt__(self, other):
        return self.t < other.t


class _TimeEvent(_Event):
    def __init__(self, f, delay=0):
        super().__init__(f)
        self.t += (delay / 1000.0)

    def times_up(self):
        return self.t < time.time()


def _click_handler(e):
    if _g.click_handler:
        col = e.x // _g.scale
        row = e.y // _g.scale
        _g.events.push(_Event(lambda: _g.click_handler((col, row))))


def _release_handler(e):
    if _g.release_handler:
        _g.events.push(_Event(lambda: _g.release_handler(e.keysym)))


# -----------------------------------------------------------------


class EmptyPriorityQueue(LookupError):
    pass


class Pq:
    def __init__(self):
        self.pq = []

    def push(self, rev_it):
        heappush(self.pq, rev_it)

    def pop(self):
        if len(self.pq) > 0:
            return heappop(self.pq)
        else:
            raise EmptyPriorityQueue

    def peek(self):
        if len(self.pq) > 0:
            return self.pq[0]
        else:
            raise EmptyPriorityQueue

    def is_empty(self):
        return len(self.pq) == 0


# -----------------------------------------------------------------


class GraphicsException(Exception):
    pass


def _verify():
    if _g and _g.root:
        pass
    else:
        raise GraphicsException


class _Graphics:
    pass


_g = None
