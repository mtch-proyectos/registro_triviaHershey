import tkinter as tk

# Datos de la trivia sobre Hershey's
PREGUNTAS = [
    {
        "pregunta": "¿En qué año se lanzó la primera barra de chocolate con leche de Hershey's?",
        "opciones": ["1893", "1900", "1912", "1925"],
        "correcta": 1,
        "explicacion": "Milton Hershey desarrolló su fórmula secreta y lanzó la icónica barra original en 1900."
    },
    {
        "pregunta": "¿Por qué recibieron su nombre los famosos chocolates 'Hershey's Kisses'?",
        "opciones": [
            "Por el sonido 'kss' que hacía la máquina al dejarlos caer",
            "Porque Milton se los regalaba a su esposa con un beso",
            "Porque la forma recuerda a unos labios sonriendo",
            "Fue una idea publicitaria inventada en 1950"
        ],
        "correcta": 0,
        "explicacion": "Se les llamó Kisses por el sonido y movimiento que hacía la boquilla al depositar la gota de chocolate."
    },
    {
        "pregunta": "¿Qué producto vendía Milton Hershey con éxito antes del chocolate?",
        "opciones": ["Galletas de avena", "Caramelos de leche (toffees)", "Helados de vainilla", "Refrescos de cola"],
        "correcta": 1,
        "explicacion": "Fundó la 'Lancaster Caramel Company' tras quebrantar dos confiterías previas."
    },
    {
        "pregunta": "¿De qué gran tragedia histórica se salvó Milton Hershey en 1912?",
        "opciones": [
            "Un gran incendio en Filadelfia",
            "El hundimiento del Titanic",
            "El terremoto de San Francisco",
            "Un descarrilamiento de tren"
        ],
        "correcta": 1,
        "explicacion": "Tenía billetes para el viaje inaugural del Titanic, pero canceló a última hora por negocios."
    },
    {
        "pregunta": "¿Quién es el dueño mayoritario de la empresa Hershey's en la actualidad?",
        "opciones": [
            "Una corporación multinacional suiza",
            "Los descendientes directos de Milton Hershey",
            "El fideicomiso de la Escuela Milton Hershey para niños huérfanos",
            "El gobierno del estado de Pensilvania"
        ],
        "correcta": 2,
        "explicacion": "Milton donó toda su fortuna a la escuela internado para niños vulnerables que fundó con su esposa."
    },
    {
        "pregunta": "¿Cómo se llamó el chocolate ultra resistente al calor para la Segunda Guerra Mundial?",
        "opciones": ["Ración D", "Barra M1", "Victory Bar", "Pack Táctico"],
        "correcta": 0,
        "explicacion": "Hershey fabricó más de 3,000 millones de barras de la 'Ración D' para el ejército de EE. UU."
    }
]

# Estilos de color
BG_DARK = "#1E1E2E"       # Fondo oscuro
CARD_BG = "#2B2B3D"       # Tarjeta
ACCENT_GOLD = "#FFC72C"   # Dorado
TEXT_LIGHT = "#FFFFFF"    # Texto blanco
TEXT_MUTED = "#A6ADC8"    # Texto gris
BTN_BG = "#363A4F"        # Botón normal
COLOR_SUCCESS = "#2ECC71" # Verde
COLOR_DANGER = "#E74C3C"  # Rojo

class TriviaHersheyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hershey's Chocolate Trivia")
        self.root.geometry("600x680")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(False, False)

        self.indice_pregunta = 0
        self.puntuacion = 0

        self.crear_pantalla_inicio()

    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def crear_pantalla_inicio(self):
        self.limpiar_pantalla()

        container = tk.Frame(self.root, bg=BG_DARK, padx=30, pady=40)
        container.pack(expand=True, fill="both")

        lbl_logo = tk.Label(container, text="🍫", font=("Segoe UI Emoji", 50), bg=BG_DARK, fg=ACCENT_GOLD)
        lbl_logo.pack(pady=(20, 10))

        lbl_titulo = tk.Label(container, text="HERSHEY'S TRIVIA", font=("Helvetica", 22, "bold"), bg=BG_DARK, fg=ACCENT_GOLD)
        lbl_titulo.pack(pady=5)

        lbl_subtitulo = tk.Label(
            container,
            text="Descubre la fascinante historia detrás del imperio del chocolate.",
            font=("Helvetica", 11), bg=BG_DARK, fg=TEXT_MUTED, wraplength=450, justify="center"
        )
        lbl_subtitulo.pack(pady=(0, 40))

        btn_iniciar = tk.Button(
            container, text="¡COMENZAR EL DESAFÍO!", font=("Helvetica", 12, "bold"),
            bg=ACCENT_GOLD, fg="black", activebackground="#E0AF25", activeforeground="black",
            bd=0, relief="flat", padx=20, pady=12, cursor="hand2", command=self.iniciar_juego
        )
        btn_iniciar.pack(fill="x")

    def iniciar_juego(self):
        self.indice_pregunta = 0
        self.puntuacion = 0
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        self.limpiar_pantalla()

        p_actual = PREGUNTAS[self.indice_pregunta]

        # Encabezado
        header = tk.Frame(self.root, bg=BG_DARK, padx=30, pady=20)
        header.pack(fill="x")

        lbl_progreso = tk.Label(
            header, text=f"Pregunta {self.indice_pregunta + 1} de {len(PREGUNTAS)}",
            font=("Helvetica", 10, "bold"), bg=BG_DARK, fg=ACCENT_GOLD
        )
        lbl_progreso.pack(anchor="w")

        canvas_bar = tk.Canvas(header, height=6, bg=BTN_BG, highlightthickness=0)
        canvas_bar.pack(fill="x", pady=(5, 0))
        ancho = (self.indice_pregunta + 1) / len(PREGUNTAS) * 540
        canvas_bar.create_rectangle(0, 0, ancho, 6, fill=ACCENT_GOLD, width=0)

        # Pregunta
        card = tk.Frame(self.root, bg=CARD_BG, padx=20, pady=20)
        card.pack(fill="x", padx=30, pady=10)

        lbl_pregunta = tk.Label(
            card, text=p_actual["pregunta"], font=("Helvetica", 12, "bold"),
            bg=CARD_BG, fg=TEXT_LIGHT, wraplength=480, justify="left"
        )
        lbl_pregunta.pack(anchor="w")

        # Contenedor de Botones
        opts_frame = tk.Frame(self.root, bg=BG_DARK, padx=30, pady=10)
        opts_frame.pack(fill="both", expand=True)

        self.botones_opciones = []
        for i, opcion in enumerate(p_actual["opciones"]):
            # Uso de lambda asignando i explícitamente en el scope
            btn = tk.Button(
                opts_frame,
                text=f"{chr(65+i)}.  {opcion}",
                font=("Helvetica", 10, "bold"),
                bg=BTN_BG, fg=TEXT_LIGHT,
                activebackground="#494D64", activeforeground=TEXT_LIGHT,
                bd=0, relief="flat", padx=15, pady=10, cursor="hand2",
                anchor="w", wraplength=450, justify="left",
                command=lambda idx=i: self.verificar_respuesta(idx)
            )
            btn.pack(fill="x", pady=5)
            self.botones_opciones.append(btn)

        self.feedback_frame = tk.Frame(self.root, bg=BG_DARK, padx=30, pady=10)
        self.feedback_frame.pack(fill="x")

    def verificar_respuesta(self, opcion_seleccionada):
        p_actual = PREGUNTAS[self.indice_pregunta]
        correcta = p_actual["correcta"]

        # Deshabilitar botones para evitar múltiples clics
        for btn in self.botones_opciones:
            btn.config(state="disabled")

        # Marcar colores
        if opcion_seleccionada == correcta:
            self.puntuacion += 1
            self.botones_opciones[opcion_seleccionada].config(bg=COLOR_SUCCESS, fg="white")
        else:
            self.botones_opciones[opcion_seleccionada].config(bg=COLOR_DANGER, fg="white")
            self.botones_opciones[correcta].config(bg=COLOR_SUCCESS, fg="white")

        # Mostrar dato curioso
        lbl_explicacion = tk.Label(
            self.feedback_frame,
            text=f"💡 {p_actual['explicacion']}",
            font=("Helvetica", 10, "italic"), bg=BG_DARK, fg=TEXT_MUTED,
            wraplength=520, justify="center"
        )
        lbl_explicacion.pack(pady=(0, 10))

        btn_siguiente = tk.Button(
            self.feedback_frame, text="Siguiente Pregunta ➔",
            font=("Helvetica", 10, "bold"), bg=ACCENT_GOLD, fg="black",
            bd=0, relief="flat", padx=15, pady=8, cursor="hand2",
            command=self.siguiente_pregunta
        )
        btn_siguiente.pack(fill="x")

    def siguiente_pregunta(self):
        self.indice_pregunta += 1
        if self.indice_pregunta < len(PREGUNTAS):
            self.mostrar_pregunta()
        else:
            self.mostrar_resultados()

    def mostrar_resultados(self):
        self.limpiar_pantalla()

        container = tk.Frame(self.root, bg=BG_DARK, padx=30, pady=40)
        container.pack(expand=True, fill="both")

        lbl_trofeo = tk.Label(container, text="🏆", font=("Segoe UI Emoji", 50), bg=BG_DARK)
        lbl_trofeo.pack(pady=10)

        lbl_titulo = tk.Label(container, text="¡Juego Terminado!", font=("Helvetica", 20, "bold"), bg=BG_DARK, fg=ACCENT_GOLD)
        lbl_titulo.pack(pady=5)

        porcentaje = (self.puntuacion / len(PREGUNTAS)) * 100
        lbl_score = tk.Label(
            container, text=f"Puntuación: {self.puntuacion} / {len(PREGUNTAS)}",
            font=("Helvetica", 15, "bold"), bg=BG_DARK, fg=TEXT_LIGHT
        )
        lbl_score.pack(pady=10)

        if porcentaje == 100:
            mensaje = "🥇 ¡Maestro Chocolatero! Conoces cada detalle de la historia de Hershey's."
        elif porcentaje >= 70:
            mensaje = "🥈 ¡Excelente trabajo! Tienes un gran conocimiento histórico."
        else:
            mensaje = "🍫 ¡Buen intento! Siempre hay más datos curiosos por aprender."

        lbl_mensaje = tk.Label(
            container, text=mensaje, font=("Helvetica", 11),
            bg=BG_DARK, fg=TEXT_MUTED, wraplength=450, justify="center"
        )
        lbl_mensaje.pack(pady=(0, 30))

        btn_reiniciar = tk.Button(
            container, text="Jugar de Nuevo", font=("Helvetica", 11, "bold"),
            bg=ACCENT_GOLD, fg="black", bd=0, relief="flat", padx=20, pady=10, cursor="hand2",
            command=self.iniciar_juego
        )
        btn_reiniciar.pack(fill="x")

if __name__ == "__main__":
    root = tk.Tk()
    app = TriviaHersheyApp(root)
    root.mainloop()