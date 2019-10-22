import curses

########
# MAIN #
########
def _main_():
    try:
        screen = _init()
        animation_loop(screen)
    except BaseException as bug_report:
        _quit(screen)
        print(bug_report)

#############
# FUNCTIONS #
#############
def _init():
    screen = curses.initscr()  # New screen initialization
    curses.start_color()       # Allow to use colors
    curses.cbreak()            # Will react directly to the key
    screen.keypad(True)
    curses.noecho()            # No display of keyboard
    curses.curs_set(0)         # Set the cursor unvisible
    return screen

def _quit(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()

def animation_loop(screen):
    while True:
        set_environment(screen)
        screen.timeout(1000)
        c = screen.getch()
        if c == ord('q'):
            _quit(screen)
            break
        else:
            screen.addstr(0, 0, "BOOM")
            screen.refresh()

def set_environment(screen):
    screen.addstr(5, 0, "~~~~~~~~~~~~~~")

##########
# LAUNCH #
##########
_main_()