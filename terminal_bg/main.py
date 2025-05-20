import sys
import signal
import argparse
import os
import configparser

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
            "❌ No se han encontrado las dependencias necesarias para ejecutar terminal‑bg:\n"
            "   • python-gobject (Gtk)\n"
            "   • gir1.2-vte-2.91 (Vte)\n"
            "   • gir1.2-gtk-layer-shell-0.1 (GtkLayerShell)\n\n"
            "En Arch Linux:\n"
            "   sudo pacman -S python-gobject vte3 gtk-layer-shell\n\n"
            "En Debian/Ubuntu:\n"
            "   sudo apt install python3-gi gir1.2-gtk-3.0 gir1.2-vte-2.91 gir1.2-gtk-layer-shell-0.1\n\n"
            "Luego vuelve a ejecutar el comando.\n"
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
    si no existen.
    """
    config_dir = os.path.dirname(CONFIG_PATH)
    os.makedirs(config_dir, exist_ok=True)

    if not os.path.exists(CONFIG_PATH):
        parser = configparser.ConfigParser()
        parser.read_dict(DEFAULT_CONFIG)
        with open(CONFIG_PATH, 'w') as f:
            parser.write(f)
        print(f"[+] Archivo de configuración creado en {CONFIG_PATH}")

def main():
    # 1) Asegurarnos de que exista la config
    ensure_config_exists()

    # 2) Cargar configuración (mezcla de DEFAULTS + ~/.config/terminal-bg/terminal-bg.conf)
    config = load_config()

    # 3) Parsear argumentos de línea de comando
    parser = argparse.ArgumentParser(description="Terminal como fondo de pantalla")
    parser.add_argument('--script', type=str, help='Script a ejecutar en la terminal')
    parser.add_argument('--monitor', type=int, help='Monitor donde mostrar (no implementado)')
    args = parser.parse_args()

    # 4) Elegir comando & parámetros
    command = args.script if args.script else config['Behavior']['default_command']
    opacity = config['Appearance']['opacity']
    bg_color = config['Appearance']['background_color']

    # 5) Crear la ventana y arrancar GTK
    win = TerminalBackground(command, opacity, bg_color)
    win.connect("destroy", Gtk.main_quit)

    # 6) Manejador de Ctrl+C para cerrar sin traceback
    signal.signal(signal.SIGINT, lambda *a: Gtk.main_quit())
    try:
        Gtk.main()
    except KeyboardInterrupt:
        Gtk.main_quit()
        sys.exit(0)

if __name__ == '__main__':
    main()
