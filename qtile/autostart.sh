#!/bin/bash
xset s off 
xset s noblank 
xset -dpms
amixer set Master 100%
xargs feh --bg-scal < ~/Wallpapers/current_wallpaper_path.txt 
/usr/bin/lxqt-policykit-agent &
nm-applet &
picom &
alacritty -e htop &
alacritty -e tty-clock -s &
alacritty -e cmatrix &
alacritty -e cava &
# discord &
# xwinwrap -g 1600x900+0+0 -ni -s -nf -b -un -ov -fdt -argb -- mpv --mute=yes --no-audio --no-osc --no-osd-bar --quiet --screen=0 --geometry=1600x900+0+0 -wid WID --loop ~/Downloads/c.mp4 &
# xwinwrap -ov -g 1600x900+0+0 -- mpv -wid WID ~/Downloads/c.mp4 --no-osc --no-osd-bar --loop-file --player-operation-mode=cplayer --no-audio --panscan=1.0 --no-input-default-bindings &
