# =============================================
# SISTEMA DE ESTADÍSTICAS - TEAM AFK
# Curso: Fundamentos de Programación
# =============================================

import pandas as pd
import os
from analisis import (
    cargar_datos_en_dataframe,
    generar_estadisticas_generales,
    encontrar_mejor_stream,
    analizar_streamers,
    generar_alertas_basicas,
    guardar_reporte,
    analisis_completo_rendimiento,
    obtener_clasificacion_rendimiento
)


# Listas globales para almacenar los datos

fechas = []
streamers = []
viewers = []
likes = []
regalos = []
horas = []


# Funciones de validacion y entrada de datos

def pedir_numero(mensaje):
    """Solicita un número entero positivo o cero al usuario"""
    while True:
        entrada = input(mensaje)
        if entrada == "":
            print("El valor no puede estar vacío")
            continue
        if entrada.isdigit():
            #isdigit verifica si son solo digitos
            return int(entrada)
        print("Error: Debes ingresar un número entero")

def pedir_numero_positivo(mensaje):
    """Solicita un número entero mayor a cero"""
    while True:
        num = pedir_numero(mensaje)
        if num > 0:
            return num
        print("El valor debe ser mayor que cero")

def pedir_texto(mensaje):
    """Solicita un texto no vacío al usuario"""
    while True:
        entrada = input(mensaje).strip()
        if entrada == "":
            print("El texto no puede estar vacío")
            continue
        return entrada

def pedir_fecha(mensaje):
    """Solicita una fecha en formato dd/mm/aaaa"""
    from datetime import datetime

    while True:
        fecha = pedir_texto(mensaje)
        
        # Validar formato básico (dd/mm/aaaa)
        if len(fecha) == 10 and fecha[2] == '/' and fecha[5] == '/':
            try:
                datetime.strptime(fecha, "%d/%m/%Y")

                #Validar que no sea año futuro
                if int(fecha[6:10]) > datetime.now().year:
                    print(f"El año no puede ser mayor a {datetime.now().year}")
                    continue
                return fecha
            
            except ValueError:
                print("Fecha inválida. El día/mes no existe")
        else:
            print("Formato inválido. Usa dd/mm/aaaa")


# Gestion de archivos (Persistencia)

def cargar_datos():
    """Carga los datos desde un archivo CSV si existe"""
    global fechas, streamers, viewers, likes, regalos, horas
    if os.path.exists("streams.csv"):
        try:
            #utf-8-sig es para manejar correctamente los caracteres especiales
            df = pd.read_csv("streams.csv", encoding='utf-8-sig')
            fechas = df['Fecha'].tolist()
            streamers = df['Streamer'].tolist()
            viewers = df['Viewers'].tolist()
            likes = df['Likes'].tolist()
            regalos = df['Regalos (S/.)'].tolist()
            horas = df['Horas Transmitidas'].tolist()
            print(f"Datos cargados {len(fechas)} streams encontrados")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}. Se iniciará con datos vacíos")
    else:
        print("No se encontró un archivo de datos previo. Iniciando nuevo registro")

def guardar_datos():
    """Guarda los datos actuales en un archivo CSV"""
    if not fechas:
        print("No hay datos para guardar")
        return
    df = cargar_datos_en_dataframe(fechas, streamers, viewers, likes, regalos, horas)
    guardar_reporte(df, "streams.csv")


# Funciones del menu

def registrar_stream():
    """Solicita los datos y registra un nuevo stream"""
    print("\n" + "="*50)
    print("NUEVO STREAM")
    print("="*50)
    
    fecha = pedir_fecha("Fecha (dd/mm/aaaa): ")
    streamer = pedir_texto("Nombre del streamer: ")
    vw = pedir_numero("Cantidad de viewers: ")
    lk = pedir_numero("Cantidad de likes: ")
    rg = pedir_numero("Regalos en soles (S/.): ")
    hr = pedir_numero_positivo("Horas transmitidas: ")

    fechas.append(fecha)
    streamers.append(streamer)
    viewers.append(vw)
    likes.append(lk)
    regalos.append(rg)
    horas.append(hr)

    print("Stream registrado exitosamente!")
    guardar_datos()

def mostrar_streams():
    """Muestra todos los streams registrados en forma de tabla"""
    print("\n" + "="*50)
    print("TODOS LOS STREAMS")
    print("="*50)
    
    if not fechas:
        print("No hay streams registrados aún")
        return
    
    df = cargar_datos_en_dataframe(fechas, streamers, viewers, likes, regalos, horas)
    print(df.to_string(index=False))

def ver_estadisticas_generales():
    """Muestra estadísticas generales usando el módulo de análisis"""
    print("\n" + "="*50)
    print("ESTADÍSTICAS GENERALES")
    print("="*50)
    
    df = cargar_datos_en_dataframe(fechas, streamers, viewers, likes, regalos, horas)
    stats = generar_estadisticas_generales(df)
    
    if "error" in stats:
        print(f"{stats['error']}")
        return
    
    print(f"Total de streams: {stats['total_streams']}")
    print(f"Promedio de viewers: {stats['promedio_viewers']:.2f}")
    print(f"Promedio de likes: {stats['promedio_likes']:.2f}")
    print(f"Promedio de regalos (S/.): {stats['promedio_regalos']:.2f}")
    print(f"Promedio de horas transmitidas: {stats['promedio_horas']:.2f}")
    print(f"Total recaudado en regalos: S/. {stats['total_regalos']:.2f}")

def analizar_rendimiento():
    """
    Función que combina varios análisis: mejor stream, mejores streamers y alertas
    """
    print("\n" + "="*60)
    print("ANÁLISIS DE RENDIMIENTO COMPLETO")
    print("="*60)
    
    df = cargar_datos_en_dataframe(fechas, streamers, viewers, likes, regalos, horas)
    if df.empty:
        print("No hay datos para analizar")
        return


    #1. Analisis de rendimiento por hora
    print("\nRENDIMIENTO POR HORA TRANSMITIDA")
    print("-" * 50)
    
    resultado = analisis_completo_rendimiento(df)
    if "error" not in resultado:
        df_rendimiento = resultado['df_rendimiento']
        
        mejor = resultado['mejor_por_hora']
        print(f"\nMEJOR RENDIMIENTO (Viewers por Hora):")
        print(f"Fecha: {mejor['Fecha']}")
        print(f"Streamer: {mejor['Streamer']}")
        print(f"Viewers por Hora: {mejor['Viewers por Hora']:.2f}")
        print(f"Clasificación: {obtener_clasificacion_rendimiento(mejor['Viewers por Hora'])}")
        
        promedios = resultado['promedios_rendimiento']
        print(f"\nPROMEDIOS GENERALES DE RENDIMIENTO:")
        print(f"Viewers promedio por hora: {promedios['prom_viewers_por_hora']:.2f}")
        print(f"Likes promedio por hora: {promedios['prom_likes_por_hora']:.2f}")
        print(f"Regalos promedio por hora: S/. {promedios['prom_regalos_por_hora']:.2f}")
        
        print(f"\nCLASIFICACIÓN DE STREAMS (de mejor a peor):")
        print("-" * 50)
        df_ordenado = df_rendimiento.sort_values('Viewers por Hora', ascending=False)
        for idx, (_, row) in enumerate(df_ordenado.iterrows(), 1):
            print(f"{idx}. {row['Fecha']} - {row['Streamer']}: {row['Viewers por Hora']:.2f} viewers/h → {row['Clasificación']}")


    #2. Mejor stream (por viewers totales)
    print("\n" + "="*60)
    print("MEJOR STREAM POR VIEWERS TOTALES")
    print("-" * 50)
    
    mejor = encontrar_mejor_stream(df)
    if mejor is not None:
        print(f"Fecha: {mejor['Fecha']}")
        print(f"Streamer: {mejor['Streamer']}")
        print(f"Viewers: {mejor['Viewers']}")
        print(f"Likes: {mejor['Likes']}")
        print(f"Regalos: S/. {mejor['Regalos (S/.)']}")
        print(f"Horas: {mejor['Horas Transmitidas']}")


    # 3. Ranking de streamers
    print("\n" + "="*60)
    print("RANKING DE STREAMERS")
    print("-" * 50)
    
    ranking = analizar_streamers(df)
    if "error" not in ranking:
        print(f"Más viewers: {ranking['mejor_por_viewers']['Streamer']} - ({ranking['mejor_por_viewers']['Viewers']} views)")
        print(f"Más likes: {ranking['mejor_por_likes']['Streamer']} - ({ranking['mejor_por_likes']['Likes']} likes)")
        print(f"Más regalos: {ranking['mejor_por_regalos']['Streamer']} - (S/. {ranking['mejor_por_regalos']['Regalos (S/.)']})")


    # 4. Alertas del sistema
    print("\n" + "="*60)
    print("ALERTAS DEL SISTEMA")
    print("-" * 50)
    
    alertas = generar_alertas_basicas(df)
    for alerta in alertas:
        print(f"{alerta}")
    print("\n" + "="*60)

def generar_reporte_csv():
    """
    Genera un reporte completo en formato CSV
    Usa la función guardar_reporte del módulo de analisis
    """
    print("\n" + "="*50)
    print("GENERAR REPORTE CSV")
    print("="*50)
    
    df = cargar_datos_en_dataframe(fechas, streamers, viewers, likes, regalos, horas)
    if df.empty:
        print("No hay datos para generar el reporte")
        return
    
    nombre_archivo = "reporte_team_afk.csv"
    guardar_reporte(df, nombre_archivo)


# Menu principal del programa

def menu():
    """Muestra el menú principal y maneja la interacción con el usuario"""
    cargar_datos()
    
    while True:
        print("\n" + "="*50)
        print("MENÚ PRINCIPAL - TEAM AFK")
        print("="*50)
        print("1. Registrar nuevo stream")
        print("2. Mostrar todos los streams")
        print("3. Ver estadísticas generales")
        print("4. Analizar rendimiento")
        print("5. Generar reporte en CSV")
        print("6. Salir")
        print("="*50)

        opcion = input("Elige una opción (1-6): ")

        if opcion == "1":
            registrar_stream()
        elif opcion == "2":
            mostrar_streams()
        elif opcion == "3":
            ver_estadisticas_generales()
        elif opcion == "4":
            analizar_rendimiento()
        elif opcion == "5":
            generar_reporte_csv()
        elif opcion == "6":
            print("\nGuardando datos y cerrando el programa")
            guardar_datos()
            print("Hasta luego Team AFK!")
            break
        else:
            print("Opción no válida. Por favor, elige un número del 1 al 6")


# Punto de entrada del programa
if __name__ == "__main__":
    menu()