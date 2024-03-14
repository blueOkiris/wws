## Windows Workspace Switcher

## Description

A set of 9 status tray icons for clicking between virtual desktops and knowing which you're on.

Windows has virtual desktops, but I want to use them like i3 or a Linux DE where I can see which workspace I'm in and click between them. Useful in conjunction with FancyWM

![img](./img/screenshot.png)

You can click on them to select a workspace, it automatically sets workspaces to 9, and when you move desktops whether by clicking or with the keyboard or with some other way, they update to show the correct current desktop.

Why 9? On many tiling WMs like i3 or Hyprland, there is a workspace corresponding to each number key. Indeed this is how FancyWM is set up to work. However, while the Linux ones go 1-10 with 0 being 10, FancyWM only goes 1-9, so I draw 9, bc I intend this to work with FancyWM.

## Run

Requirements:

- Python 3 (I use Microsoft Store version)

Download repo and place somewhere like `C:\wws` or on your Desktop or in Program Files.

To launch manually, go to the folder and double click `start.vbs`. This will silently call `run.bat` which will (the first time) set up a local Python virtual environment with all dependencies and then launch the program in the background.

To launch automatically at startup, create a shortcut to `start.vbs` and place it in the "Startup" folder in Explorer (`C:\Users\<your-name>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`).

To kill, right click an indicator and click "Exit"

