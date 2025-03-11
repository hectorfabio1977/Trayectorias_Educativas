import pandas as pd
import glob
import os
import re


# Define la ruta donde deseas guardar los archivos
ruta_destino = r'C:\Users\hlond\OneDrive\Escritorio\Trayectorias_Educativas\Consolidados_Años'

# Paso 1: Cargar los archivos mensuales con ';' O (, ) como separador
# ** es un patrón que coincide con todos los directorios y subdirectorios.
# El parámetro recursive=True le indica a glob que busque de forma recursiva en todas las subcarpetas dentro de la carpeta principal.
archivos = glob.glob(r'C:\Users\hlond\OneDrive\Escritorio\Trayectorias_Educativas\Matriculas_por_Años\**\*.csv', recursive=True)

# Ordenar los archivos en orden descendente por nombre (para asegurarse que noviembre O EL ULTIMO MES DEL AÑO esté primero)
archivos = sorted(archivos, reverse=True)
dataframes = {}

# Expresión regular para extraer mes y año del nombre del archivo
# Modificada para capturar los nombres con formato Mes_Año (ejemplo: Abril_2020)
patron = r'([a-zA-Z]+)_(\d{4})'

for archivo in archivos:
    # Leer archivo CSV
    df = pd.read_csv(archivo, sep=';', na_filter=False, low_memory=False)
    
    # Eliminar espacios en blanco de los nombres de las columnas
    df.columns = df.columns.str.strip()

    # Agregar columna 'estado_nuevo' con el nombre del archivo (sin ruta completa)
    #df['estado_nuevo'] = os.path.basename(archivo)  # Obtiene solo el nombre del archivo
    
    # Extraer el mes y año del nombre del archivo usando la expresión regular
    match = re.search(patron, os.path.basename(archivo))
    if match:
        mes = match.group(1)  # El primer grupo es el mes
        año = match.group(2)  # El segundo grupo es el año

         # Asignar solo mes y año a la columna 'estado_nuevo'
        df['estado_nuevo'] = f"{mes}_{año}"

    else:
        print(f"Advertencia: El archivo {archivo} no tiene un formato de mes_año válido.")
        df['estado_nuevo'] = "Formato_invalido"  # Si no se encuentra un mes/año, asignar un valor por defecto
        continue  # Si no se puede extraer el mes/año, se ignora el archivo

    # Verificar si 'Id' existe después de limpiar espacios
    if 'PER_ID' not in df.columns:
        print(f"Advertencia: El archivo {archivo} no tiene la columna 'Id' incluso después de limpiar espacios.")
    else:
        # Si el año no existe en el diccionario, lo inicializamos
        if año not in dataframes:
            dataframes[año] = []
        
        # Agregar el DataFrame a la lista correspondiente al año
        dataframes[año].append(df)

# Paso 2: Consolidar y guardar los DataFrames por año
for año, dfs in dataframes.items():
    # Combinar todos los DataFrames del mismo año
    df_consolidado = pd.concat(dfs, ignore_index=True)
    
    # Eliminar duplicados usando 'Id'
    df_consolidado = df_consolidado.drop_duplicates(subset=['PER_ID'])
    
    # Guardar el DataFrame consolidado por año en un nuevo archivo CSV
    nombre_archivo = os.path.join(ruta_destino, f"{año}.csv")
    #nombre_archivo = f"matricula_consolidada_{año}.csv"
    df_consolidado.to_csv(nombre_archivo, sep=';', index=False)
    print(f"Archivo consolidado para el año {año} guardado como {nombre_archivo}.")
