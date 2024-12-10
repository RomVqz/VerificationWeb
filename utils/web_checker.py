import requests
import os
import re
from urllib.parse import urlparse

# Reutilizar conexiones HTTP
session = requests.Session()

def simplify_error(error_message):
    """
    Simplifica los mensajes de error a un formato legible.
    """
    if "Max retries exceeded" in error_message:
        return "Error: Max retries exceeded"
    if "Failed to resolve" in error_message:
        return "Error: DNS resolution failed"
    if "LocationParseError" in error_message:
        return "Error: Invalid URL format"
    return "Error: Request failed"

def fix_url(url):
    """
    Corrige URLs añadiendo esquema (http/https), eliminando puntos iniciales, y añadiendo 'www.' si es necesario.
    """
    # Eliminar punto inicial si existe
    if url.startswith("."):
        url = url.lstrip(".")
    # Añadir esquema si falta
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"http://{url}"
    # Añadir www si no está presente
    if not url.startswith("http://www.") and not url.startswith("https://www."):
        url = url.replace("http://", "http://www.", 1).replace("https://", "https://www.", 1)
    return url

def is_valid_url(url):
    """
    Valida si una URL tiene un formato correcto.
    """
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)  # Debe tener esquema y dominio
    except Exception:
        return False

def sanitize_filename(filename):
    """
    Limpia el nombre del archivo reemplazando caracteres no válidos.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def check_url_status(url):
    """
    Verifica el estado de una URL sin descargar contenido.
    """
    url = fix_url(url)  # Corrige la URL
    if not is_valid_url(url):
        return "Error: Invalid URL format"

    try:
        response = session.head(url, timeout=2, allow_redirects=True)  # Usamos HEAD para no descargar contenido
        return response.status_code  # Devuelve el código de estado HTTP
    except requests.RequestException as e:
        return simplify_error(str(e))  # Devuelve un mensaje de error simplificado

def check_and_download(url, output_dir="output/html_pages"):
    """
    Verifica el estado de una URL y descarga el HTML si está activa.
    """
    url = fix_url(url)  # Corregir la URL
    if not is_valid_url(url):
        return "Error: Invalid URL format"

    try:
        response = session.get(url, timeout=2)  # Reutilizar sesión
        status_code = response.status_code

        if status_code == 200:
            os.makedirs(output_dir, exist_ok=True)
            sanitized_name = sanitize_filename(url.replace('http://', '').replace('https://', '').replace('/', '_'))
            file_name = os.path.join(output_dir, f"{sanitized_name}.html")
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(response.text)

        return status_code  # Código HTTP
    except requests.RequestException as e:
        return simplify_error(str(e))  # Simplificar mensaje de error

# Ejemplo de uso
urls = [
    ".jualrumahpontianak.com",
    "example.com",
    "https://valid-url.com"
]

# Verificar y descargar si está activa
for url in urls:
    status = check_url_status(url)
    print(f"URL: {url}, Estado: {status}")

    if status == 200:  # Descarga solo si está activa
        download_status = check_and_download(url)
        print(f"Descarga completada: {download_status}")
