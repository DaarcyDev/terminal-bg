import os
import cairo
import gi
import sys
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')
gi.require_version('GtkLayerShell', '0.1')
from gi.repository import Gtk, Vte, GLib, Gdk, GtkLayerShell

class TerminalBackground(Gtk.Window):
    MIN_W, MIN_H = 50, 50
    def __init__(self, command, opacity, background_color, monitor, x=None, y=None, width=None, height=None, mode="fullscreen"):
        super().__init__(title="TerminalBackground")
        
        display = Gdk.Display.get_default()
        monitor_obj = display.get_monitor(monitor)
        
        if monitor_obj is None:
            n_monitors = display.get_n_monitors()
            sys.stderr.write(
                f"Error: Monitor with index {monitor} does not exist. "
                f"{n_monitors} monitor(s) detected.\n"
            )
            sys.exit(1)
        
        geom = monitor_obj.get_geometry()
        mon_w, mon_h = geom.width, geom.height
        
        if mode == "floating":
            # comprueba mínimos
            if width < self.MIN_W or height < self.MIN_H:
                sys.stderr.write(
                    f"Error: Minimum size is --w {self.MIN_W}, --h {self.MIN_H}. "
                    f"Received: --w {width}, --h {height}.\n"
                )
                sys.exit(1)
            # comprueba que no se salga de la pantalla
            if x + width > mon_w or y + height > mon_h:
                sys.stderr.write(
                    f"Error: The window exceeds the monitor bounds ({mon_w}×{mon_h}). "
                    f"Position+Size: x+width={x+width}, y+height={y+height}.\n"
                )
                sys.exit(1)
        
        GtkLayerShell.init_for_window(self)
        if mode == "fullscreen":
            GtkLayerShell.set_layer(self, GtkLayerShell.Layer.BACKGROUND)
            for edge in [GtkLayerShell.Edge.TOP, GtkLayerShell.Edge.BOTTOM, GtkLayerShell.Edge.LEFT, GtkLayerShell.Edge.RIGHT]:
                GtkLayerShell.set_anchor(self, edge, True)
        else:
            m_top = y
            m_left = x
            m_right = mon_w - x - width
            m_bottom = mon_h - y - height

            GtkLayerShell.set_layer(self, GtkLayerShell.Layer.BACKGROUND)
            for edge in (GtkLayerShell.Edge.TOP, GtkLayerShell.Edge.BOTTOM, GtkLayerShell.Edge.LEFT, GtkLayerShell.Edge.RIGHT):
                GtkLayerShell.set_anchor(self, edge, True)

            # Asignar márgenes
            GtkLayerShell.set_margin(self, GtkLayerShell.Edge.TOP, m_top)
            GtkLayerShell.set_margin(self, GtkLayerShell.Edge.LEFT, m_left)
            GtkLayerShell.set_margin(self, GtkLayerShell.Edge.RIGHT, m_right)
            GtkLayerShell.set_margin(self, GtkLayerShell.Edge.BOTTOM, m_bottom)



        GtkLayerShell.set_namespace(self, "terminal-background")

        # Obtener monitor por índice
        display = Gdk.Display.get_default()
        monitor_obj = display.get_monitor(monitor)

        if monitor_obj is None:
            sys.exit(1)

        GtkLayerShell.set_monitor(self, monitor_obj)


        for edge in [GtkLayerShell.Edge.TOP, GtkLayerShell.Edge.BOTTOM, GtkLayerShell.Edge.LEFT, GtkLayerShell.Edge.RIGHT]:
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
