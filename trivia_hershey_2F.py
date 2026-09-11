import sys
import os
import csv
import pygame
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Requiere: pip install pillow

def obtener_ruta_recurso(ruta_relativa):
    """Obtiene la ruta absoluta para recursos, compatible con entorno dev y PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath("."), ruta_relativa)

# ==========================================
# PALETAS DE COLORES SEPARADAS
# ==========================================

# --- PALETA 1: TEMA CHOCOLATE OSCURO (Inicio, Registro, Resultado) ---
BG_DARK_CARD = "#1C0D08"        # Tarjeta Marrón Oscuro
BG_DARK_HEADER = "#120704"      # Encabezado súper oscuro
TEXT_DARK_WHITE = "#FFFFFF"     # Texto blanco
TEXT_DARK_SILVER = "#CBD5E1"    # Texto secundario claro
GOLD_ACCENT = "#FFD700"         # Dorado Hershey's
GOLD_LIGHT = "#FFF099"

# --- PALETA 2: TEMA COOKIES 'N' CREAM (Pantalla de Preguntas) ---
# Diseñada para contrastar impecablemente sobre fondo2.jpeg (fondo claro/crema)
BG_LIGHT_CARD = "#1A0C0E"       # Fondo de tarjeta oscuro (para contraste sobre crema)
BG_LIGHT_HEADER = "#110608"     # Encabezado oscuro dentro de la tarjeta
KISSES_BLUE = "#0066CC"         # Azul eléctrico icónico de Kisses / Cookies 'n' Cream
TEXT_LIGHT_WHITE = "#FFFFFF"    # Texto sobre tarjeta oscura
TEXT_LIGHT_SILVER = "#E2E8F0"

# --- ESTILO BOTONES CHOCOLATE (Compartido/Generico) ---
CHOCO_BASE = "#3D1C12"
CHOCO_HIGHLIGHT = "#5A2B1C"
CHOCO_DARK = "#24100A"


class HersheysTriviaApp:
    def __init__(self, root):
        self.root = root

        # Inicializar el sistema de audio de pygame
        pygame.mixer.init()

        self.root.title("Trivia Hershey's Lover")

        # Ruta de la música de fondo (asegúrate de incluirla en recursos)
        self.ruta_musica_inicio = obtener_ruta_recurso("audio/musica_inicio.mp3")

        # --- PANTALLA COMPLETA ---
        self.root.attributes('-fullscreen', True)
        #self.root.bind("<Escape>", lambda event: self.root.attributes('-fullscreen', False))
        
        # Cierra la ventana por completo al presionar Esc
        #self.root.bind("<Escape>", lambda event: self.root.destroy())
        # Deshabilitar Esc para el usuario y usar Ctrl+Q para salir
        self.root.bind("<Control-q>", lambda event: self.root.destroy())        

        # Cache de imágenes de fondo
        self.bg_fondo1_tk = None
        self.bg_fondo2_tk = None
        
        self.cargar_fondos()

        self.root.geometry("1024x768")
        self.root.configure(bg=BG_DARK_CARD)

        self.score = 0
        self.respuestas_usuario = {}
        self.pregunta_actual = 0

        self.opcion_seleccionada = None
        self.botones_canvas = []
        self.timer_transicion = None

        self.ruta_banner_fijo = "banner.png"
        self.banner_img_tk = None
        self.imagenes_cache = {}

        self.cargar_imagen_banner_fijo()

        # Datos de Preguntas
        self.preguntas = [
            {
                "id": 1,
                "pregunta": "1. Tu chocolate ideal es...",
                "opciones": [
                    ("A. Cremoso", 10, "images/cream.jpg"),
                    ("B. Intenso", 15, "images/dark.jpg"),
                    ("C. Con toppings", 12, "images/cookies.jpg"),
                    ("D. ¡Todos!", 20, "images/variedad.jpg")
                ]
            },
            {
                "id": 2,
                "pregunta": "2. ¿Cuál reconoces con los ojos cerrados?",
                "opciones": [
                    ("A. Hershey's Milk Chocolate", 15, "images/milk.jpg"),
                    ("B. Hershey's Cookies 'n' Cream", 20, "images/cookies.jpg"),
                    ("C. Hershey's Special Dark", 15, "images/dark.jpg"),
                    ("D. Todos por su olor característico", 25, "images/variedad.jpg")
                ]
            },
            {
                "id": 3,
                "pregunta": "3. ¿Cuál de estos SÍ es un producto Hershey’s?",
                "opciones": [
                    ("A. Kisses Classic", 10, "images/kisses.jpg"),
                    ("B. Pelon Pelo Rico", 15, "images/pelon.jpg"),
                    ("C. Reese's Peanut Butter Cups", 20, "images/reeses.jpg"),
                    ("D. ¡Todos pertenecen a la familia Hershey's!", 25, "images/variedad.jpg")
                ]
            },
            {
                "id": 4,
                "pregunta": "4. Completa la frase: 'Chocolate + __ = momento perfecto'",
                "opciones": [
                    ("A. Una película / serie", 15, "images/milk.jpg"),
                    ("B. Un café / merienda", 15, "images/dark.jpg"),
                    ("C. Compartir con amigos", 20, "images/conamigos.jpg"),
                    ("D. Un antojo nocturno", 10, "images/cookies.jpg")
                ]
            },
            {
                "id": 5,
                "pregunta": "5. Pregunta final: ¿Cuánto crees que sabes de Hershey’s?",
                "opciones": [
                    ("A. Lo básico, ¡pero me encanta!", 10, "images/milk.jpg"),
                    ("B. Sé bastante, soy fan", 15, "images/dark.jpg"),
                    ("C. ¡Soy un experto total!", 20, "images/kisses.jpg"),
                    ("D. Vivo para comer chocolate", 25, "images/variedad.jpg")
                ]
            }
        ]

        self.mostrar_pantalla_inicio()

    def reproducir_musica_inicio(self):
        """Carga y reproduce la música de fondo en bucle infinito."""
        if os.path.exists(self.ruta_musica_inicio):
            try:
                pygame.mixer.music.load(self.ruta_musica_inicio)
                pygame.mixer.music.set_volume(0.25)  # Volumen al 25%
                pygame.mixer.music.play(-1)          # -1 indica bucle infinito
            except Exception as e:
                print(f"Error al cargar audio: {e}")

    def detener_musica(self):
        """Detiene o atenúa la música al iniciar el juego."""
        pygame.mixer.music.fadeout(1000)  # Desvanecimiento progresivo en 1 segundo

    def cargar_fondos(self):
        """Carga y escala ambas imágenes de fondo para ajustar a la pantalla actual."""
        ancho = self.root.winfo_screenwidth()
        alto = self.root.winfo_screenheight()

        # Cargar Fondo 1 (Chocolate)
        ruta1 = obtener_ruta_recurso("images/fondo_app.jpeg")
        if os.path.exists(ruta1):
            try:
                img1 = Image.open(ruta1).resize((ancho, alto), Image.Resampling.LANCZOS)
                self.bg_fondo1_tk = ImageTk.PhotoImage(img1)
            except Exception as e:
                print(f"Error al cargar fondo 1: {e}")

        # Cargar Fondo 2 (Cookies 'n' Cream)
        ruta2 = obtener_ruta_recurso("images/fondo2.jpeg")
        if os.path.exists(ruta2):
            try:
                img2 = Image.open(ruta2).resize((ancho, alto), Image.Resampling.LANCZOS)
                self.bg_fondo2_tk = ImageTk.PhotoImage(img2)
            except Exception as e:
                print(f"Error al cargar fondo 2: {e}")

    def cargar_imagen_banner_fijo(self):
        ruta_real = obtener_ruta_recurso(self.ruta_banner_fijo)
        if os.path.exists(ruta_real):
            try:
                img = Image.open(ruta_real)
                img.thumbnail((500, 150), Image.Resampling.LANCZOS)
                self.banner_img_tk = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error al cargar el banner: {e}")

    def obtener_imagen_opcion(self, nombre_archivo):
        ruta_real = obtener_ruta_recurso(nombre_archivo)
        if ruta_real in self.imagenes_cache:
            return self.imagenes_cache[ruta_real]

        if os.path.exists(ruta_real):
            try:
                img = Image.open(ruta_real)
                img.thumbnail((260, 140), Image.Resampling.LANCZOS)
                tk_img = ImageTk.PhotoImage(img)
                self.imagenes_cache[ruta_real] = tk_img
                return tk_img
            except Exception as e:
                print(f"Error al cargar imagen {ruta_real}: {e}")
        return None

    # ==========================================
    # PANTALLA 1: INICIO (Con Fondo 1 y sin contenedor para las letras)
    # ==========================================
    # ==========================================
    # PANTALLA 1: INICIO (Sin Contenedor / Textos en Canvas)
    # ==========================================
    def mostrar_pantalla_inicio(self):
        self.limpiar_pantalla()

        # Iniciar audio al volver o entrar a la pantalla principal
        self.reproducir_musica_inicio()

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        centro_x = ancho_pantalla // 2

        # 1. Canvas Principal con Fondo 1 (Chocolate Oscuro)
        main_canvas = tk.Canvas(self.root, highlightthickness=0)
        main_canvas.pack(fill="both", expand=True)

        if self.bg_fondo1_tk:
            main_canvas.create_image(0, 0, image=self.bg_fondo1_tk, anchor="nw")
        else:
            main_canvas.configure(bg=BG_DARK_CARD)

        # 2. Textos Flotantes Dibujados Directo en Canvas

        # Marca Superior
        main_canvas.create_text(
            centro_x, 180,
            text="TRIVIA HERSHEY'S LOVER",
            font=("Helvetica", 16, "bold"),
            fill=TEXT_DARK_SILVER,
            anchor="center"
        )

        # Título Principal (Dorado Hershey's)
        main_canvas.create_text(
            centro_x, 260,
            text="¿QUÉ TAN HERSHEY'S\nLOVER ERES?",
            font=("Helvetica", 38, "bold"),
            fill=GOLD_ACCENT,
            justify="center",
            anchor="center"
        )

        # Bajada / Descripción
        main_canvas.create_text(
            centro_x, 370,
            text="Responde 5 preguntas rápidas | Regístrate\nDescubre tu nivel | Gana premios exclusivos",
            font=("Helvetica", 18),
            fill=TEXT_DARK_WHITE,
            justify="center",
            anchor="center"
        )

        # 3. Botón Principal "¡EMPEZAR TRIVIA!" (Dibujado en Canvas)
        width_btn = 360
        height_btn = 65
        x1_btn = centro_x - (width_btn // 2)
        y1_btn = 430
        x2_btn = centro_x + (width_btn // 2)
        y2_btn = y1_btn + height_btn

        # Sombra y Cuerpo del Botón Dorado
        btn_shadow = main_canvas.create_rectangle(x1_btn + 4, y1_btn + 4, x2_btn + 4, y2_btn + 4, fill="#120704", outline="")
        btn_rect = main_canvas.create_rectangle(x1_btn, y1_btn, x2_btn, y2_btn, fill=GOLD_ACCENT, outline="#FFFFFF", width=2)
        btn_text = main_canvas.create_text(
            centro_x, y1_btn + (height_btn // 2),
            text="¡EMPEZAR TRIVIA!",
            font=("Helvetica", 20, "bold"),
            fill=BG_DARK_CARD,
            anchor="center"
        )

        # Eventos del Botón
        def on_click_start(e):
            self.iniciar_trivia()

        for element_id in [btn_shadow, btn_rect, btn_text]:
            main_canvas.tag_bind(element_id, "<Button-1>", on_click_start)
            main_canvas.tag_bind(element_id, "<Enter>", lambda e: main_canvas.config(cursor="hand2"))
            main_canvas.tag_bind(element_id, "<Leave>", lambda e: main_canvas.config(cursor=""))

        # 4. Banner Footer en la Parte Inferior
        banner_container = tk.Frame(
            main_canvas, 
            bg=BG_DARK_HEADER, 
            width=500, 
            height=110, 
            highlightbackground=GOLD_ACCENT, 
            highlightthickness=1.5
        )
        banner_container.pack_propagate(False)

        # Posicionamos el marco del banner flotando hacia el fondo inferior
        main_canvas.create_window(centro_x, alto_pantalla - 120, window=banner_container, anchor="n")

        lbl_banner = tk.Label(banner_container, bg=BG_DARK_HEADER)
        lbl_banner.pack(expand=True, fill="both")

        if self.banner_img_tk:
            lbl_banner.config(image=self.banner_img_tk)
        else:
            lbl_banner.config(text="🍫 HERSHEY'S 🍫", font=("Helvetica", 16, "bold"), fg=GOLD_ACCENT)
    
    # ==========================================
    # PANTALLA 2: PREGUNTAS (Texto Dibujado Directo en Canvas)
    # ==========================================
    def iniciar_trivia(self):
        # Detener la música justo al hacer clic en "¡EMPEZAR TRIVIA!"
        self.detener_musica()
        
        self.score = 0
        self.pregunta_actual = 0
        self.respuestas_usuario = {}
        self.mostrar_pregunta()

    def mostrar_pregunta(self):
        self.limpiar_pantalla()
        self.opcion_seleccionada = None
        self.botones_canvas = []

        q_data = self.preguntas[self.pregunta_actual]
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        centro_x = ancho_pantalla // 2

        # 1. Canvas Principal de Pantalla Completa
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)

        # Cargar Fondo 2 (Cookies 'n' Cream)
        if self.bg_fondo2_tk:
            self.main_canvas.create_image(0, 0, image=self.bg_fondo2_tk, anchor="nw")
        else:
            self.main_canvas.configure(bg="#F4EBE1")

        # 2. Textos Dibujados Directamente en el Canvas (Sin Frame / Sin Fondo)
        
        # Header / Marca
        self.main_canvas.create_text(
            centro_x, 120,
            text="[ LOGO PROVEEDOR / MARCA ]",
            font=("Helvetica", 12, "bold"),
            fill=CHOCO_BASE,
            anchor="center"
        )

        # Indicador de Progreso (Azul Kisses)
        self.main_canvas.create_text(
            centro_x, 150,
            text=f"PREGUNTA {self.pregunta_actual + 1} DE {len(self.preguntas)}",
            font=("Helvetica", 14, "bold"),
            fill=KISSES_BLUE,
            anchor="center"
        )

        # Texto de la Pregunta (Marrón Chocolate Oscuro con ajuste de línea)
        self.main_canvas.create_text(
            centro_x, 205,
            text=q_data["pregunta"],
            font=("Helvetica", 24, "bold"),
            fill="#24100A",
            width=750,
            justify="center",
            anchor="center"
        )

        # 3. Dibujar Botones de Opciones
        y_inicial = 280
        espaciado = 60

        for i, (texto, puntos, foto_path) in enumerate(q_data["opciones"]):
            pos_y = y_inicial + (i * espaciado)
            self.crear_boton_chocolate_canvas(self.main_canvas, centro_x, pos_y, i, texto, puntos, foto_path)

        # 4. Cuadro de Previsualización de Imagen (Debajo de los botones)
        y_preview = y_inicial + (len(q_data["opciones"]) * espaciado) + 20
        
        preview_frame = tk.Frame(
            self.main_canvas, 
            bg=BG_DARK_HEADER, 
            width=260, 
            height=95, 
            highlightbackground=KISSES_BLUE, 
            highlightthickness=1.5
        )
        preview_frame.pack_propagate(False)

        # Insertar la previsualización dentro del Canvas principal
        self.main_canvas.create_window(centro_x, y_preview, window=preview_frame, anchor="n")

        self.lbl_preview_img = tk.Label(
            preview_frame, 
            text="Selecciona una opción 🍫", 
            font=("Helvetica", 12, "italic"), 
            bg=BG_DARK_HEADER, 
            fg=TEXT_LIGHT_SILVER
        )
        self.lbl_preview_img.pack(expand=True, fill="both")

    def crear_boton_chocolate_canvas(self, canvas_padre, x, y, index, texto, puntos, foto_path):
        """Crea un botón estilizado directamente dentro del Canvas principal."""
        width = 620
        height = 50
        x1 = x - (width // 2)
        y1 = y
        x2 = x + (width // 2)
        y2 = y + height

        # Sombra y Botón
        rect_shadow = canvas_padre.create_rectangle(x1 + 4, y1 + 4, x2 + 4, y2 + 4, fill=CHOCO_DARK, outline="")
        rect_main = canvas_padre.create_rectangle(x1, y1, x2, y2, fill=CHOCO_BASE, outline=GOLD_ACCENT, width=2)
        
        # Biseles
        line_top = canvas_padre.create_line(x1 + 2, y1 + 2, x2 - 2, y1 + 2, fill=CHOCO_HIGHLIGHT, width=2)
        line_left = canvas_padre.create_line(x1 + 2, y1 + 2, x1 + 2, y2 - 2, fill=CHOCO_HIGHLIGHT, width=2)

        # Texto de la Opción
        text_id = canvas_padre.create_text(
            x, y + (height // 2), 
            text=texto, 
            fill=TEXT_LIGHT_WHITE, 
            font=("Helvetica", 15, "bold"),
            width=width - 20,
            justify="center"
        )

        # Guardar referencias de los elementos para los eventos de clic
        item_data = {
            "rect_main": rect_main,
            "text_id": text_id,
            "puntos": puntos,
            "texto": texto,
            "foto_path": foto_path,
            "index": index,
            "ids": [rect_shadow, rect_main, line_top, line_left, text_id]
        }
        self.botones_canvas.append(item_data)

        def seleccionar_opcion(e):
            if self.timer_transicion:
                self.root.after_cancel(self.timer_transicion)
                self.timer_transicion = None

            self.opcion_seleccionada = (puntos, texto)
            
            # Resaltar la opción seleccionada
            for btn in self.botones_canvas:
                if btn["index"] == index:
                    canvas_padre.itemconfig(btn["rect_main"], fill=CHOCO_HIGHLIGHT, outline="#FFFFFF", width=3)
                    canvas_padre.itemconfig(btn["text_id"], fill=GOLD_ACCENT)
                else:
                    canvas_padre.itemconfig(btn["rect_main"], fill=CHOCO_BASE, outline=GOLD_ACCENT, width=2)
                    canvas_padre.itemconfig(btn["text_id"], fill=TEXT_LIGHT_WHITE)

            # Actualizar previsualización
            img_tk = self.obtener_imagen_opcion(foto_path)
            if img_tk:
                self.lbl_preview_img.config(image=img_tk, text="")
                self.lbl_preview_img.image = img_tk
            else:
                self.lbl_preview_img.config(image="", text=f"🍫 [{texto}]")

            self.timer_transicion = self.root.after(1500, self.confirmar_respuesta)

        # Vincular evento de clic a todos los componentes gráficos del botón
        for element_id in item_data["ids"]:
            canvas_padre.tag_bind(element_id, "<Button-1>", seleccionar_opcion)
            canvas_padre.tag_bind(element_id, "<Enter>", lambda e: canvas_padre.config(cursor="hand2"))
            canvas_padre.tag_bind(element_id, "<Leave>", lambda e: canvas_padre.config(cursor=""))

    def confirmar_respuesta(self):
        if not self.opcion_seleccionada:
            return

        puntos, opcion_texto = self.opcion_seleccionada
        self.score += puntos
        self.respuestas_usuario[f"pregunta_{self.pregunta_actual + 1}"] = opcion_texto
        self.pregunta_actual += 1

        if self.pregunta_actual < len(self.preguntas):
            self.mostrar_pregunta()
        else:
            self.mostrar_formulario_registro()

    # ==========================================
    # PANTALLA 3: REGISTRO (Con Fondo 1)
    # ==========================================
    def mostrar_formulario_registro(self):
        self.limpiar_pantalla()

        main_canvas = tk.Canvas(self.root, highlightthickness=0)
        main_canvas.pack(fill="both", expand=True)

        if self.bg_fondo1_tk:
            main_canvas.create_image(0, 0, image=self.bg_fondo1_tk, anchor="nw")
        else:
            main_canvas.configure(bg=BG_DARK_CARD)

        center_frame = tk.Frame(main_canvas, bg=BG_DARK_CARD)
        main_canvas.create_window(
            self.root.winfo_screenwidth() // 2,
            self.root.winfo_screenheight() // 2,
            window=center_frame,
            anchor="center"
        )

        title = tk.Label(
            center_frame, 
            text="¡CASI LISTO!", 
            font=("Helvetica", 32, "bold"), 
            bg=BG_DARK_CARD, 
            fg=GOLD_ACCENT
        )
        title.pack(pady=(10, 5))

        subtitle = tk.Label(
            center_frame, 
            text="Ingresa tus datos para revelar tu nivel Hershey's y participar:", 
            font=("Helvetica", 17), 
            bg=BG_DARK_CARD, 
            fg=TEXT_DARK_WHITE
        )
        subtitle.pack(pady=10)

        card_form = tk.Frame(center_frame, bg=BG_DARK_HEADER, padx=35, pady=35, highlightbackground=GOLD_ACCENT, highlightthickness=2)
        card_form.pack(pady=15)

        tk.Label(card_form, text="Nombre Completo:", font=("Helvetica", 16, "bold"), bg=BG_DARK_HEADER, fg=TEXT_DARK_WHITE).grid(row=0, column=0, sticky="w", pady=15, padx=10)
        self.entry_nombre = tk.Entry(card_form, font=("Helvetica", 16), width=22, bg="#FFFFFF", fg="#000000")
        self.entry_nombre.grid(row=0, column=1, pady=15, padx=10)

        tk.Label(card_form, text="Teléfono o Email:", font=("Helvetica", 16, "bold"), bg=BG_DARK_HEADER, fg=TEXT_DARK_WHITE).grid(row=1, column=0, sticky="w", pady=15, padx=10)
        self.entry_contacto = tk.Entry(card_form, font=("Helvetica", 16), width=22, bg="#FFFFFF", fg="#000000")
        self.entry_contacto.grid(row=1, column=1, pady=15, padx=10)

        btn_submit = tk.Button(
            center_frame, 
            text="VER MI RESULTADO 🍫", 
            font=("Helvetica", 20, "bold"), 
            bg=GOLD_ACCENT, 
            fg=BG_DARK_CARD, 
            padx=30, 
            pady=12, 
            bd=0,
            cursor="hand2",
            command=self.procesar_registro
        )
        btn_submit.pack(pady=20)

    def procesar_registro(self):
        nombre = self.entry_nombre.get().strip()
        contacto = self.entry_contacto.get().strip()

        if not nombre or not contacto:
            messagebox.showwarning("Atención", "Por favor completa tu nombre y contacto.")
            return

        perfil = self.calcular_perfil()
        self.guardar_en_bd(nombre, contacto, perfil)
        self.mostrar_resultado(perfil)

    def calcular_perfil(self):
        if self.score <= 50:
            return "Hershey's Lover"
        elif self.score <= 75:
            return "Chocolate Expert"
        elif self.score <= 95:
            return "Chocolate Addict"
        else:
            return "Nivel Hershey's: ¡Maestro!"

    def guardar_en_bd(self, nombre, contacto, perfil):
        archivo = "leads_hersheys_farmatodo.csv"
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        headers = ["Fecha", "Nombre", "Contacto", "Perfil", "Puntuacion", "Pref_Sabor", "Frase_Momento"]
        row = [
            fecha, 
            nombre, 
            contacto, 
            perfil, 
            self.score,
            self.respuestas_usuario.get("pregunta_1", ""),
            self.respuestas_usuario.get("pregunta_4", "")
        ]

        try:
            with open(archivo, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow(headers)
                writer.writerow(row)
        except Exception as e:
            print(f"Error al guardar datos: {e}")

    # ==========================================
    # PANTALLA 4: RESULTADO FINAL (Con Fondo 1)
    # ==========================================
    def mostrar_resultado(self, perfil):
        self.limpiar_pantalla()

        main_canvas = tk.Canvas(self.root, highlightthickness=0)
        main_canvas.pack(fill="both", expand=True)

        if self.bg_fondo1_tk:
            main_canvas.create_image(0, 0, image=self.bg_fondo1_tk, anchor="nw")
        else:
            main_canvas.configure(bg=BG_DARK_CARD)

        center_frame = tk.Frame(main_canvas, bg=BG_DARK_CARD)
        main_canvas.create_window(
            self.root.winfo_screenwidth() // 2,
            self.root.winfo_screenheight() // 2,
            window=center_frame,
            anchor="center"
        )

        lbl_congrats = tk.Label(
            center_frame, 
            text="✨ ¡FELICIDADES, HEMOS EVALUADO TU PERFIL! ✨", 
            font=("Helvetica", 18, "bold"), 
            bg=BG_DARK_CARD, 
            fg=GOLD_LIGHT
        )
        lbl_congrats.pack(pady=(10, 10))

        card_res = tk.Frame(
            center_frame, 
            bg=BG_DARK_HEADER, 
            padx=45, 
            pady=30, 
            highlightbackground=GOLD_ACCENT, 
            highlightthickness=3
        )
        card_res.pack(pady=15, padx=30)

        lbl_sub = tk.Label(
            card_res, 
            text="TU NIVEL HERSHEY'S ES:", 
            font=("Helvetica", 15, "bold"), 
            bg=BG_DARK_HEADER, 
            fg=TEXT_DARK_SILVER
        )
        lbl_sub.pack(pady=(0, 10))

        glow_box = tk.Frame(
            card_res, 
            bg=CHOCO_BASE, 
            padx=35, 
            pady=20, 
            highlightbackground=GOLD_ACCENT, 
            highlightthickness=2
        )
        glow_box.pack(pady=10)

        lbl_perfil = tk.Label(
            glow_box, 
            text=f"🍫 {perfil} 🍫", 
            font=("Helvetica", 38, "bold"), 
            bg=CHOCO_BASE, 
            fg=GOLD_ACCENT
        )
        lbl_perfil.pack()

        lbl_msg = tk.Label(
            card_res, 
            text="¡Gracias por participar!\nDemuestra tu pasión buscando tu chocolate favorito.", 
            font=("Helvetica", 17), 
            bg=BG_DARK_HEADER, 
            fg=TEXT_DARK_WHITE, 
            justify="center"
        )
        lbl_msg.pack(pady=(20, 5))

        btn_restart = tk.Button(
            center_frame, 
            text="FINALIZAR / NUEVO JUEGO", 
            font=("Helvetica", 20, "bold"), 
            bg=GOLD_ACCENT, 
            fg=BG_DARK_CARD, 
            activebackground="#E6C200", 
            padx=35,
            pady=12,
            bd=0,
            cursor="hand2",
            command=self.mostrar_pantalla_inicio
        )
        btn_restart.pack(pady=20)

    def limpiar_pantalla(self):
        if self.timer_transicion:
            self.root.after_cancel(self.timer_transicion)
            self.timer_transicion = None

        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = HersheysTriviaApp(root)
    root.mainloop()