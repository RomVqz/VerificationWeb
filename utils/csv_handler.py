import pandas as pd

def read_and_prepare_csv(file_path, chunk_size):
    """
    Lee el archivo CSV en bloques y agrega una columna para el estado si no existe.
    """
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        if 'status' not in chunk.columns:
            chunk['status'] = 'Pendiente'
        yield chunk

def save_csv_in_chunks(df, file_path, mode='a', header=False):
    """
    Guarda un bloque del DataFrame en un archivo CSV.
    """
    df.to_csv(file_path, mode=mode, index=False, header=header)
