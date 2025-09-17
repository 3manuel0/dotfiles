# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration

# from qtile_extras import widget
# from qtile_extras.widget.decorations import PowerLineDecoration
import os
import subprocess
from subprocess import call
import random
from libqtile import hook

# breeze-icon-theme

mod = "mod4"
terminal = "alacritty"
home = os.path.expanduser("~")


# qtile.cmd_spawn("picom")
@lazy.function
def next_wallpaper(qtile):
    home = os.path.expanduser("~")
    qtile.cmd_spawn(f"alacritty -e python3 {home}/projects/project_wallpaper/next.py")


# arrow_powerlineLeft = {
#     "decorations": [
#         PowerLineDecoration(
#             path="arrow_left",
#             size=11,
#         )
#     ]
# }

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),  # Previous Track
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer -q sset Master 1%+"),
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer -q sset Master 1%-"),
    ),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key(
        [mod],
        "w",
        lazy.spawn(f"python3 {home}/projects/project_wallpaper/next.py"),
        desc="next Wallpaper",
    ),
    Key(
        [mod],
        "s",
        lazy.spawn(f"python3 {home}/projects/project_wallpaper/prev.py"),
        desc="previous Wallpaper",
    ),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    # screens[0].cmd_set_wallpaper('~/Downloads/wallhaven-yxdvjx.png', 'fill')
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "b", lazy.spawn("google-chrome"), desc="Launch browzer"),
    Key([mod], "e", lazy.spawn("dolphin"), desc="Launch browzer"),
    # Toggle between different layouts as defined below
    Key([mod, "shift"], "s", lazy.spawn("scrot -s"), desc="screenshot"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "a",
        lazy.spawn("rofi -show drun"),
        desc="Start Rofi menu for desktop apps",
    ),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="Start Rofi menu"),
]

# Add key bindings to switch VTs in Wayland.
# We can't check qtile.core.name in default config as it is loaded before qtile is started
# We therefore defer the check until the key binding is run by using .when(func=...)
for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = []
group_names = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
]
group_labels = [
    "一",
    "二",
    "三",
    "四",
    "五",
    "六",
    "七",
    "八",
    "九",
]

group_layouts = [
    "Matrix",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
    "monadtall",
]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        )
    )

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Move focused window to group {}".format(i.name),
            ),
        ]
    )


# groups = [Group(i) for i in ["一", "二", "三", "四", "五", "六", "七", "八", "九"]]
# group_hotkeys = "123456789"
# for g, k in zip(groups, group_hotkeys):
#     # print(g)
#     keys.extend(
#         [
#             # mod1 + group number = switch to group
#             Key(
#                 [mod],
#                 k,
#                 lazy.group[g.name].toscreen(),
#                 desc=f"Switch to group {g.name}",
#             ),
#             # mod1 + shift + group number = switch to & move focused window to group
#             Key(
#                 [mod, "shift"],
#                 k,
#                 lazy.window.togroup(g.name, switch_group=False),
#                 desc=f"Switch to & move focused window to group {g.name}",
#             ),
#             # Or, use below if you prefer not to switch to that group.
#             # # mod1 + shift + group number = move focused window to group
#             # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
#             #     desc="move focused window to group {}".format(i.name)),
#         ]
#     )

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    # layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=4),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(border_width=0, margin=4, border_focus="#7D0DC3"),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    layout.Matrix(border_width=0, margin=4, border_focus="#7D0DC3"),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="DejaVu Sans Mono Bold, Hack Nerd Font",
    fontsize=16,
    foreground="#cdd6f4",
)
extension_defaults = widget_defaults.copy()


def exBtop():
    qtile.cmd_spawn("alacritty -e btop")


def volumeDown():
    qtile.cmd_spawn("amixer -q sset Master 5%+")


def volumeUp():
    qtile.cmd_spawn("amixer -q sset Master 5%-")


def volumeMute():
    qtile.cmd_spawn("amixer -q sset Master toggle")


powerlineRight = {
    "decorations": [
        PowerLineDecoration(
            path="arrow_right",
        )
    ]
}
powerRoundRight = {
    "decorations": [
        PowerLineDecoration(
            path="rounded_right",
        )
    ]
}
powerRoundLeft = {
    "decorations": [
        PowerLineDecoration(
            path="rounded_left",
        )
    ]
}

powerlineLeft = {
    "decorations": [
        PowerLineDecoration(
            path="arrow_left",
        )
    ]
}
decoration_group = {
    "decorations": [RectDecoration(colour="#000000", radius=10, filled=True)],
    # "padding": 10,
}
length = 10
screens = [
    Screen(
        top=bar.Bar(
            [
                # widget.CurrentLayout(),
                widget.GroupBox(
                    fontsize=16,
                    font="Source Han Serif Jp Heavy",
                    # margin_y = 2,
                    margin_x=3,
                    # padding_y = 2,
                    padding_x=3,
                    borderwidth=0,
                    disable_drag=True,
                    inactive="#cdd6f4",
                    active="#cdd6f4",
                    rounded=False,
                    highlight_method="block",
                    background="#000000",
                    block_highlight_text_color="#000000",
                    this_current_screen_border="#ffffff",
                    **powerRoundLeft,
                ),
                # widget.Spacer(
                #     length=5,
                # ),
                widget.Prompt(),
                widget.WindowName(
                    font="monospace Bold",
                    foreground="#e8ecfa",
                    **powerlineLeft,
                ),
                # widget.Chord(
                #     chords_colors={
                #         "launch": ("#ff0000", "#ffffff"),
                #     },
                #     background="#121212",
                #     name_transform=lambda name: name.upper(),
                # ),
                # widget.TextBox("default config", name="default"),
                # widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Spacer(
                    length=20,
                    **powerRoundRight,
                ),
                # widget.CryptoTicker(
                #     format=" {crypto}:{amount:,.2f}$",
                #     crypto="BTC",
                #     fmt="<b >{}</b>",
                #     background="#ffffff",
                #     foreground="#000000",
                #     **powerRoundRight,
                # ),
                widget.CPU(
                    format="{load_percent}%",
                    fmt="<b> {}</b>",
                    mouse_callbacks={"Button1": exBtop},
                    background="#000000",
                ),
                widget.Spacer(
                    length=length,
                    background="#000000",
                ),
                widget.Memory(
                    measure_mem="M",
                    format="{MemUsed:.0f}M",
                    fmt="<b>  {}</b>",
                    markup=True,
                    background="#000000",
                ),
                widget.Spacer(
                    length=length,
                    background="#000000",
                ),
                widget.Clock(
                    format="%a%b%d %H:%M",
                    fmt="<b>󰸗 {}</b>",
                    background="#000000",
                ),
                widget.Spacer(
                    length=length,
                    background="#000000",
                ),
                widget.Volume(
                    emoji=False,
                    fmt="<b >  {}</b>",
                    mouse_callbacks={
                        "Button1": volumeDown,
                        "Button3": volumeUp,
                        "Button2": volumeMute,
                    },
                    background="#000000",
                ),
                widget.Spacer(
                    length=length,
                    background="#000000",
                    **powerRoundRight,
                ),
                widget.Systray(),
                widget.Notify(),
                # widget.Spacer(length=5, background="#8A9294"),
                # widget.QuickExit(),
            ],
            24,
            border_color="#222140",
            background="#1e1e2e",
            # border_width = [1,1,1,1],
            # margin = [5,20,0,20],
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # wallpaper="~/Downloads/wallhaven-yxdvjx.png",
        # wallpaper_mode="fill",
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        Match(wm_class="Tk"),
        Match(wm_class="gnome-calculator"),
        Match(wm_class="ghidra-Ghidra"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~")
    subprocess.call([home + "/.config/qtile/autostart.sh"])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.

wmname = "LG3D"
