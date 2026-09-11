import csv
from datetime import datetime
import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Requiere: pip install pillow
import pygame


def obtener_ruta_recurso(ruta_relativa):
    """Obtiene la ruta absoluta para recursos, compatible con PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, ruta_relativa)


# ==========================================
# PALETAS DE COLORES SEPARADAS
# ==========================================

# --- PALETA 1: TEMA CHOCOLATE OSCURO (Inicio, Registro, Resultado) ---
BG_DARK_CARD = "#1C0D08"  # Tarjeta Marrón Oscuro
BG_DARK_HEADER = "#120704"  # Encabezado súper oscuro
TEXT_DARK_WHITE = "#FFFFFF"  # Texto blanco
TEXT_DARK_SILVER = "#CBD5E1"  # Texto secundario claro
GOLD_ACCENT = "#FFD700"  # Dorado Hershey's
GOLD_LIGHT = "#FFF099"

# --- PALETA 2: TEMA COOKIES 'N' CREAM (Pantalla de Preguntas) ---
BG_LIGHT_CARD = "#1A0C0E"  # Fondo de tarjeta oscuro
BG_LIGHT_HEADER = "#110608"  # Encabezado oscuro dentro de la tarjeta
KISSES_BLUE = "#0066CC"  # Azul eléctrico icónico
TEXT_LIGHT_WHITE = "#FFFFFF"  # Texto sobre tarjeta oscura
TEXT_LIGHT_SILVER = "#E2E8F0"

# --- ESTILO BOTONES CHOCOLATE ---
CHOCO_BASE = "#3D1C12"
CHOCO_HIGHLIGHT = "#5A2B1C"
CHOCO_DARK = "#24100A"


class HersheysTriviaApp:

    def __init__(self, root):
        self.root = root

        # Cargar Logo
        self.logo_tk = None
        self.cargar_logo()

        # Vincular la tecla Escape para cerrar la aplicación
        self.root.bind("<Escape>", lambda event: self.salir_juego())

        # Inicializar el sistema de audio de pygame
        pygame.mixer.init()
        # Construyes la ruta apuntando a la carpeta 'audio'
        ruta_audio = os.path.join("audio", "sound1.mp3")

        try:
            self.sfx_wap = pygame.mixer.Sound(ruta_audio)
            self.sfx_wap.set_volume(0.8)
        except Exception as e:
            print(f"Error al cargar el audio desde la carpeta: {e}")
            self.sfx_wap = None
        

        self.ruta_musica_inicio = obtener_ruta_recurso(
            os.path.join("audio", "musica_inicio.mp3")
        )
        self.ruta_musica_juego = obtener_ruta_recurso(
            os.path.join("audio", "musica_juego.mp3")
        )
        self.ruta_musica_registro = obtener_ruta_recurso(
            os.path.join("audio", "musica_registro.mp3")
        )
        self.ruta_musica_resultado = obtener_ruta_recurso(
            os.path.join("audio", "musica_resultado.mp3")
        )

        self.root.title("Trivia Hershey's Lover")

        # Teclas de acceso rápido
        self.root.bind("<Up>", self.subir_volumen)
        self.root.bind("<Down>", self.bajar_volumen)
        self.root.bind("<Control-q>", lambda event: self.root.destroy())

        # Pantalla completa
        self.root.attributes("-fullscreen", True)

        # Cache de imágenes de fondo
        self.bg_fondo1_tk = None
        self.bg_fondo2_tk = None
        self.bg_fondo3_tk = None

        self.cargar_fondos()

        self.root.geometry("1024x768")
        self.root.configure(bg=BG_DARK_CARD)

        self.score = 0
        self.respuestas_usuario = {}
        self.pregunta_actual = 0

        self.opcion_seleccionada = None
        self.botones_canvas = []
        self.timer_transicion = None

        # --- TIMERS DE INACTIVIDAD/AUTO-REINICIO ---
        self.timer_registro_id = None
        self.tiempo_restante_registro = 15

        self.timer_resultado_id = None
        self.tiempo_restante_resultado = 10

        self.ruta_banner_fijo = "banner.png"
        self.banner_img_tk = None
        self.imagenes_cache = {}

        # Cargar la imagen del botón de chocolate
        try:
            ruta_btn = obtener_ruta_recurso("BotonesH.jpg")
            if os.path.exists(ruta_btn):
                self.img_boton_raw = Image.open(ruta_btn)
            else:
                self.img_boton_raw = None
        except Exception as e:
            print(f"Error al cargar BotonesH.jpg: {e}")
            self.img_boton_raw = None

        self.imagenes_botones = []

        # Datos de Preguntas
        self.preguntas = [
            {
                "id": 1,
                "pregunta": "1. Tu chocolate ideal es...",
                "opciones": [
                    ("1. Cremoso", 10, "images/cream.jpg"),
                    ("2. Intenso", 15, "images/dark.jpg"),
                    ("3. Con toppings", 12, "images/cookies.jpg"),
                    ("4. ¡Todos!", 20, "images/variedad.jpg"),
                ],
            },
            {
                "id": 2,
                "pregunta": "2. ¿Cuál reconoces con los ojos cerrados?",
                "opciones": [
                    ("1. Hershey's Milk Chocolate", 15, "images/milk.jpg"),
                    (
                        "2. Hershey's Cookies 'n' Cream",
                        20,
                        "images/cookies.jpg",
                    ),
                    ("3. Hershey's Special Dark", 15, "images/dark.jpg"),
                    (
                        "4. Todos por su olor característico",
                        25,
                        "images/variedad.jpg",
                    ),
                ],
            },
            {
                "id": 3,
                "pregunta": "3. ¿Cuál de estos SÍ es un producto Hershey’s?",
                "opciones": [
                    ("1. Kisses Classic", 10, "images/kisses.jpg"),
                    ("2. Pelon Pelo Rico", 15, "images/pelon.jpg"),
                    (
                        "3. Reese's Peanut Butter Cups",
                        20,
                        "images/reeses.jpg",
                    ),
                    (
                        "4. ¡Todos pertenecen a la familia Hershey's!",
                        25,
                        "images/variedad.jpg",
                    ),
                ],
            },
            {
                "id": 4,
                "pregunta": (
                    "4. Completa la frase: 'Chocolate + __ = momento"
                    " perfecto'"
                ),
                "opciones": [
                    ("1. Una película / serie", 15, "images/milk.jpg"),
                    ("2. Un café / merienda", 15, "images/dark.jpg"),
                    ("3. Compartir con amigos", 20, "images/conamigos.jpg"),
                    ("4. Un antojo nocturno", 10, "images/cookies.jpg"),
                ],
            },
            {
                "id": 5,
                "pregunta": (
                    "5. Pregunta final: ¿Cuánto crees que sabes de Hershey’s?"
                ),
                "opciones": [
                    ("1. Lo básico, ¡pero me encanta!", 10, "images/milk.jpg"),
                    ("2. Sé bastante, soy fan", 15, "images/dark.jpg"),
                    ("3. ¡Soy un experto total!", 20, "images/kisses.jpg"),
                    (
                        "4. Vivo para comer chocolate",
                        25,
                        "images/variedad.jpg",
                    ),
                ],
            },
        ]

        self.mostrar_pantalla_inicio()

    def subir_volumen(self, event=None):
        vol_actual = pygame.mixer.music.get_volume()
        nuevo_vol = min(1.0, vol_actual + 0.1)
        pygame.mixer.music.set_volume(nuevo_vol)

    def bajar_volumen(self, event=None):
        vol_actual = pygame.mixer.music.get_volume()
        nuevo_vol = max(0.0, vol_actual - 0.1)
        pygame.mixer.music.set_volume(nuevo_vol)

    def cancelar_timer_registro(self):
        if self.timer_registro_id is not None:
            try:
                self.root.after_cancel(self.timer_registro_id)
            except Exception:
                pass
            self.timer_registro_id = None

    def cancelar_timer_resultado(self):
        if self.timer_resultado_id is not None:
            try:
                self.root.after_cancel(self.timer_resultado_id)
            except Exception:
                pass
            self.timer_resultado_id = None

    def cargar_logo(self):
        self.logo_blanco_tk = None
        self.logo_marron_tk = None

        ruta_logo_blanco = obtener_ruta_recurso(
            os.path.join("images", "LogoBlanco.png")
        )
        ruta_logo_marron = obtener_ruta_recurso(
            os.path.join("images", "LogoMarron.png")
        )

        if os.path.exists(ruta_logo_blanco):
            try:
                img_b = Image.open(ruta_logo_blanco).resize(
                    (300, 120), Image.Resampling.LANCZOS
                )
                self.logo_blanco_tk = ImageTk.PhotoImage(img_b)
            except Exception as e:
                print(f"Error al cargar LogoBlanco.png: {e}")

        if os.path.exists(ruta_logo_marron):
            try:
                img_m = Image.open(ruta_logo_marron).resize(
                    (300, 120), Image.Resampling.LANCZOS
                )
                self.logo_marron_tk = ImageTk.PhotoImage(img_m)
            except Exception as e:
                print(f"Error al cargar LogoMarron.png: {e}")

    def crear_rectangulo_redondeado(
        self, canvas, x1, y1, x2, y2, radio=25, **kwargs
    ):
        puntos = [
            x1 + radio,
            y1,
            x1 + radio,
            y1,
            x2 - radio,
            y1,
            x2 - radio,
            y1,
            x2,
            y1,
            x2,
            y1 + radio,
            x2,
            y1 + radio,
            x2,
            y2 - radio,
            x2,
            y2 - radio,
            x2,
            y2,
            x2 - radio,
            y2,
            x2 - radio,
            y2,
            x1 + radio,
            y2,
            x1 + radio,
            y2,
            x1,
            y2,
            x1,
            y2 - radio,
            x1,
            y2 - radio,
            x1,
            y1 + radio,
            x1,
            y1 + radio,
            x1,
            y1,
        ]
        return canvas.create_polygon(puntos, smooth=True, **kwargs)

    def limpiar_pantalla(self):
        self.cancelar_timer_registro()
        self.cancelar_timer_resultado()

        if self.timer_transicion:
            try:
                self.root.after_cancel(self.timer_transicion)
            except Exception:
                pass
            self.timer_transicion = None

        for widget in self.root.winfo_children():
            widget.destroy()

        for tecla in [
            "1",
            "2",
            "3",
            "4",
            "<KP_1>",
            "<KP_2>",
            "<KP_3>",
            "<KP_4>",
        ]:
            try:
                self.root.unbind(tecla)
            except Exception:
                pass

    def cargar_fondos(self):
        ancho = self.root.winfo_screenwidth()
        alto = self.root.winfo_screenheight()

        ruta1 = obtener_ruta_recurso("images/fondo_app.jpeg")
        if os.path.exists(ruta1):
            try:
                img1 = Image.open(ruta1).resize(
                    (ancho, alto), Image.Resampling.LANCZOS
                )
                self.bg_fondo1_tk = ImageTk.PhotoImage(img1)
            except Exception as e:
                print(f"Error al cargar fondo 1: {e}")

        ruta2 = obtener_ruta_recurso("images/fondo2.jpeg")
        if os.path.exists(ruta2):
            try:
                img2 = Image.open(ruta2).resize(
                    (ancho, alto), Image.Resampling.LANCZOS
                )
                self.bg_fondo2_tk = ImageTk.PhotoImage(img2)
            except Exception as e:
                print(f"Error al cargar fondo 2: {e}")

        ruta3 = obtener_ruta_recurso("images/fondo3.jpeg")
        if os.path.exists(ruta3):
            try:
                img3 = Image.open(ruta3).resize(
                    (ancho, alto), Image.Resampling.LANCZOS
                )
                self.bg_fondo3_tk = ImageTk.PhotoImage(img3)
            except Exception as e:
                print(f"Error al cargar fondo 3: {e}")

    # --- AUDIO ---
    def reproducir_musica_inicio(self):
        if os.path.exists(self.ruta_musica_inicio):
            try:
                pygame.mixer.music.load(self.ruta_musica_inicio)
                pygame.mixer.music.set_volume(0.8)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"Error audio inicio: {e}")

    def reproducir_musica_juego(self):
        if os.path.exists(self.ruta_musica_juego):
            try:
                pygame.mixer.music.fadeout(500)
                pygame.mixer.music.load(self.ruta_musica_juego)
                pygame.mixer.music.set_volume(0.18)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"Error audio juego: {e}")

    def reproducir_musica_registro(self):
        if os.path.exists(self.ruta_musica_registro):
            try:
                pygame.mixer.music.fadeout(500)
                pygame.mixer.music.load(self.ruta_musica_registro)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"Error audio registro: {e}")

    def reproducir_musica_resultado(self):
        if os.path.exists(self.ruta_musica_resultado):
            try:
                pygame.mixer.music.fadeout(300)
                pygame.mixer.music.load(self.ruta_musica_resultado)
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play(-1)
            except Exception as e:
                print(f"Error audio resultado: {e}")

    def detener_musica(self, msec=1000):
        try:
            pygame.mixer.music.fadeout(msec)
        except Exception as e:
            print(f"Error al detener música: {e}")

    def reproducir_sfx_boton(self):
        if self.sonido_boton:
            try:
                self.sonido_boton.play()
            except Exception as e:
                print(f"Error SFX: {e}")

    def salir_juego(self):
        self.detener_musica(0)
        self.root.destroy()

    # ==========================================
    # PANTALLA 1: INICIO
    # ==========================================
    def mostrar_pantalla_inicio(self):
        self.limpiar_pantalla()
        self.reproducir_musica_inicio()

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        centro_x = ancho_pantalla // 2

        main_canvas = tk.Canvas(self.root, highlightthickness=0)
        main_canvas.pack(fill="both", expand=True)

        if self.bg_fondo1_tk:
            main_canvas.create_image(0, 0, image=self.bg_fondo1_tk, anchor="nw")
        else:
            main_canvas.configure(bg=BG_DARK_CARD)

        main_canvas.create_text(
            centro_x,
            180,
            text="TRIVIA HERSHEY'S LOVER",
            font=("Helvetica", 16, "bold"),
            fill=TEXT_DARK_SILVER,
            anchor="center",
        )

        main_canvas.create_text(
            centro_x,
            260,
            text="¿QUÉ TAN HERSHEY'S\nLOVER ERES?",
            font=("Helvetica", 38, "bold"),
            fill=GOLD_ACCENT,
            justify="center",
            anchor="center",
        )

        main_canvas.create_text(
            centro_x,
            370,
            text=(
                "Responde 5 preguntas rápidas | Regístrate\nDescubre tu nivel |"
                " Gana premios exclusivos"
            ),
            font=("Helvetica", 18),
            fill=TEXT_DARK_WHITE,
            justify="center",
            anchor="center",
        )

        width_btn = 360
        height_btn = 65
        x1_btn = centro_x - (width_btn // 2)
        y1_btn = 430
        x2_btn = centro_x + (width_btn // 2)
        y2_btn = y1_btn + height_btn

        btn_shadow = self.crear_rectangulo_redondeado(
            main_canvas,
            x1_btn + 4,
            y1_btn + 4,
            x2_btn + 4,
            y2_btn + 4,
            radio=20,
            fill="#120704",
            outline="",
        )
        btn_rect = self.crear_rectangulo_redondeado(
            main_canvas,
            x1_btn,
            y1_btn,
            x2_btn,
            y2_btn,
            radio=20,
            fill=GOLD_ACCENT,
            outline="#FFFFFF",
            width=2,
        )

        btn_text = main_canvas.create_text(
            centro_x,
            y1_btn + (height_btn // 2),
            text="¡EMPEZAR TRIVIA!",
            font=("Helvetica", 20, "bold"),
            fill=BG_DARK_CARD,
            anchor="center",
        )

        def on_click_start(e=None):
            #self.reproducir_sfx_boton()
            self.iniciar_trivia()

        for element_id in [btn_shadow, btn_rect, btn_text]:
            main_canvas.tag_bind(element_id, "<Button-1>", on_click_start)
            main_canvas.tag_bind(
                element_id,
                "<Enter>",
                lambda e: main_canvas.config(cursor="hand2"),
            )
            main_canvas.tag_bind(
                element_id, "<Leave>", lambda e: main_canvas.config(cursor="")
            )

        for tecla in [
            "1",
            "2",
            "3",
            "4",
            "<KP_1>",
            "<KP_2>",
            "<KP_3>",
            "<KP_4>",
        ]:
            self.root.bind(tecla, lambda e: self.iniciar_trivia())

        if hasattr(self, "logo_blanco_tk") and self.logo_blanco_tk:
            main_canvas.create_image(
                centro_x,
                alto_pantalla - 100,
                image=self.logo_blanco_tk,
                anchor="center",
            )

    def iniciar_trivia(self):
        self.reproducir_musica_juego()
        self.score = 0
        self.pregunta_actual = 0
        self.respuestas_usuario = {}
        self.mostrar_pregunta()

    def reproducir_sfx_boton(self):
        if hasattr(self, "sfx_wap") and self.sfx_wap:
            self.sfx_wap.play()
            
    # ==========================================
    # PANTALLA 2: PREGUNTAS
    # ==========================================
    def mostrar_pregunta(self):
        self.limpiar_pantalla()
        self.opcion_seleccionada = None
        self.botones_canvas = []
        self.imagenes_botones.clear()

        q_data = self.preguntas[self.pregunta_actual]
        ancho_pantalla = self.root.winfo_screenwidth()
        centro_x = ancho_pantalla // 2

        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)

        if self.bg_fondo2_tk:
            self.main_canvas.create_image(
                0, 0, image=self.bg_fondo2_tk, anchor="nw"
            )
        else:
            self.main_canvas.configure(bg="#F4EBE1")

        if hasattr(self, "logo_marron_tk") and self.logo_marron_tk:
            self.main_canvas.create_image(
                centro_x, 90, image=self.logo_marron_tk, anchor="center"
            )
        else:
            self.main_canvas.create_text(
                centro_x,
                90,
                text="HERSHEY'S",
                font=("Helvetica", 16, "bold"),
                fill=CHOCO_BASE,
                anchor="center",
            )

        self.main_canvas.create_text(
            centro_x,
            210,
            text=q_data["pregunta"],
            font=("Helvetica", 24, "bold"),
            fill="#24100A",
            width=750,
            justify="center",
            anchor="center",
        )

        y_inicial = 290
        espaciado = 85
        btn_ancho = 550
        btn_alto = 70

        for i, (texto, puntos, foto_path) in enumerate(q_data["opciones"]):
            pos_y = y_inicial + (i * espaciado)
            texto_completo = f"{texto}"

            if hasattr(self, "img_boton_raw") and self.img_boton_raw:
                img_resized = self.img_boton_raw.resize(
                    (btn_ancho, btn_alto), Image.Resampling.LANCZOS
                )
                tk_img = ImageTk.PhotoImage(img_resized)
                self.imagenes_botones.append(tk_img)

                btn_img_id = self.main_canvas.create_image(
                    centro_x, pos_y, image=tk_img, anchor="center"
                )
                # Guardamos como tipo imagen
                self.botones_canvas.append({"tipo": "image", "id": btn_img_id})
            else:
                btn_img_id = self.main_canvas.create_rectangle(
                    centro_x - (btn_ancho // 2),
                    pos_y - (btn_alto // 2),
                    centro_x + (btn_ancho // 2),
                    pos_y + (btn_alto // 2),
                    fill="#3d1c11",
                    outline="#ffffff",
                    width=2,
                )

                # Guardamos como tipo rectángulo
                self.botones_canvas.append({"tipo": "rectangle", "id": btn_img_id})

            btn_txt_id = self.main_canvas.create_text(
                centro_x,
                pos_y,
                text=texto_completo,
                font=("Helvetica", 14, "bold"),
                fill="#FFFFFF",
                anchor="center",
                width=btn_ancho - 40,
            )

            def hacer_click(e, idx=i):
                self.seleccionar_opcion_por_indice(idx)

            self.main_canvas.tag_bind(btn_img_id, "<Button-1>", hacer_click)
            self.main_canvas.tag_bind(btn_txt_id, "<Button-1>", hacer_click)

        self.root.bind(
            "1", lambda e: self.seleccionar_opcion_por_indice(0, True)
        )
        self.root.bind(
            "2", lambda e: self.seleccionar_opcion_por_indice(1, True)
        )
        self.root.bind(
            "3", lambda e: self.seleccionar_opcion_por_indice(2, True)
        )
        self.root.bind(
            "4", lambda e: self.seleccionar_opcion_por_indice(3, True)
        )

        self.root.bind(
            "<KP_1>", lambda e: self.seleccionar_opcion_por_indice(0, True)
        )
        self.root.bind(
            "<KP_2>", lambda e: self.seleccionar_opcion_por_indice(1, True)
        )
        self.root.bind(
            "<KP_3>", lambda e: self.seleccionar_opcion_por_indice(2, True)
        )
        self.root.bind(
            "<KP_4>", lambda e: self.seleccionar_opcion_por_indice(3, True)
        )

    def seleccionar_opcion_por_indice(self, index, via_teclado=False):
        # 1. Reproducir el efecto de sonido inmediatamente (mouse o teclado)
        self.reproducir_sfx_boton()

        # 2. Desvincular clics del ratón de inmediato para evitar clics múltiples durante la espera
        if hasattr(self, "main_canvas") and self.main_canvas:
            self.main_canvas.unbind_all("<Button-1>")

        q_data = self.preguntas[self.pregunta_actual]
        opciones = q_data["opciones"]

        if 0 <= index < len(opciones):
            # ==========================================
            # HIGHLIGHT / DESTACADO DEL BOTÓN SELECCIONADO
            # ==========================================
            if index < len(self.botones_canvas):
                btn_info = self.botones_canvas[index]
                btn_id = btn_info["id"]

                if btn_info["tipo"] == "rectangle":
                    # Si es rectángulo dibujado: Cambiar relleno a un tono más claro/dorado y borde más grueso
                    self.main_canvas.itemconfig(btn_id, fill="#6b301c", outline="#FFD700", width=4)
                
                elif btn_info["tipo"] == "image":
                    # Si es una imagen personalizada: Añadir rectángulo dorado justo detrás
                    bbox = self.main_canvas.bbox(btn_id)
                    if bbox:
                        highlight_bg = self.main_canvas.create_rectangle(
                            bbox[0] - 4, bbox[1] - 4, bbox[2] + 4, bbox[3] + 4,
                            outline="#FFD700", width=4
                        )
                        self.main_canvas.tag_lower(highlight_bg, btn_id)
            # ==========================================

            opcion = opciones[index]

            if isinstance(opcion, (tuple, list)):
                elem1, elem2 = opcion[0], opcion[1]
                if (
                    str(elem1).replace("-", "").isdigit() is False
                    and str(elem2).replace("-", "").isdigit() is True
                ):
                    texto, puntos_raw = elem1, elem2
                else:
                    puntos_raw, texto = elem1, elem2
            else:
                puntos_raw, texto = 0, str(opcion)

            try:
                puntos = int(puntos_raw)
            except (ValueError, TypeError):
                puntos = 0

            self.score += puntos
            self.respuestas_usuario[f"pregunta_{self.pregunta_actual + 1}"] = texto

            self.desvincular_teclas_pregunta()
            self.root.after(900, self.siguiente_pregunta)

    def desvincular_teclas_pregunta(self):
        for tecla in [
            "1",
            "2",
            "3",
            "4",
            "<KP_1>",
            "<KP_2>",
            "<KP_3>",
            "<KP_4>",
        ]:
            try:
                self.root.unbind(tecla)
            except Exception:
                pass

    def siguiente_pregunta(self):
        self.pregunta_actual += 1

        if self.pregunta_actual < len(self.preguntas):
            self.mostrar_pregunta()
        else:
            self.detener_musica(500)
            self.mostrar_formulario_registro()

    # ==========================================
    # PANTALLA 3: REGISTRO
    # ==========================================
    # ==========================================
    # PANTALLA 3: REGISTRO
    # ==========================================
    def mostrar_formulario_registro(self):
        self.limpiar_pantalla()
        self.reproducir_musica_registro()

        self.tiempo_restante_registro = 15

        # CORRECCIÓN: Guardar en self.main_canvas en lugar de una variable local
        self.main_canvas = tk.Canvas(self.root, highlightthickness=0)
        self.main_canvas.pack(fill="both", expand=True)

        # Misma estructura de validación para el fondo 3
        if hasattr(self, "bg_fondo3_tk") and self.bg_fondo3_tk:
            self.main_canvas.create_image(
                0, 0, image=self.bg_fondo3_tk, anchor="nw"
            )
        else:
            self.main_canvas.configure(bg="#F4EBE1")  # Color fallback de seguridad

        # Montamos el frame del formulario sobre self.main_canvas
        center_frame = tk.Frame(self.main_canvas, bg=BG_DARK_CARD)
        self.main_canvas.create_window(
            self.root.winfo_screenwidth() // 2,
            self.root.winfo_screenheight() // 2,
            window=center_frame,
            anchor="center",
        )

        title = tk.Label(
            center_frame,
            text="¡CASI LISTO!",
            font=("Helvetica", 32, "bold"),
            bg=BG_DARK_CARD,
            fg=GOLD_ACCENT,
        )
        title.pack(pady=(10, 5))

        subtitle = tk.Label(
            center_frame,
            text=(
                "Ingresa tus datos para revelar tu nivel Hershey's y"
                " participar:"
            ),
            font=("Helvetica", 17),
            bg=BG_DARK_CARD,
            fg=TEXT_DARK_WHITE,
        )
        subtitle.pack(pady=5)

        self.lbl_timer_registro = tk.Label(
            center_frame,
            text=f"⏱️ Tiempo restante: {self.tiempo_restante_registro}s",
            font=("Helvetica", 14, "bold"),
            bg=BG_DARK_CARD,
            fg="#FFD166",
        )
        self.lbl_timer_registro.pack(pady=(0, 10))

        card_form = tk.Frame(
            center_frame,
            bg=BG_DARK_HEADER,
            padx=35,
            pady=30,
            highlightbackground=GOLD_ACCENT,
            highlightthickness=2,
        )
        card_form.pack(pady=10)

        tk.Label(
            card_form,
            text="Nombre Completo:",
            font=("Helvetica", 16, "bold"),
            bg=BG_DARK_HEADER,
            fg=TEXT_DARK_WHITE,
        ).grid(row=0, column=0, sticky="w", pady=15, padx=10)
        self.entry_nombre = tk.Entry(
            card_form, font=("Helvetica", 16), width=22, bg="#FFFFFF", fg="#000000"
        )
        self.entry_nombre.grid(row=0, column=1, pady=15, padx=10)

        tk.Label(
            card_form,
            text="Teléfono o Email:",
            font=("Helvetica", 16, "bold"),
            bg=BG_DARK_HEADER,
            fg=TEXT_DARK_WHITE,
        ).grid(row=1, column=0, sticky="w", pady=15, padx=10)
        self.entry_contacto = tk.Entry(
            card_form, font=("Helvetica", 16), width=22, bg="#FFFFFF", fg="#000000"
        )
        self.entry_contacto.grid(row=1, column=1, pady=15, padx=10)

        self.entry_nombre.bind("<Key>", self.reiniciar_timer_registro)
        self.entry_contacto.bind("<Key>", self.reiniciar_timer_registro)

        btn_frame = tk.Frame(center_frame, bg=BG_DARK_CARD)
        btn_frame.pack(pady=15)

        btn_submit = tk.Button(
            btn_frame,
            text="VER MI RESULTADO 🍫",
            font=("Helvetica", 18, "bold"),
            bg=GOLD_ACCENT,
            fg=BG_DARK_CARD,
            padx=25,
            pady=10,
            bd=0,
            cursor="hand2",
            command=self.procesar_registro,
        )
        btn_submit.pack(side="left", padx=10)

        btn_omitir = tk.Button(
            btn_frame,
            text="OMITIR E INICIO 🏠",
            font=("Helvetica", 14, "bold"),
            bg="#3D1C12",
            fg=TEXT_DARK_SILVER,
            padx=15,
            pady=10,
            bd=0,
            cursor="hand2",
            command=self.mostrar_pantalla_inicio,
        )
        btn_omitir.pack(side="left", padx=10)

        self.actualizar_timer_registro()

    def reiniciar_timer_registro(self, event=None):
        self.tiempo_restante_registro = 15
        if (
            hasattr(self, "lbl_timer_registro")
            and self.lbl_timer_registro.winfo_exists()
        ):
            self.lbl_timer_registro.config(
                text=f"⏱️ Tiempo restante: {self.tiempo_restante_registro}s"
            )

    def actualizar_timer_registro(self):
        if self.tiempo_restante_registro > 0:
            self.tiempo_restante_registro -= 1
            if (
                hasattr(self, "lbl_timer_registro")
                and self.lbl_timer_registro.winfo_exists()
            ):
                self.lbl_timer_registro.config(
                    text=f"⏱️ Tiempo restante: {self.tiempo_restante_registro}s"
                )
            self.timer_registro_id = self.root.after(
                1000, self.actualizar_timer_registro
            )
        else:
            self.cancelar_timer_registro()
            self.mostrar_pantalla_inicio()

    def procesar_registro(self):
        self.reproducir_sfx_boton()
        nombre = self.entry_nombre.get().strip()
        contacto = self.entry_contacto.get().strip()

        if not nombre or not contacto:
            messagebox.showwarning(
                "Atención", "Por favor completa tu nombre y contacto."
            )
            return

        self.cancelar_timer_registro()
        perfil = self.calcular_perfil()
        self.guardar_en_bd(nombre, contacto, perfil)
        self.mostrar_resultado(perfil)

    def calcular_perfil(self):
        if self.score <= 50:
            return "Hershey's Lover"
        elif self.score <= 75:
            return "Chocolate Expert"
        elif self.score <= 100:
            return "Choco Master"
        else:
            return "Hershey's Legend"

    def guardar_en_bd(self, nombre, contacto, perfil):
        archivo_csv = "resultados_trivia.csv"
        existe = os.path.exists(archivo_csv)

        try:
            with open(archivo_csv, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                if not existe:
                    writer.writerow([
                        "Fecha_Hora",
                        "Nombre",
                        "Contacto",
                        "Puntaje",
                        "Perfil",
                        "Respuestas",
                    ])
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    nombre,
                    contacto,
                    self.score,
                    perfil,
                    str(self.respuestas_usuario),
                ])
        except Exception as e:
            print(f"Error al guardar datos en CSV: {e}")

    # ==========================================
    # PANTALLA 4: RESULTADO
    # ==========================================
    def mostrar_resultado(self, perfil):
        self.limpiar_pantalla()
        self.reproducir_musica_resultado()

        self.tiempo_restante_resultado = 15

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        centro_x = ancho_pantalla // 2

        main_canvas = tk.Canvas(self.root, highlightthickness=0)
        main_canvas.pack(fill="both", expand=True)

        if self.bg_fondo1_tk:
            main_canvas.create_image(0, 0, image=self.bg_fondo1_tk, anchor="nw")
        else:
            main_canvas.configure(bg=BG_DARK_CARD)

        # 1. Título Superior
        main_canvas.create_text(
            centro_x,
            160,
            text="¡TU RESULTADO!",
            font=("Helvetica", 24, "bold"),
            fill=TEXT_DARK_SILVER,
            anchor="center",
        )

        # 2. Perfil Destacado
        main_canvas.create_text(
            centro_x,
            230,
            text=f"PERFIL: {perfil.upper()}",
            font=("Helvetica", 36, "bold"),
            fill=GOLD_ACCENT,
            anchor="center",
        )

        # 3. Puntuación Total
        main_canvas.create_text(
            centro_x,
            300,
            text=f"Puntuación Total: {self.score} Puntos",
            font=("Helvetica", 22, "bold"),
            fill=TEXT_DARK_WHITE,
            anchor="center",
        )

        # 4. Mensaje del Perfil
        mensaje_perfil = (
            "¡Eres un verdadero fanático del chocolate!\nPasa por el stand"
            " para reclamar tu experiencia exclusiva Hershey's."
        )
        main_canvas.create_text(
            centro_x,
            370,
            text=mensaje_perfil,
            font=("Helvetica", 16),
            fill=TEXT_DARK_SILVER,
            justify="center",
            anchor="center",
        )

        # 5. Timer de Reinicio
        self.lbl_timer_id = main_canvas.create_text(
            centro_x,
            440,
            text=f"⏱️ Reiniciando en {self.tiempo_restante_resultado} segundos...",
            font=("Helvetica", 14, "bold"),
            fill="#FFD166",
            anchor="center",
        )

        # 6. Botón Visual (Volver al inicio)
        width_btn = 360
        height_btn = 60
        x1_btn = centro_x - (width_btn // 2)
        y1_btn = 490
        x2_btn = centro_x + (width_btn // 2)
        y2_btn = y1_btn + height_btn

        btn_shadow = self.crear_rectangulo_redondeado(
            main_canvas,
            x1_btn + 4,
            y1_btn + 4,
            x2_btn + 4,
            y2_btn + 4,
            radio=20,
            fill="#120704",
            outline="",
        )
        btn_rect = self.crear_rectangulo_redondeado(
            main_canvas,
            x1_btn,
            y1_btn,
            x2_btn,
            y2_btn,
            radio=20,
            fill=GOLD_ACCENT,
            outline="#FFFFFF",
            width=2,
        )

        btn_text = main_canvas.create_text(
            centro_x,
            y1_btn + (height_btn // 2),
            text="PRESIONA CUALQUIER BOTÓN 🏠",
            font=("Helvetica", 16, "bold"),
            fill=BG_DARK_CARD,
            anchor="center",
        )

        # --- FUNCIÓN DE REINICIO ---
        def reiniciar_trivia(e=None):
            # Desvinculamos los eventos para evitar ejecuciones dobles
            self.root.unbind("<Key>")
            main_canvas.unbind("<Button-1>")
            
            #self.reproducir_sfx_boton()
            self.cancelar_timer_resultado()
            self.mostrar_pantalla_inicio()

        # 1. Detectar CUALQUIER tecla del teclado / keypad
        self.root.bind("<Key>", reiniciar_trivia)

        # 2. Detectar CUALQUIER clic del ratón en la pantalla
        # main_canvas.bind("<Button-1>", reiniciar_trivia)

        # 3. Mantener el efecto visual del cursor al pasar sobre el botón
        for element_id in [btn_shadow, btn_rect, btn_text]:
            main_canvas.tag_bind(
                element_id,
                "<Enter>",
                lambda e: main_canvas.config(cursor="hand2"),
            )
            main_canvas.tag_bind(
                element_id, "<Leave>", lambda e: main_canvas.config(cursor="")
            )

        self.main_canvas = main_canvas
        self.actualizar_timer_resultado()

    def actualizar_timer_resultado(self):
        if self.tiempo_restante_resultado > 0:
            self.tiempo_restante_resultado -= 1
            if hasattr(self, "lbl_timer_id") and hasattr(self, "main_canvas"):
                self.main_canvas.itemconfig(
                    self.lbl_timer_id,
                    text=f"⏱️ Reiniciando en {self.tiempo_restante_resultado} segundos...",
                )
            self.timer_resultado_id = self.root.after(
                1000, self.actualizar_timer_resultado
            )
        else:
            self.cancelar_timer_resultado()
            self.mostrar_pantalla_inicio()

    def actualizar_timer_resultado(self):
        if self.tiempo_restante_resultado > 0:
            self.tiempo_restante_resultado -= 1
            if (
                hasattr(self, "lbl_timer_resultado")
                and self.lbl_timer_resultado.winfo_exists()
            ):
                self.lbl_timer_resultado.config(
                    text=(
                        "⏱️ Reiniciando en"
                        f" {self.tiempo_restante_resultado} segundos..."
                    )
                )
            self.timer_resultado_id = self.root.after(
                1000, self.actualizar_timer_resultado
            )
        else:
            self.cancelar_timer_resultado()
            self.mostrar_pantalla_inicio()


if __name__ == "__main__":
    root = tk.Tk()
    app = HersheysTriviaApp(root)
    root.mainloop()