import pandas as pd
import os

# Definir la carpeta donde se encuentran los archivos unificados por cada año
folder_path = r'C:\Users\hlond\OneDrive\Escritorio\Trayectorias_Educativas\Consolidados_Años'

# Lista de los años ya unificados (estos deben existir como 'Matricula_Consolidada_2014.csv', etc.)
years = [2016, 2025]  # Lista de los años a procesar

# Inicializamos un DataFrame vacío para almacenar el resumen final
summary_data = pd.DataFrame()

# Iteramos sobre los archivos consolidados por cada año
for year in years:
    # Leemos el archivo unificado de ese año
    file_path = os.path.join(folder_path, f'Matricula_Consolidada_{year}.csv')

    if os.path.exists(file_path):
        try:
            # Cargamos el archivo en un DataFrame, especificando que el delimitador es el punto y coma (;)
            data_year = pd.read_csv(file_path, sep=';', engine='python', quotechar='"')
            
            # Verificamos si las columnas 'PER_ID' y 'GRADO' existen
            if 'PER_ID' in data_year.columns and 'GRADO' in data_year.columns:
                # Seleccionamos solo las columnas necesarias, incluida 'INSTITUCION' y 'JORNADA'
                columns_to_select = ['PER_ID', 'GRADO', 'INSTITUCION', 'JORNADA'] if 'INSTITUCION' in data_year.columns and 'JORNADA' in data_year.columns else ['PER_ID', 'GRADO']
                data_year = data_year[columns_to_select]

                # Renombramos la columna 'GRADO' para que sea el año correspondiente (usando el año como string)
                data_year.rename(columns={'GRADO': str(year)}, inplace=True)

                # Hacemos un merge con el DataFrame de resumen si ya existe uno
                if summary_data.empty:
                    summary_data = data_year
                else:
                    summary_data = pd.merge(summary_data, data_year, on='PER_ID', how='outer')

                print(f"Procesado el archivo de {year}")
            else:
                print(f"El archivo {file_path} no contiene las columnas necesarias.")
        except pd.errors.ParserError as e:
            print(f"Error al leer el archivo {file_path}: {e}")
    else:
        print(f"El archivo {file_path} no existe.")

# Validación de la trayectoria educativa para cada estudiante
for student in summary_data['PER_ID'].unique():
    student_data = summary_data[summary_data['PER_ID'] == student]
    
    trajectory_completed = False  # Inicializamos la trayectoria como no completada
    
    # Verificamos que el estudiante haya comenzado en grado 0 (2016) y terminado en grado 11 (2025 o 2026)
    if '2016' in student_data.columns and '2025' in student_data.columns:
        grade_2016 = student_data['2016'].values[0] if not student_data['2016'].isnull().values[0] else None
        grade_2025 = student_data['2025'].values[0] if not student_data['2025'].isnull().values[0] else None
        
        # Si tiene grado 0 en 2016 y grado 11 en 2025 o 2026, la trayectoria es "Eficaz"
        if grade_2016 == 0 and grade_2025 == 11:
            trajectory_completed = True
    
    # Añadimos la validación de la trayectoria
    summary_data.loc[summary_data['PER_ID'] == student, 'Trayectoria'] = 'Eficaz' if trajectory_completed else 'No culminó'

    # Agregamos el colegio inicial, colegio final y jornada
    colegio_inicial = None
    colegio_final = None
    jornada_inicial = None
    jornada_final = None
    
    # Verificamos si las columnas de los colegios y jornadas existen y tomamos los valores correspondientes
    if '2016' in student_data.columns and 'INSTITUCION' in student_data.columns:
        colegio_inicial = student_data[student_data['PER_ID'] == student]['INSTITUCION'].iloc[0] if not student_data[student_data['PER_ID'] == student].empty else None
        jornada_inicial = student_data[student_data['PER_ID'] == student]['JORNADA'].iloc[0] if not student_data[student_data['PER_ID'] == student].empty else None
    
    if '2025' in student_data.columns and 'INSTITUCION' in student_data.columns:
        colegio_final = student_data[student_data['PER_ID'] == student]['INSTITUCION'].iloc[-1] if not student_data[student_data['PER_ID'] == student].empty else None
        jornada_final = student_data[student_data['PER_ID'] == student]['JORNADA'].iloc[-1] if not student_data[student_data['PER_ID'] == student].empty else None
    
    # Asignamos los valores al DataFrame resumen
    summary_data.loc[summary_data['PER_ID'] == student, 'Colegio Inicial'] = colegio_inicial
    summary_data.loc[summary_data['PER_ID'] == student, 'Colegio Final'] = colegio_final
    summary_data.loc[summary_data['PER_ID'] == student, 'Jornada Inicial'] = jornada_inicial
    summary_data.loc[summary_data['PER_ID'] == student, 'Jornada Final'] = jornada_final

# Guardamos el archivo resumen con la trayectoria de los estudiantes
output_file = 'resumen_trayectorias.csv'
summary_data.to_csv(output_file, index=False)

print(f"Resumen de trayectorias generado exitosamente. Archivo guardado como {output_file}.")
