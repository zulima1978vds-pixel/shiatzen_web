import reflex as rx
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "pyuser",
    "password": "python123",
    "database": "shiatzen_usuarios",
}

ADMIN_PASSWORD = "admin123"  # Puedes cambiarla cuando quieras

class State(rx.State):
    nombre: str = ""
    email: str = ""
    mensaje: str = ""
    
    menu_abierto: bool = False
    def toggle_menu(self):
        self.menu_abierto = False

    def registrar(self):
        if not self.nombre.strip() or not self.email.strip():
            self.mensaje = "❌ Por favor, rellena todos los campos."
            return
        try:
            conexion = mysql.connector.connect(**DB_CONFIG, use_pure=True)
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes WHERE email = %s", (self.email,))
            if cursor.fetchone():
                self.mensaje = "❌ Este correo ya está registrado."
                return
            sql = "INSERT INTO clientes (nombre, email) VALUES (%s, %s)"
            cursor.execute(sql, (self.nombre, self.email))
            conexion.commit()
            conexion.close()
            self.nombre = ""
            self.email = ""
            self.mensaje = "✅ Registro exitoso. Gracias por suscribirte."
        except Exception as e:
            self.mensaje = f"❌ Error al registrar: {e}"

class AdminState(rx.State):
    contraseña: str = ""
    acceso: bool = False
    registros: list[tuple] = []
    error_admin: str = ""

    def reset_admin(self):
        self.acceso = False
        self.contraseña = ""
        self.error_admin = ""
        self.registros = []

    def verificar(self):
        if self.contraseña == ADMIN_PASSWORD:
            self.acceso = True
            self.obtener_registros()
        else:
            self.acceso = False

    def obtener_registros(self):
        try:
            conexion = mysql.connector.connect(**DB_CONFIG, use_pure=True)
            cursor = conexion.cursor()
            cursor.execute("SELECT nombre, email FROM clientes")
            self.registros = cursor.fetchall()
            conexion.close()
        except Exception as e:
            self.registros = [("Error", str(e))]
            
    def eliminar_usuario(self, nombre: str, email: str):
        try:
            conexion = mysql.connector.connect(**DB_CONFIG, use_pure=True)
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM clientes WHERE nombre = %s AND email = %s", (nombre, email))
            conexion.commit()
            conexion.close()
            self.obtener_registros()
        except Exception as e:
            print(f"❌ Error al eliminar: {e}")

# Colores
bg_color = "#fffaf2"
text_color = "#4b3e2f"
accent_color = "#c4a484"
navbar_color = "#f0e4d0"

# Componentes

def navbar():
    return rx.box(
        rx.drawer.root(
            rx.hstack(
                rx.image(src="logo_masajista.png", height="80px"),
                rx.text("ver.03", font_size="40px", font_weight="bold", color=text_color),
                rx.spacer(),
                rx.hstack(
                    rx.drawer.trigger(
                        rx.icon(tag="menu", size=28, cursor="pointer", color=text_color)
                    ),
                    rx.link(
                        rx.icon(tag="user", size=22, color=text_color),
                        href="/admin",
                        padding_left="1em"
                    ),
                    spacing="2",
                    align="center"
                ),
                justify="between",
                align="center",
                width="100%",
                padding="1em",
                background_color="white",
            ),
            rx.drawer.content(
                rx.box(
                    rx.drawer.close(
                        rx.icon(tag="x", size=28, cursor="pointer", color="white"),
                    ),
                    rx.vstack(
                        #rx.link("Inicio", href="#inicio", color="white", on_click=State.toggle_menu),
                        
                        rx.link("Sobre nosotros", href="#sobre", color="white", on_click=State.toggle_menu),
                        rx.link("Nuestros servicios", href="#servicios", color="white", on_click=State.toggle_menu),
                        rx.link("Ubicación", href="#ubicacion", color="white", on_click=State.toggle_menu),
                        rx.link("Mini presentación", href="#video", color="white", on_click=State.toggle_menu),
                        rx.link("Contacto", href="#contacto", color="white", on_click=State.toggle_menu),
                        align="start",
                        spacing="4",
                        padding="1.5em",
                    ),
                    width="180px",
                    height="35vh",
                    background_color="#333",
                ),
                side="right",
                overlay=True
            )
        ),
        position="sticky",
        top="0",
        z_index="999",
        width="100%"
    )


def section(id, title, content):
    return rx.box(
        rx.vstack(
            rx.heading(title, font_size="3xl", color=text_color),
            rx.text(content, font_size="xl", color=text_color, max_width="800px", text_align="center"),
            spacing="4"
        ),
        id=id,
        padding_y="6em",
        padding_x="2em",
        align="center",
        width="100vw",
        max_width="100vw",
        overflow_x="hidden",
        bg=bg_color
        
    )

def section_oscura(id, title, content):
    return rx.box(
        rx.vstack(
            rx.heading(title, font_size="3xl", color="white"),
            rx.text(content, font_size="xl", color="white", max_width="800px", text_align="center"),
            spacing="4"
        ),
        id=id,
        padding_y="6em",
        padding_x="2em",
        align="center",
        width="100%",
        bg="#1a1a1a"
    )

def puerta_parallax():
    return rx.box(
        height="60vh",
        width="100vw",
        background_image="url('/puerta1.jpg')",
        background_position="center",
        background_repeat="no-repeat",
        background_size="cover",
        background_attachment="fixed",  # ← clave para el efecto fondo fijo
        opacity="1",
        overflow_x="hidden"
    )

def servicios_expandido():
    return rx.box(
        rx.vstack(
            rx.heading("Nuestros Servicios Ampliados", font_size="3xl", color=text_color),
            rx.text("Ofrecemos una gama completa de tratamientos para el bienestar físico y emocional:", font_size="xl", color=text_color),
            rx.unordered_list([
                "Shiatsu terapéutico (60 min) - Equilibrio energético y alivio de tensiones.",
                "Masaje relajante con aceites esenciales (45 min).",
                "Terapia de ventosas - estimulación circulatoria y bienestar.",
                "Reflexología podal - relajación total desde los pies.",
                "Masaje deportivo - calentamiento, recuperación y prevención.",
                "Sesiones zen: mezcla de técnicas con ambiente meditativo y música suave.",
                "Pack bienestar: combinación personalizada según tus necesidades."
            ], font_size="lg", color=text_color),
            rx.text("Cada sesión termina con infusión herbal de cortesía y pequeñas pautas de estiramiento para casa.", font_size="md", color=text_color),
            spacing="3"
        ),
        id="servicios",
        padding_y="4em",
        padding_x="2em",
        width="100%",
        bg=bg_color,
        style={"scrollMarginTop": "255px"} 
    )

def map_embed():
    return rx.html("""
    <div style='padding: 2em; text-align: center;'>
        <iframe 
            src='https://www.google.com/maps?q=Calle+Vicente+Guzm%C3%A1n+16,+Aldaia,+Valencia&output=embed'
            width='100%' height='200' style='border:0;' allowfullscreen='' loading='lazy'
            referrerpolicy='no-referrer-when-downgrade'>
        </iframe>
    </div>
    """)
    

def centro_recomendado():
    return rx.section(
        rx.fragment(
            rx.heading("Centro recomendado: Shiatzen", font_size="2xl", color=text_color),
            rx.text("📍 Calle Vicente Guzmán 16, Aldaia (46960), Valencia", color=text_color),
            rx.text("📞 606.814.061", color=text_color),
            rx.text("🕐 Horario: L-V 09:30-20:00, Sáb 09:30-14:00", color=text_color),
            rx.text("💆 Sesiones de shiatsu de 60-90 min para equilibrio físico y mental.", color=text_color),
        ),
        id="centro",
        padding_y="4em",
        padding_x="2em",
        align="center",
        bg=bg_color
    )

def formulario_registro():
    return rx.center(
        rx.vstack(
            rx.heading("Regístrate para recibir ofertas y noticias", font_size="2xl", color=text_color),
            rx.input(placeholder="Tu nombre", on_change=State.set_nombre),
            rx.input(placeholder="Tu correo electrónico", on_change=State.set_email),
            rx.button("Registrarse", on_click=State.registrar, color_scheme="green"),
            rx.cond(State.mensaje != "", rx.text(State.mensaje, color="blue")),
            spacing="4",
            width="100%",
            max_width="400px",
        ),
        padding="4em",
        id="registro",
        bg="#1a1a1a"
    )

def video_presentacion():
    return rx.center(
        rx.vstack(
            rx.heading("Mini presentación del centro", font_size="2xl", color=text_color),
            rx.button("▶️ Ver presentación",
                      on_click=lambda: State.set_mensaje("video"),
                      color_scheme="teal",
                      size="3"),
            rx.cond(State.mensaje == "video",
                rx.html("""
                <div style='padding-top: 2em;'>
                    <iframe width="360" height="640"
                        src="https://www.youtube.com/embed/OqY6nPyxjNs?autoplay=1&mute=1"
                        title="Presentación Shiatzen"
                        frameborder="0"
                        allow="autoplay; encrypted-media"
                        allowfullscreen>
                    </iframe>
                </div>
                """))
        ),
        id="video",
        padding_y="4em",
        bg=bg_color,
        style={"scrollMarginTop": "500px"} 
    )
    
@rx.page(route="/", title="Shiatzen Web", on_load=State.set_mensaje(""))
def index():
    return rx.box(
        rx.html("""<link rel="icon" type="image/x-icon" href="/assets/favicon.ico?v=2">"""),
        navbar(),
        section("inicio", "Bienvenid@", "Centro de masaje terapéutico japonés. Relájate, respira, y recarga tu energía."),
        puerta_parallax(),
        servicios_expandido(),
        puerta_parallax(),
        section("ubicacion", "Ubicación", "Nos encontramos en Aldaia, a las afueras de Valencia."),
        map_embed(),
        centro_recomendado(),
        puerta_parallax(),
        video_presentacion(),
        section_oscura("contacto", "Contacto", "Puedes escribirnos o llamarnos para pedir cita."),
        formulario_registro(),
    )

@rx.page(route="/admin", title="Panel Admin", on_load=AdminState.reset_admin)
def admin():
    return rx.center(
        rx.vstack(
            rx.heading("Acceso administrador", font_size="2xl", color=text_color),
            rx.cond(
                ~AdminState.acceso,
                rx.fragment(
                    rx.input(
                        placeholder="Contraseña de acceso",
                        type_="password",
                        on_change=AdminState.set_contraseña,
                        color="white",
                        bg="black"
                    ),
                    rx.button("Entrar", on_click=AdminState.verificar, color_scheme="red"),
                    rx.cond(
                        AdminState.error_admin != "",
                        rx.text(AdminState.error_admin, color="red")
                    )
                ),
                rx.fragment(
                    rx.heading("Registros de usuarios", font_size="xl", color=text_color),
                    rx.box(
                        rx.vstack(
                            # Encabezado
                            rx.hstack(
                                rx.text("Nombre", font_weight="bold", min_width="150px", white_space="nowrap", color=text_color),
                                rx.text("Email", font_weight="bold", min_width="300px", white_space="nowrap", color=text_color)
                            ),
                            # Filas
                            rx.foreach(
                                AdminState.registros,
                                lambda item: rx.hstack(
                                    rx.text(item[0], min_width="150px", white_space="nowrap", color=text_color),
                                    rx.text(item[1], min_width="300px", word_break="break-word", color=text_color),
                                    rx.text("❌", 
                                        color="red",
                                        font_weight="bold",
                                        cursor="pointer",
                                        on_click=lambda: AdminState.eliminar_usuario(item[0], item[1])
                                    ),
                                    padding_y="0.5em",
                                    spacing="4"
                                )
                            )

                        ),
                        width="100%",
                        max_width="600px",
                        padding="1em",
                        border="1px solid #ccc",
                        border_radius="10px",
                        box_shadow="md",
                        bg=bg_color
                    )
                )
            ),
            spacing="4",
            width="100%",
            max_width="800px"
        ),
        padding="4em",
        bg=bg_color
    )

# App
app = rx.App()