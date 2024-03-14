# Spawn 10 systray icons which can be used to show active/inactive workspaces and switch to them

from PIL import Image
from pystray import Icon, Menu, MenuItem
import pyvda
from pyvda import VirtualDesktop
from threading import Thread
import time

# ---------- Icon Stuff ----------

def on_change_desktop_clicked(icon, item):
    VirtualDesktop(number = int(icon.name)).go()

def on_exit_clicked(icon, item):
    global SHOULD_CLOSE

    SHOULD_CLOSE = True

def icon_create(i, img_desel):
    VirtualDesktop(number = i + 1).rename(f'Desktop {i + 1}')
    icon = Icon(
        str(i + 1),
        icon = img_desel,
        menu = Menu(
            MenuItem('ChangeDesktop', on_change_desktop_clicked, default = True),
            MenuItem('Exit', on_exit_clicked)
        )
    )
    return icon

def icon_run(icon):
    icon.run(on_change_desktop_clicked)

# ---------- Desktop Stuff ----------

def desktops_get_all():
    return [ (vd.number - 1, vd) for vd in pyvda.get_virtual_desktops() ]

def desktops_remove_extra(desktops):
    if len(desktops) > 10:
        print('Warning: WWS only works with exactly 10 desktops, but you have more. Closing extra')
        for i in range(len(desktops) - 10):
            print(f'> Closing desktop {i + 10}...')
            for (n, vd) in filter(lambda desktop: desktop[0] == i + 10, desktops):
                vd.remove()
    return list(filter(lambda desktop: desktop[0] < 10, desktops))

def desktops_make_enough(desktops):
    new_desktops = desktops.copy()
    if len(desktops) < 10:
        print('Warning: WWS only works with exactly 10 desktops, and you have too few. Creating')
        old_len = len(desktops)
        for i in range(10 - old_len):
            print(f'> Creating desktop {i + old_len}')
            new_desktops.append(VirtualDesktop.create())
    return new_desktops

# ---------- Main ----------

SHOULD_CLOSE = False
STARTUP_DELAY = 1.0

def load_images():
    sel_imgs = []
    desel_imgs = []
    for i in range(10):
        with Image.open(f'img/sel/{i}.png') as sel_img, \
                Image.open(f'img/desel/{i}.png') as desel_img:
            sel_imgs.append(sel_img.copy())
            desel_imgs.append(desel_img.copy())
    sel_imgs.append(sel_imgs[0])
    sel_imgs.pop(0)
    desel_imgs.append(desel_imgs[0])
    desel_imgs.pop(0)
    return (sel_imgs, desel_imgs)

def main():
    global SHOULD_CLOSE
    global STARTUP_DELAY

    (sel_imgs, desel_imgs) = load_images()
    
    desktops = desktops_get_all()
    desktops = desktops_remove_extra(desktops)
    desktops = desktops_make_enough(desktops)

    icons = [ icon_create(i, desel_imgs[i]) for i in range(10) ]
    threads = []
    for i in [ 0, 9, 8, 7, 6, 5, 4, 3, 2, 1 ]: # They don't show up in the correct order otherwise
        thread = Thread(target = icons[i].run)
        threads.append(thread)
        thread.start()
        time.sleep(STARTUP_DELAY) # Also needed for delay

    last_cur_num = -1
    while not SHOULD_CLOSE:
        cur_num = VirtualDesktop.current().number
        if last_cur_num != cur_num:
            for icon in icons:
                if icon.name == str(cur_num):
                    icon.icon = sel_imgs[cur_num - 1]
                else:
                    icon.icon = desel_imgs[int(icon.name) - 1]
            last_cur_num = cur_num
        time.sleep(0.01)

    for icon in icons:
        icon.stop()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()

