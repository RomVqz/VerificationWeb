# URL Checker and API Integration

## Descripción

Este proyecto proporciona una solución integral para verificar URLs a partir de un archivo CSV, actualizar su estado y descargar el contenido HTML si las URLs están activas. La solución incluye una aplicación de línea de comandos y una API basada en **FastAPI** que permite interactuar con las funcionalidades de verificación y descarga.

---


---

## Funcionalidades

### 1. **Aplicación Principal (`main.py`)**
- **Entrada:** Archivo CSV con una columna `url`.
- **Procesamiento:**
  - Divide el archivo CSV en bloques.
  - Procesa las URLs en paralelo usando hilos.
  - Verifica el estado de las URLs.
  - Guarda los resultados en múltiples archivos CSV.
- **Salida:** Archivos CSV procesados en la carpeta `output_chunks`.

### 2. **API REST (`api.py`)**
- **Endpoints:**
  - `/`: Información sobre los endpoints disponibles.
  - `POST /upload-csv/`: Subir y procesar un archivo CSV.
  - `GET /download-updated-csv/`: Descargar el archivo CSV actualizado.
  - `GET /get-html-files/`: Listar los archivos HTML descargados.

### 3. **Módulos Utilitarios**
#### - **`csv_handler.py`**
  - Leer y procesar archivos CSV en bloques.
  - Guardar resultados en un archivo CSV.

#### - **`web_checker.py`**
  - Validar el formato de URLs.
  - Verificar el estado de URLs (códigos HTTP).
  - Descargar contenido HTML de URLs activas.

---

## Requisitos

1. **Entorno de desarrollo:**
   - Python 3.9 o superior.
   - Sistema operativo compatible (Windows, macOS o Linux).

2. **Librerías necesarias:**
   Instalar las dependencias con:
   ```bash
   pip install -r requirements.txt

---

# URL Checker and API Integration

## Uso

### 1. **Ejecución de la Aplicación Principal**
Ejecuta la aplicación principal con:
 
python main.py

- El archivo de entrada se configura en main.py en la variable input_csv.
- Los resultados se guardan en la carpeta output_chunks.

---
## Ejecución de la API

Inicia el servidor con:

uvicorn api:app --reload

- La API estará disponible en: http://127.0.0.1:8000.

---

## Resultados

CSV actualizado:

1. **Incluye el estado HTTP** (200, 404, etc.) de cada URL.
Archivos HTML descargados:

2. Almacena las páginas activas en la carpeta output/html_pages.

---

# Créditos
- Autor: **José Guillermo Mottú Vázquez**
- Contacto: **mottu.guillermo@gmail.com**

