# Terminal-bg

Python script that turns your terminal into a transparent, live desktop background using GTK, VTE, and GtkLayerShell, giving you the ability to run terminal animations as wallpaper.


## Preview
### cava
  ![terminal-bg running cava](terminal-bg-cava.gif)

### lavat
![terminal-bg running lavat](terminal-bg-lavat.gif)

## Disclaimer

I’m just a junior developer who loves Linux. This project was built with help from ChatGPT—apologies if anything is broken or doesn’t work correctly. Use at your own risk!

---

## Features

- **Transparent terminal background**: Run any CLI program as your live wallpaper.  
- **Configurable appearance**: Adjust opacity and RGBA background color via a simple config file.  
- **Automatic config creation**: First launch auto-generates `~/.config/terminal-bg/terminal-bg.conf` with sane defaults.  
- **Custom script & monitor support**: Override the default command and target monitor at runtime.  
- **Lightweight & responsive**: Built on GTK3 + VTE with GtkLayerShell for smooth, accurate layering.  
- **Multi‑monitor friendly**: Choose which display to use for your animated background.

---

## Requirements

- **Python 3.6+**  
- **Python GObject Introspection** bindings for:
  - GTK3 (`python3-gi`, `gir1.2-gtk-3.0`)  
  - VTE (`gir1.2-vte-2.91`)  
  - GtkLayerShell (`gir1.2-gtk-layer-shell-0.1`)  
- A compositing window manager or desktop environment that supports true transparency.  


## Installation

The recommended way to install **terminal‑bg** is using `pipx`. This makes the `terminal-bg` command available globally while keeping its dependencies isolated in its own virtual environment.

### Using `pipx` (Recommended)

`pipx` installs Python CLI applications into isolated environments and makes them globally available without polluting your system Python or requiring you to manually activate a virtualenv.

#### Install `pipx` (if you haven’t already)

The best way to install `pipx` on Linux is via your distribution’s package manager:

- **Ubuntu / Debian**  
  ```bash
  sudo apt update
  sudo apt install pipx
  pipx ensurepath
  sudo pipx ensurepath --global    # optional, enables `--global` flag

- **Fedora**  
  ```bash
    sudo dnf install pipx
    pipx ensurepath
    sudo pipx ensurepath --global    # optional

- **Arch Linux**  
  ```bash
    sudo pacman -S python-pipx
    pipx ensurepath
    sudo pipx ensurepath --global    # optional

- **Other distros (via pip)**  
  ```bash
    python3 -m pip install --user pipx
    python3 -m pipx ensurepath
    sudo pipx ensurepath --global    # optional

After installing, restart your shell or run source ~/.bashrc (or equivalent) so that the pipx command is on your PATH.

### Install terminal‑bg
- **From Github** 
    ```bash
    pipx install git+https://github.com/DaarcyDev/terminal-bg.git

- **From a local clone** 
    ```bash
    git clone https://github.com/DaarcyDev/terminal-bg.git
    cd terminal-bg
    pipx install .

## Usage
Once installed, you can launch your animated terminal background with:

    
    terminal-bg [OPTIONS]


For example:
    
    # Run 'cava' on monitor 1
    terminal-bg --script cava --monitor 1

    # Run 'lavat' on monitor 0
    terminal-bg --script 'lavat -c red -R 1' --monitor 1


---

## Autostart (Run on system startup)

If you want terminal-bg to launch automatically when your system starts (for example, with a window manager like bspwm, i3, or Hyprland), you can add one of the following lines to your autostart configuration file:

  - For bspwm: edit ~/.config/bspwm/bspwmrc

  - For i3: edit ~/.config/i3/config

  - For Hyprland: edit ~/.config/hypr/hyprland.conf

Try them in this order until one works for your setup:

1. **If the binary is in your PATH (installed via pipx):**
    ```bash
    exec-once = terminal-bg --script 'cava' --monitor 1

2. **If the command is not found, try with the full path:**
    ```bash
    exec-once = /home/your-username/.local/bin/terminal-bg --script 'cava' --monitor 1

3. **If it starts too early before the session is fully ready, try with a delay:**
    ```bash
    exec-once = bash -c "sleep 10 && /home/your-username/.local/bin/terminal-bg --script 'cava' --monitor 2"
