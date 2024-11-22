import os


def next_wallpaper():
    path = "/home/l3manuel/Wallpapers/"
    current_wallpaper_index_file = "current_wallpaper_index.txt"
    current_wallpaper_path = "current_wallpaper_path.txt"
    feh_command = "feh --bg-scal "
    current_index = 0
    wallpapers_list = [
        f for f in os.listdir(path=path) if f.lower().endswith((".png", ".jpg"))
    ]
    try:
        with open(path + current_wallpaper_index_file, "r") as f:
            current_index = int(f.read())
    except:
        with open(path + current_wallpaper_index_file, "w") as f:
            f.write("0")
    if current_index >= len(wallpapers_list) - 1:
        current_index = 0
    else:
        current_index += 1

    with open(path + current_wallpaper_index_file, "w") as f:
        f.write(str(current_index))
    os.system(feh_command + path + wallpapers_list[current_index])
    with open(path + current_wallpaper_path, "w") as f:
        f.write(path + wallpapers_list[current_index])


next_wallpaper()
