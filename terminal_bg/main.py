import argparse
import os
import configparser
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
    Gtk.main()
