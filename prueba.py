
import csv
from datetime import datetime
import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Requiere: pip install pillow
import pygame
import qrcode
import requests
from datetime import datetime
import requests

# 1. Coloca tu URL pública de Easypanel (asegúrate de que sea la correcta)
URL_BASE = "https://trivia-hershey-trivia-app.dy6ey0.easypanel.host"

# 2. Datos simulados
datos_prueba = {
    "nombre": "Prueba Mary",
    "email": "test@ejemplo.com",
    "telefono": "+123456789",
    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

print("Enviando petición a Express...")

try:
    respuesta = requests.post(
        f"{URL_BASE}/api/registro",
        json=datos_prueba,
        headers={"Content-Type": "application/json"},
        timeout=10,
    )

    print(f"--> Código de Estado HTTP: {respuesta.status_code}")
    print(f"--> Respuesta del Servidor: {respuesta.text}")

except Exception as e:
    print(f"--> Error de conexión: {e}")