import pandas as pd
import os

# Definir la carpeta donde se encuentran los archivos unificados por cada año
folder_path = 'ruta_a_tu_carpeta/'  # Ruta de los archivos unificados

# Lista de los años ya unificados (estos deben existir como 'proyecto_unificado_2014.csv', etc.)
years = [2014, 2015, 2016, 2017, 2018, 2019, 2020]  # Lista de los años a procesar

# Inicializamos un DataFrame vacío para almacenar el resumen final
summary_data = pd.DataFrame()

# Iteramos sobre los archivos consolidados por cada año
for year in years:
    # Leemos el archivo unificado de ese año
    file_path = os.path.join(folder_path, f'proyecto_unificado_{year}.csv')
    
    if os.path.exists(file_path):
        # Cargamos el archivo en un DataFrame
        data_year = pd.read_csv(file_path)
        
        # Iteramos sobre cada estudiante en el año (suponiendo que la columna 'ID_estudiante' identifica a cada estudiante)
        for student in data_year['ID_estudiante'].unique():
            student_data = data_year[data_year['ID_estudiante'] == student]

            # Obtenemos el grado por cada año
            student_summary = {}
            student_summary['ID_estudiante'] = student
            
            # Asumimos que tienes una columna 'Grado' y que el año está en la columna 'Año'
            student_summary[f'Grado_{year}'] = student_data['Grado'].values[0] if not student_data.empty else None

            # Verificamos si el estudiante completó la trayectoria correctamente
            trajectory_completed = True

            # Validamos la trayectoria educativa desde 2014 hasta el año actual
            for i in range(2014, year+1):  # Compara de 2014 hasta el año actual
                if f'Grado_{i}' not in student_summary:
                    student_summary[f'Grado_{i}'] = None  # Si no tiene información para ese año, ponemos None
                else:
                    # Comprobamos que la secuencia de grados sea la esperada
                    expected_grade = i - 2014
                    if student_summary[f'Grado_{i}'] != expected_grade:
                        trajectory_completed = False
                        break
            
            # Añadimos la columna de trayectoria en el resumen
            student_summary['Trayectoria'] = 'Eficaz' if trajectory_completed else 'No culminó'

            # Agregamos los datos del estudiante al resumen
            summary_data = summary_data.append(student_summary, ignore_index=True)
        
        print(f"Procesado el archivo de {year}")

    else:
        print(f"El archivo {file_path} no existe.")

# Guardamos el archivo resumen con la trayectoria de los estudiantes
summary_data.to_csv('resumen_trayectorias.csv', index=False)

print("Resumen de trayectorias generado exitosamente.")