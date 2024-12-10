from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from utils.csv_handler import read_and_prepare_csv, save_csv
from utils.web_checker import check_and_download
import pandas as pd
import os

# Crear instancia de FastAPI
app = FastAPI()

# Directorios para guardar resultados
OUTPUT_CSV = "output/urls_updated.csv"
HTML_DIR = "output/html_pages"


@app.get("/")
async def root():
    """
    Endpoint raíz de la API.
    """
    return {
        "message": "Bienvenido a la API para verificación de URLs.",
        "endpoints": [
            {"method": "POST", "path": "/upload-csv/", "description": "Subir y procesar un archivo CSV."},
            {"method": "GET", "path": "/download-updated-csv/", "description": "Descargar el CSV actualizado."},
            {"method": "GET", "path": "/get-html-files/", "description": "Listar los archivos HTML descargados."},
        ],
    }


@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    """
    Endpoint para subir un archivo CSV, verificar URLs y actualizar el estado.
    """
    # Leer el archivo subido
    content = await file.read()
    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as temp_file:
        temp_file.write(content)

    # Procesar el archivo CSV
    df = read_and_prepare_csv(temp_path)
    results = []

    for index, row in df.iterrows():
        url = row["url"]
        print(f"Verificando: {url}")
        status = check_and_download(url, output_dir=HTML_DIR)
        df.at[index, "status"] = status
        results.append({"url": url, "status": status})

    # Guardar el archivo actualizado
    save_csv(df, OUTPUT_CSV)
    os.remove(temp_path)  # Limpiar archivo temporal

    return {"message": "CSV procesado exitosamente", "results": results}


@app.get("/download-updated-csv/")
async def download_updated_csv():
    """
    Endpoint para descargar el CSV actualizado con los estados de las URLs.
    """
    if os.path.exists(OUTPUT_CSV):
        return JSONResponse(
            content={
                "message": "Archivo CSV actualizado disponible.",
                "file_path": OUTPUT_CSV,
            }
        )
    else:
        return JSONResponse(
            status_code=404, content={"message": "Archivo actualizado no encontrado."}
        )


@app.get("/get-html-files/")
async def list_html_files():
    """
    Endpoint para listar los archivos HTML descargados.
    """
    if not os.path.exists(HTML_DIR):
        return JSONResponse(
            status_code=404, content={"message": "No se encontraron archivos HTML."}
        )

    html_files = os.listdir(HTML_DIR)
    return {"message": "Archivos HTML descargados:", "files": html_files}
