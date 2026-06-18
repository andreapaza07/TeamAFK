# =============================================
# MÓDULO DE ANÁLISIS - TEAM AFK
# Contiene funciones para procesar y analizar datos de streams
# Utiliza pandas para hacer el análisis más sencillo
# =============================================

import pandas as pd


# Funciones basicas
def cargar_datos_en_dataframe(fechas, streamers, viewers, likes, regalos, horas):
    """
    Crea un DataFrame de pandas a partir de las listas de datos
    Esta es la base para todos los análisis
    """
    data = {
        'Fecha': fechas,
        'Streamer': streamers,
        'Viewers': viewers,
        'Likes': likes,
        'Regalos (S/.)': regalos,
        'Horas Transmitidas': horas
    }
    df = pd.DataFrame(data)
    return df

def generar_estadisticas_generales(df):
    """
    Calcula estadísticas basicas (suma, promedio, etc.) usando pandas
    Retorna un diccionario con los resultados
    """
    #empty verifica si el DataFrame está vacío
    if df.empty:
        return {"error": "No hay datos para analizar"}

    estadisticas = {
        #mean() calcula el promedio de la columna especificada
        "total_streams": len(df),
        "promedio_viewers": df['Viewers'].mean(),
        "promedio_likes": df['Likes'].mean(),
        "promedio_regalos": df['Regalos (S/.)'].mean(),
        "promedio_horas": df['Horas Transmitidas'].mean(),
        "total_regalos": df['Regalos (S/.)'].sum()
    }
    return estadisticas

def encontrar_mejor_stream(df):
    """
    Encuentra el stream con más viewers
    Retorna una serie con los datos del mejor stream
    """
    if df.empty:
        return None
    
    #idmax() encuentra el índice del valor máximo en la columna 'Viewers'
    #loc se usa para obtener la fila correspondiente a ese índice
    indice_mejor = df['Viewers'].idxmax()
    mejor_stream = df.loc[indice_mejor]
    return mejor_stream

def analizar_streamers(df):
    """
    Realiza un análisis de los streamers
    Encuentra al streamer con más viewers, likes y regalos
    Retorna un diccionario con los resultados
    """
    if df.empty:
        return {"error": "No hay datos para analizar"}

    #groupby permite agrupar los datos por streamer y luego sumar las métricas
    #agg() permite aplicar funciones de agregación a las columnas seleccionadas
    #'sum' suma los valores de cada columna para cada streamer
    #reset_index() convierte el índice del DataFrame en una columna normal
    resumen_streamers = df.groupby('Streamer').agg({
        'Viewers': 'sum',
        'Likes': 'sum',
        'Regalos (S/.)': 'sum'
    }).reset_index()

    mejor_por_viewers = resumen_streamers.loc[resumen_streamers['Viewers'].idxmax()]
    mejor_por_likes = resumen_streamers.loc[resumen_streamers['Likes'].idxmax()]
    mejor_por_regalos = resumen_streamers.loc[resumen_streamers['Regalos (S/.)'].idxmax()]

    return {
        #to_dict() convierte la serie en un diccionario para facilitar su uso
        "mejor_por_viewers": mejor_por_viewers.to_dict(),
        "mejor_por_likes": mejor_por_likes.to_dict(),
        "mejor_por_regalos": mejor_por_regalos.to_dict()
    }

def guardar_reporte(df, nombre_archivo="reporte_streams.csv"):
    """
    Guarda el DataFrame completo en un archivo CSV
    """
    #to_csv() guarda el DataFrame en un archivo CSV
    #index=False evita que se guarde el índice del DataFrame en el archivo
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print(f"Reporte guardado como '{nombre_archivo}'")


# Funciones de alerta mejoradas
def generar_alertas_basicas(df):
    """
    Genera alertas simples basadas en el rendimiento
    Detecta streams con bajo rendimiento, pocos likes o pocos regalos
    """
    if df.empty:
        return ["No hay datos para generar alertas"]
    
    alertas = []
    
    #1. Alerta: Streams con menos de 40 viewers
    streams_bajos_viewers = df[df['Viewers'] < 40]
    if not streams_bajos_viewers.empty:
        #_, row recorre sobre cada fila del DataFrame filtrado
        #iterrows() devuelve un índice y una serie para cada fila
        for _, row in streams_bajos_viewers.iterrows():
            alertas.append(f"BAJO RENDIMIENTO: Stream del {row['Fecha']} con solo {row['Viewers']} viewers.")
    
    #2. Alerta: Streams con menos de 50 likes (poca interacción)
    streams_bajos_likes = df[df['Likes'] < 50]
    if not streams_bajos_likes.empty:
        for _, row in streams_bajos_likes.iterrows():
            alertas.append(f"POCA INTERACCIÓN: Stream del {row['Fecha']} con solo {row['Likes']} likes.")
    
    #3. Alerta: Streams que duraron mucho pero tuvieron pocos viewers
    #copy() se usa para evitar advertencias de pandas sobre la modificación de un DataFrame filtrado
    df_copy = df.copy()
    df_copy['Viewers_por_hora'] = df_copy['Viewers'] / df_copy['Horas Transmitidas']
    streams_ineficientes = df_copy[df_copy['Viewers_por_hora'] < 50]
    
    if not streams_ineficientes.empty:
        for _, row in streams_ineficientes.iterrows():
            alertas.append(f"STREAM INEFICIENTE: {row['Fecha']} - {row['Viewers_por_hora']:.1f} viewers/hora (duró {row['Horas Transmitidas']} horas)")
    
    #4. Alerta: Streams con 0 regalos
    streams_sin_regalos = df[df['Regalos (S/.)'] == 0]
    if not streams_sin_regalos.empty:
        for _, row in streams_sin_regalos.iterrows():
            alertas.append(f"SIN REGALOS: Stream del {row['Fecha']} no recibió regalos.")
    
    #Si no hay alertas mostramos mensaje positivo
    if not alertas:
        alertas.append("Todo en orden! No se detectaron problemas")
    return alertas


# Funciones de analisis de rendimiento por hora

def calcular_rendimiento_por_hora(df):
    """
    Calcula el rendimiento de cada stream en relación a las horas transmitidas
    Retorna un DataFrame con las métricas de rendimiento
    """
    if df.empty:
        return None
    
    df_rendimiento = df.copy()
    df_rendimiento['Viewers por Hora'] = df_rendimiento['Viewers'] / df_rendimiento['Horas Transmitidas']
    df_rendimiento['Likes por Hora'] = df_rendimiento['Likes'] / df_rendimiento['Horas Transmitidas']
    df_rendimiento['Regalos por Hora (S/.)'] = df_rendimiento['Regalos (S/.)'] / df_rendimiento['Horas Transmitidas']
    return df_rendimiento

def obtener_clasificacion_rendimiento(viewers_por_hora):
    """
    Clasifica el rendimiento según los viewers por hora
    """
    if viewers_por_hora >= 500:
        return "EXCELENTE"
    elif viewers_por_hora >= 200:
        return "BUENO"
    elif viewers_por_hora >= 100:
        return "REGULAR"
    else:
        return "MEJORABLE"

def analisis_completo_rendimiento(df):
    """
    Realiza un análisis completo de rendimiento incluyendo métricas por hora
    """
    if df.empty:
        return {"error": "No hay datos para analizar"}
    
    df_rendimiento = calcular_rendimiento_por_hora(df)
    mejor_por_hora = df_rendimiento.loc[df_rendimiento['Viewers por Hora'].idxmax()]
    
    promedio_rendimiento = {
        'prom_viewers_por_hora': df_rendimiento['Viewers por Hora'].mean(),
        'prom_likes_por_hora': df_rendimiento['Likes por Hora'].mean(),
        'prom_regalos_por_hora': df_rendimiento['Regalos por Hora (S/.)'].mean()
    }
    #apply() se usa para aplicar la funcion de clasificacion
    df_rendimiento['Clasificación'] = df_rendimiento['Viewers por Hora'].apply(obtener_clasificacion_rendimiento)
    
    return {
        'df_rendimiento': df_rendimiento,
        'mejor_por_hora': mejor_por_hora.to_dict(),
        'promedios_rendimiento': promedio_rendimiento
    }