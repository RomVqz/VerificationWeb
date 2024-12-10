import os
import time
from utils.csv_handler import read_and_prepare_csv, save_csv_in_chunks
from utils.web_checker import check_url_status


def process_chunk(df_chunk, max_threads=48):
    """
    Procesa un bloque de URLs en paralelo usando hilos.
    """
    from concurrent.futures import ThreadPoolExecutor

    # Procesar URLs en paralelo
    with ThreadPoolExecutor(max_threads) as executor:
        results = executor.map(check_url_status, df_chunk['url'])

    # Asignar resultados a la columna 'status'
    df_chunk['status'] = list(results)
    return df_chunk


def main():
    # Ruta del archivo CSV
    input_csv = "C:/Users/mottu/Documents/INEGI/API/Partes/parte_11.csv"
    output_folder = "output_chunks"  # Carpeta para los CSV generados

    # Crear carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)

    # Configuración
    chunk_size = 10000  # Tamaño de los bloques
    max_threads = 48  # Número de hilos

    # Medir el tiempo de ejecución
    start_time = time.time()

    print("Leyendo archivo CSV y procesando en bloques...")
    for chunk_index, df_chunk in enumerate(read_and_prepare_csv(input_csv, chunk_size=chunk_size)):
        print(f"Procesando bloque {chunk_index + 1}...")

        # Procesar el bloque en paralelo
        df_chunk = process_chunk(df_chunk, max_threads=max_threads)

        # Generar un nombre único para cada archivo CSV
        chunk_file_name = os.path.join(output_folder, f"urls_chunk_{chunk_index + 1}_{int(time.time())}.csv")

        # Guardar los resultados del bloque en un archivo separado
        save_csv_in_chunks(df_chunk, chunk_file_name, mode='w', header=True)
        print(f"Bloque {chunk_index + 1} guardado en {chunk_file_name}")

    # Calcular el tiempo total
    end_time = time.time()
    print(f"Proceso completado. Archivos guardados en la carpeta {output_folder}")
    print(f"Tiempo total: {end_time - start_time:.2f} segundos")


if __name__ == "__main__":
    main()
