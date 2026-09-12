import time

# Banco de preguntas sobre la historia de Hershey's
PREGUNTAS_HERSHEY = [
    {
        "pregunta": "¿En qué año se lanzó la primera barra de chocolate con leche de Hershey's?",
        "opciones": {
            "a": "1893",
            "b": "1900",
            "c": "1912",
            "d": "1925"
        },
        "respuesta": "b",
        "explicacion": "Milton Hershey desarrolló su fórmula secreta de leche condensada y lanzó la barra original en 1900."
    },
    {
        "pregunta": "¿Por qué recibieron su nombre los famosos chocolates 'Hershey's Kisses'?",
        "opciones": {
            "a": "Por el sonido 'kss' que hacía la máquina al dejarlos caer sobre la cinta",
            "b": "Porque Milton Hershey se los regala a su esposa con un beso",
            "c": "Porque la forma se parece a un labio al sonreír",
            "d": "Fue una idea de una agencia de publicidad en 1950"
        },
        "respuesta": "a",
        "explicacion": "Se les llamó Kisses por el característico sonido y movimiento que hacía la boquilla al depositar la gota de chocolate."
    },
    {
        "pregunta": "¿Qué producto vendía Milton Hershey con gran éxito antes de dedicarse al chocolate?",
        "opciones": {
            "a": "Galletas de avena",
            "b": "Caramelos de leche (toffees)",
            "c": "Helados de vainilla",
            "d": "Refrescos de cola"
        },
        "respuesta": "b",
        "explicacion": "Fundó la 'Lancaster Caramel Company' tras fracasar en dos confiterías previas en Filadelfia y Nueva York."
    },
    {
        "pregunta": "¿De qué trágico evento histórico se salvó Milton Hershey a última hora en 1912?",
        "opciones": {
            "a": "Un gran incendio en Filadelfia",
            "b": "El hundimiento del Titanic",
            "c": "El terremoto de San Francisco",
            "d": "Un descarrilamiento de tren"
        },
        "respuesta": "b",
        "explicacion": "Tenía billetes reservados para el viaje inaugural del Titanic, pero canceló a última hora por una reunión urgente en la fábrica."
    },
    {
        "pregunta": "¿Quién es el dueño mayoritario de la empresa Hershey's en la actualidad?",
        "opciones": {
            "a": "Una corporación multinacional suiza",
            "b": "Los descendientes directos de Milton Hershey",
            "c": "El fideicomiso de la Escuela Milton Hershey para niños huérfanos",
            "d": "El gobierno del estado de Pensilvania"
        },
        "respuesta": "c",
        "explicacion": "Al no tener hijos, Milton donó toda su fortuna y acciones a la escuela internado para niños de bajos recursos que fundó junto a su esposa."
    },
    {
        "pregunta": "¿Cómo se llamó el chocolate resistente al calor creado por Hershey para las tropas en la Segunda Guerra Mundial?",
        "opciones": {
            "a": "Ración D",
            "b": "Barra M1",
            "c": "Victory Bar",
            "d": "Pack Táctico"
        },
        "respuesta": "a",
        "explicacion": "Fabricaron más de 3,000 millones de barras de la 'Ración D' para el ejército estadounidense, diseñadas para no derretirse en el frente."
    },
    {
        "pregunta": "¿En qué año se introdujo la icónica plumilla de papel que sobresale del envoltorio de los Kisses?",
        "opciones": {
            "a": "1907",
            "b": "1921",
            "c": "1940",
            "d": "1965"
        },
        "respuesta": "b",
        "explicacion": "En 1921 se añadió la tira de papel sobresaliente para garantizar que el cliente supiera que era un Kiss original de Hershey."
    }
]

def limpiar_pantalla():
    print("\n" + "=" * 60 + "\n")

def ejecutar_trivia():
    puntuacion = 0
    total_preguntas = len(PREGUNTAS_HERSHEY)
    
    print("🍫 ¡BIENVENIDO A LA TRIVIA HISTÓRICA DE HERSHEY'S! 🍫")
    print("Demuestra tus conocimientos sobre el imperio del chocolate.\n")
    time.sleep(1)

    for idx, item in enumerate(PREGUNTAS_HERSHEY, start=1):
        limpiar_pantalla()
        print(f"Pregunta {idx} de {total_preguntas}:")
        print(f"📌 {item['pregunta']}\n")
        
        for clave, opcion in item["opciones"].items():
            print(f"  [{clave.upper()}] {opcion}")
            
        print()
        while True:
            respuesta = input("👉 Elige tu respuesta (A/B/C/D): ").strip().lower()
            if respuesta in item["opciones"]:
                break
            print("❌ Opción inválida. Ingresa A, B, C o D.")

        if respuesta == item["respuesta"]:
            print("\n🎉 ¡CORRECTO!")
            puntuacion += 1
        else:
            resp_correcta = item["respuesta"].upper()
            print(f"\n❌ INCORRECTO. La respuesta correcta era [{resp_correcta}].")

        print(f"💡 Dato curioso: {item['explicacion']}")
        time.sleep(2)

    # Pantalla final de resultados
    limpiar_pantalla()
    print("🏆 RESULTADOS FINALES 🏆")
    print(f"Puntuación obtenida: {puntuacion} / {total_preguntas}")
    
    porcentaje = (puntuacion / total_preguntas) * 100
    if porcentaje == 100:
        print("🥇 ¡Nivel Maestro Chocolatero! Conociste cada detalle de la historia.")
    elif porcentaje >= 70:
        print("🥈 ¡Excelente! Eres un verdadero fanático de Hershey's.")
    elif porcentaje >= 40:
        print("🥉 ¡Buen intento! Conoces lo básico sobre el imperio del chocolate.")
    else:
        print("🍫 ¡Aún hay mucho por aprender! Vuelve a intentar para descubrir más secretos.")

if __name__ == "__main__":
    ejecutar_trivia()