import pandas as pd
import os # Interacción con el sistema operativo
from src.decorators.decorators import timethis, logthis # Import de módulos internos: decoradores para loggin

""" @timethis
@logthis """
def load_data(data_path):
    if data_path.endswith(".csv"):
        df = pd.read_csv(data_path)
    #elif data_path.endswith(".xlsx"):
        #df = pd.read_excel(data_path)
        if not df:
            raise FileNotFoundError("File does not exist. Try again")
    else:
        raise ValueError("Invalid file format")
    
    print("File required for analysis: ✅")
    return df

""" @timethis
@logthis """
def analyze_data(df):        
    # Análisis básico de los datos
    highest_prices = df.nlargest(10, "Precio")
    mean_price = f"${df['Precio'].mean():.2f}"
    max_price = f"${df['Precio'].max():.2f}"
    min_price = f"${df['Precio'].min():.2f}"
    
    print("Productos: análisis general")
    print("\n")
    print(f"Precio promedio: ${df['Precio'].mean():.2f}")
    print(f"Precio más alto: ${df['Precio'].max():.2f}")
    print(f"Precio mínimo: ${df['Precio'].min():.2f}")
    
    print("\n")

    print("\n Productos: top 10, precios más altos")
    print(highest_prices)
    
    # Filtrar los registros que tienen una marca válida (es decir, que no son None)
    df_brand_filtered = df.dropna(subset=['Marca'])
    
    

# Función para contar la frecuencia de las palabras clave en los nombres de los productos
def contar_palabras_clave(nombre_producto):
    # Lista de palabras clave
    palabras_clave = ['frizz', 'edad', 'hidratante', 'tratamiento', 'facial', 'capilar']  # Agrega aquí tus palabras clave
    # Convertir el nombre del producto a minúsculas para hacer coincidencias insensibles a mayúsculas y minúsculas
    nombre_producto_lower = nombre_producto.lower()
    # Contar la frecuencia de cada palabra clave en el nombre del producto
    frecuencia_palabras_clave = {palabra: nombre_producto_lower.count(palabra.lower()) for palabra in palabras_clave}
    return frecuencia_palabras_clave

    

    """ results = {
        "Top 10, precios más altos": highest_prices,
        "Precio promedio": mean_price,
        "Precio más alto": max_price,
        "Precio mínimo": min_price
    }
    print(results) """


if __name__ == "__main__":  
    base = "data/processed/scraped_all_data"
    data_path = f"{base}.csv"
    df = load_data(data_path)   
    nombre_producto = "Muss antifrizz"
    analyze_data(df)
    contar_palabras_clave(nombre_producto)
    
    