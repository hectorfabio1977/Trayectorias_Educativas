import pandas as pd
import os

# Define la carpeta base donde están las carpetas por año
folder_path = 'ruta_a_tu_carpeta/'

# Archivo de control para los archivos procesados
control_file = 'archivos_procesados.txt'

# Lista de meses en orden de diciembre a enero
months = ['diciembre', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
          'julio', 'agosto', 'septiembre', 'octubre', 'noviembre']

# Lista de años para procesar
years = list(range(2014, 2026))  # Ajusta según necesidad

# Cargar archivos procesados previamente
if os.path.exists(control_file):
    with open(control_file, 'r') as f:
        archivos_procesados = set(f.read().splitlines())
else:
    archivos_procesados = set()

# Iteramos sobre los años
for year in years:
    year_folder = os.path.join(folder_path, str(year))

    # Verificamos si la carpeta del año existe
    if not os.path.exists(year_folder):
        continue  # Si no existe la carpeta del año, pasa al siguiente

    unified_data = pd.DataFrame()  # DataFrame para consolidar el año

    for month in months:
        file_path = os.path.join(year_folder, f'{year}_{month}.csv')

        # Si el archivo no existe o ya fue procesado, lo saltamos
        if not os.path.exists(file_path) or file_path in archivos_procesados:
            continue

        # Cargamos el archivo en un DataFrame
        df = pd.read_csv(file_path, sep=';')  # Ajusta el separador si es necesario
        df['Mes'] = month  # Agregar columna del mes

        # Unimos el DataFrame del mes con el DataFrame unificado
        unified_data = pd.concat([unified_data, df], ignore_index=True)

        # Agregar el archivo al registro de procesados
        archivos_procesados.add(file_path)

    # Si hay datos, los procesamos y guardamos
    if not unified_data.empty:
        unified_data = unified_data.sort_values(by=['ID_estudiante', 'Mes'], ascending=[True, False])
        unified_data = unified_data.drop_duplicates(subset=['ID_estudiante'], keep='first')
        output_file = os.path.join(folder_path, f'proyecto_unificado_{year}.csv')
        unified_data.to_csv(output_file, index=False, sep=';')  # Ajusta el separador si es necesario
        print(f'Archivo unificado para el año {year} guardado correctamente.')

# Guardamos el archivo de control con los archivos ya procesados
with open(control_file, 'w') as f:
    f.write("\n".join(archivos_procesados))

print("Proceso completado.")