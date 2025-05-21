import os
import cairo
import gi
import sys
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Vte, GLib, Gdk, GtkLayerShell

class TerminalBackground(Gtk.Window):
    def __init__(self, command, opacity, background_color, monitor):
        super().__init__(title="TerminalBackground")

        GtkLayerShell.init_for_window(self)
        GtkLayerShell.set_layer(self, GtkLayerShell.Layer.BACKGROUND)
        GtkLayerShell.set_namespace(self, "terminal-background")

        # Obtener monitor por índice
        display = Gdk.Display.get_default()
        monitor_obj = display.get_monitor(monitor)

        if monitor_obj is None:
            print(f"❌ Monitor {monitor} no encontrado.")
            sys.exit(1)

        GtkLayerShell.set_monitor(self, monitor_obj)


        for edge in [GtkLayerShell.Edge.TOP, GtkLayerShell.Edge.BOTTOM,
                     GtkLayerShell.Edge.LEFT, GtkLayerShell.Edge.RIGHT]:
            GtkLayerShell.set_anchor(self, edge, True)

        self.set_app_paintable(True)
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
        self.set_decorated(False)

        self.terminal = Vte.Terminal()
        self.terminal.set_opacity(float(opacity))

        color = Gdk.RGBA()
        color.parse(background_color)
        self.terminal.set_color_background(color)
        self.terminal.set_clear_background(True)

        self.terminal.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["bash", "-lc", command],
            None, GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None, None, -1, None, None
        )

        box = Gtk.Box()
        box.pack_start(self.terminal, True, True, 0)
        self.add(box)

        self.connect("draw", self.on_draw)
        self.show_all()

    def on_draw(self, widget, cr):
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)
        return False
