import pandas as pd
import os

# Define la carpeta donde están tus archivos por año
folder_path = 'ruta_a_tu_carpeta/'

# Lista de meses en orden de diciembre a enero
months = ['diciembre', 'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre']

# Lista de años para procesar (ajústala según tus necesidades)
years = [2014, 2015, 2016, 2017, 2018, 2019, 2020,2021,2022,2023,2024,2025]  # Lista de años a unificar

# Iteramos sobre los años
for year in years:
    # Inicializamos un DataFrame vacío para almacenar los datos unificados de cada año
    unified_data = pd.DataFrame()

    # Iteramos sobre los meses en orden de diciembre a enero
    for month in months:
        # Leemos el archivo correspondiente a cada mes
        file_path = os.path.join(folder_path, f'{year}_{month}.csv')  # Suponiendo que tus archivos tienen el formato '2014_diciembre.csv'

        # Verificamos si el archivo existe antes de intentar leerlo
        if os.path.exists(file_path):
            # Cargamos el archivo en un DataFrame
            df = pd.read_csv(file_path)

            # Añadimos la columna del mes
            df['Mes'] = month

            # Unimos el DataFrame del mes con el DataFrame unificado
            unified_data = pd.concat([unified_data, df], ignore_index=True)
        else:
            print(f"El archivo {file_path} no existe.")

    # Evitamos duplicados por 'ID_estudiante' manteniendo solo el último registro de cada estudiante
    unified_data = unified_data.sort_values(by=['ID_estudiante', 'Mes'], ascending=[True, False])  # Ordenamos de diciembre a enero
    unified_data = unified_data.drop_duplicates(subset=['ID_estudiante'], keep='first')  # Mantiene el primer registro para cada estudiante

    # Guardamos el archivo unificado para cada año
    unified_data.to_csv(f'proyecto_unificado_{year}.csv', index=False)

    print(f'Archivo unificado para el año {year} guardado correctamente.')