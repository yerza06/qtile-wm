# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
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

import datetime
from os import path
from subprocess import Popen, check_output, run
from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from my_widget import MyCustomWidget as MCW




mod = "mod4"
terminal = guess_terminal()
home = path.expanduser("~")
qconf = home + "/.config/qtile/"
autostart = qconf + "autostart.sh"


@hook.subscribe.startup_once
def autostart():
    Popen(["bash", autostart])   


keys = [
    Key([mod], "Backspace", lazy.reload_config()),

    Key([mod], "f", lazy.spawn("firefox")),
    Key([mod], "t", lazy.spawn("telegram-desktop")),
    Key([mod], "e", lazy.spawn("nemo")),
    Key([mod], "d", lazy.spawn("discord")),
    Key([mod], "s", lazy.spawn("spotify-launcher")),
    Key([mod], "o", lazy.spawn("obsidian")),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui")),

    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +2%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 2%-")),

    Key([], "XF86KbdBrightnessUp", lazy.spawn("brightnessctl -d asus::kbd_backlight set +25%")),
    Key([], "XF86KbdBrightnessDown", lazy.spawn("brightnessctl -d asus::kbd_backlight set 25%-")),

    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -2%")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +2%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    Key([], "XF86Launch1", lazy.spawn("playerctl play-pause")),
    Key([], "XF86Launch3", lazy.spawn("playerctl previous")),
    Key([], "XF86Launch4", lazy.spawn("playerctl next")),

    Key([mod], "space", lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),
    
    Key([], "XF86TouchpadToggle", lazy.spawn("kitty start-server.sh")),
    #Key(["mod", "shift"], "v", lazy.spawn("clipmenu")),

    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    #Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
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
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod, "shift"],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod, "shift"], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
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


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(
        border_focus_stack=["##e74c3c", "##b03a2e"], 
        border_width=5,
        margin = 10
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]


# Screen Widgets
line = "┇"
line = "|"
line_color = "#939393"
color_in = "#F65B5BFF"

# background = "#151515"
# foreground = "#fff1f3"
# color1 = "#2c2525"
# color2 = "#fd6883"
# color3 = "#adda78"
# color4 = "#f9cc6c"
# color5 = "#2870ff"
# color6 = "#a8a9eb"
# color7 = "#85dacc"
# color8 = "#fff1f3"

widget_defaults = dict(
    font="JetBrainsMonoNerdFont",
    fontsize=20,
    padding=5,
)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.TextBox(format="|"),
                #widget.TextBox("default config", name="default"),
                #widget.TextBox("Press &lt;M-r&gt; to spawn", foreground="#d75f5f"),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                #widget.StatusNotifier(),

                widget.TextBox(" ", foreground=color_in),
                widget.Backlight(
                    backlight_name="intel_backlight",  # Замените на имя устройства подсветки
                    format="{percent:2.0%}",       # Иконка + процент
                    #change_command="brightnessctl set {0}%",
                    fmt="{}",
                ),
                widget.TextBox(line, foreground=line_color),
                widget.TextBox("󰕾", foreground=color_in),
                widget.Volume(fmt="{}"),
                widget.TextBox(line, foreground=line_color),
                widget.TextBox("󰌌", foreground=color_in),
                widget.KeyboardLayout(configured_keyboards=['us', 'ru', 'kz'], fmt="{}"),
                widget.TextBox(line, foreground=line_color),
                # widget.Memory(format="{MemPercent}%",fmt="<b>RAM </b> {}"),
                # widget.TextBox(line, foreground=line_color),
                # widget.CPU(format="{load_percent}%", fmt="<b>CPU</b> {}"),
                # widget.TextBox(line, foreground=line_color),
                widget.TextBox(" ", foreground=color_in),
                widget.Countdown(date=datetime.datetime(2024, 12, 31)),
                widget.TextBox(line, foreground=line_color),
                # widget.TextBox(line, foreground=line_color),
                #widget.Systray(),
                #widget.Battery(
                #    format="{char} {percent:2.0%}",
                #    charge_char="↑",  # Символ для зарядки
                #    discharge_char="↓",  # Символ для разрядки
                #    empty_char="✗",  # Символ для пустой батареи
                #    full_char="⚡",  # Символ для полной зарядки
                #    update_interval=30,  # Интервал обновления в секундах
                #),
                widget.TextBox("󰃮", foreground=color_in),
                widget.Clock(format="%Y-%m-%d", fmt="<b>{}</b>"),
                widget.TextBox(line, foreground=line_color),
                widget.TextBox("󰥔", foreground=color_in),
                widget.Clock(format="%H:%M:%S", fmt="<b>{}</b>"),
                # widget.TextBox(line, foreground=line_color),
                # widget.QuickExit(fmt="<b>{}</b>  ", default_text="  "),
                # widget.Wallpaper(),
            ],
            28,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
        bottom=bar.Bar(
            [
                # widget.TextBox(
                #     "", 
                #     foreground="#26A5E4", 
                #     mouse_callbacks={"Button1": lazy.spawn("telegram-desktop")}
                # ),
                # widget.TextBox(line, foreground=line_color),
                widget.TextBox("<b>MEM</b>", foreground=color_in),
                widget.Memory(format="{MemPercent}%",fmt="{}"),
                widget.TextBox(line, foreground=line_color),
                widget.TextBox("<b>CPU</b>", foreground=color_in),
                widget.CPU(format="{load_percent}%", fmt="{}"),
                widget.TextBox(line, foreground=line_color),
                widget.TextBox("<b>GPU</b>", foreground=color_in),
                widget.NvidiaSensors(threshold=60, foreground_alert='ff6000', fmt="{}"),
                widget.TextBox(line, foreground=line_color),
                widget.TextBox("<b> </b>", foreground=color_in),
                widget.Wlan(fmt="{}", use_ethernet=True, mouse_callbacks={"Button1": lazy.spawn("kitty nmtui")}),
                widget.TextBox(line, foreground=line_color),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.TextBox(" ", foreground=color_in),
                widget.TextBox(f"{MCW.get_wifi_ip()}", mouse_callbacks={"Button1": lazy.spawn("kitty nmtui")}),
                # widget.TextBox(line, foreground=line_color),
                # widget.TextBox(f"󰲝 ", foreground=color_in),
                # widget.TextBox(f"{MCW.get_external_ip()}"),
                widget.TextBox(line, foreground=line_color),
                #widget.TextBox(f" ", foreground=color_in),
                # widget.Clipboard(fmt="[ {} ]", max_chars=20, scroll_step=3),
                #widget.GenPollCommand(
                #    name="clipboard",
                #    fmt="Clipboard: {}",
                #    update_interval=2,  # Обновление каждые 2 секунды
                #    command="clipmenu -p '' | tail -n 1",
                #),
                widget.TextBox(" ", foreground=color_in),
                widget.Pomodoro(),

                widget.TextBox(line, foreground=line_color),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("alacritty")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("firefox")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("flatpak run org.torproject.torbrowser-launcher")}),
                widget.TextBox("󰖂 ", mouse_callbacks={"Button1": lazy.spawn("flatpak run com.protonvpn.www")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("telegram-desktop")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("discord")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("obsidian")}),
                widget.TextBox("󰏆 ", mouse_callbacks={"Button1": lazy.spawn("libreoffice")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("code")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("arduino-ide"), "Button3": lazy.spawn("flatpak run org.thonny.Thonny"), "Button2": lazy.spawn("flatpak run org.fritzing.Fritzing")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("flatpak run com.axosoft.GitKraken")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("flatpak run com.warlordsoftwares.youtube-downloader-4ktube")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("spotify-launcher"), "Button3": lazy.spawn("flatpak run app.moosync.moosync")}),
                widget.TextBox(" ", mouse_callbacks={"Button1": lazy.spawn("steam")}),
                widget.TextBox("󰍳 ", mouse_callbacks={"Button1": lazy.spawn("xmcl-0.47.15-x86_64.AppImage"), "Button2": lazy.spawn("minecraft-launcher")}),

            ],
            28,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
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
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "yerza06"