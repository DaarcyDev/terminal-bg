import sys
import signal
import argparse
import os
import configparser
import subprocess

# Primero, comprobamos que las librerías GI estén instaladas
def check_gi_dependencies():
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('Vte', '2.91')
        gi.require_version('GtkLayerShell', '0.1')
        from gi.repository import Gtk, Vte, GtkLayerShell
    except (ImportError, ValueError):
        sys.stderr.write(
            "Required dependencies for running terminal‑bg are missing:\n"
            "   • python-gobject (Gtk)\n"
            "   • gir1.2-vte-2.91 (Vte)\n"
            "   • gir1.2-gtk-layer-shell-0.1 (GtkLayerShell)\n\n"
            "On Arch Linux:\n"
            "   sudo pacman -S python-gobject vte3 gtk-layer-shell\n\n"
            "On Debian/Ubuntu:\n"
            "   sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-vte-2.91 gir1.2-gtk-layer-shell-0.1\n\n"
            "Then run the command again.\n"
        )
        sys.exit(1)

check_gi_dependencies()

# Ahora que sabemos que existirá, importamos lo que necesitamos de GI
from .config import load_config, DEFAULT_CONFIG, CONFIG_PATH
from .terminal_window import TerminalBackground
from gi.repository import Gtk

def ensure_config_exists():
    """
    Crea el directorio y el archivo de configuración con los valores por defecto
    si no existen..
    """
    config_dir = os.path.dirname(CONFIG_PATH)
    os.makedirs(config_dir, exist_ok=True)

    if not os.path.exists(CONFIG_PATH):
        parser = configparser.ConfigParser()
        parser.read_dict(DEFAULT_CONFIG)
        with open(CONFIG_PATH, 'w') as f:
            parser.write(f)
        print(f"[+] Configuration file created at {CONFIG_PATH}")

def main():
    parser = argparse.ArgumentParser(description="Terminal as a wallpaper")

    parser.add_argument('--script', type=str, help='Script to execute in the terminal')
    parser.add_argument('--monitor', type=int, help='Monitor index to display on')
    parser.add_argument('--x', type=int, help='Horizontal position of the terminal (px)')
    parser.add_argument('--y', type=int, help='Vertical position of the terminal (px)')
    parser.add_argument('--w', type=int, help='Width of the terminal (px)')
    parser.add_argument('--h', type=int, help='Height of the terminal (px)')
    parser.add_argument('--update', action='store_true', help='Update terminal-bg from the latest Git commit')

    args = parser.parse_args()

    if args.update:
        print("🔄 Running update script...")
        script_path = os.path.join(os.path.dirname(__file__), "..", "update.sh")
        script_path = os.path.abspath(script_path)

        if not os.path.exists(script_path):
            print("❌ update.sh not found. Are you running from the source directory?")
            return

        try:
            subprocess.run(["bash", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Update failed with error code {e.returncode}")
        return

    # 1) Ensure config exists
    ensure_config_exists()

    # 2) Load config
    config = load_config()

    # 3) Validate float mode parameters
    float_params = [args.x, args.y, args.w, args.h]
    if any(p is not None for p in float_params):
        if not all(p is not None for p in float_params):
            sys.stderr.write("Error: If using position and size parameters (--x, --y, --w, --h), you must specify all of them.\n")
            sys.exit(1)
        mode = "floating"
    else:
        mode = "fullscreen"

    # 4) Determine parameters
    command = args.script if args.script else config['Behavior']['default_command']
    monitor = args.monitor if args.monitor is not None else int(config['Behavior']['default_monitor'])
    opacity = config['Appearance']['opacity']
    bg_color = config['Appearance']['background_color']

    # 5) Create window
    win = TerminalBackground(command, opacity, bg_color, monitor, x=args.x, y=args.y, width=args.w, height=args.h, mode=mode)
    win.connect("destroy", Gtk.main_quit)

    # 6) Graceful Ctrl+C
    signal.signal(signal.SIGINT, lambda *a: Gtk.main_quit())
    try:
        Gtk.main()
    except KeyboardInterrupt:
        Gtk.main_quit()
        sys.exit(0)


if __name__ == '__main__':
    main()
