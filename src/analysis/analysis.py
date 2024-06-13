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
    mean_price = f"${df['Precio'].mean()}"
    max_price = f"${df['Precio'].max()}"
    min_price = f"${df['Precio'].min()}"
    
    """ print("Productos: análisis general")
    print("\n")
    print(f"Precio promedio: ${df['Precio'].mean():.2f}")
    print(f"Precio más alto: ${df['Precio'].max():.2f}")
    print(f"Precio mínimo: ${df['Precio'].min():.2f}")
    
    print("\n")

    print("\n Productos: top 10, precios más altos")
    print(highest_prices) """

    # Agrupa por categoría y calcula estadísticas descriptivas
    estadisticas_por_categoria = df.groupby('Categoría')['Precio'].describe()
    # Identifica las categorías con los precios más altos y más bajos
    categorias_extremas = estadisticas_por_categoria.sort_values(by='mean', ascending=False)

    # Marcas preferidas del público
    frecuencia_marcas = df['Marca'].value_counts()
    # Categorías preferidas del público
    frecuencia_categorías = df['Categoría'].value_counts()

    # 1. Se aplica la función contar_palabras_clave a la columna 'Producto' 
    df_palabras_clave = pd.DataFrame(df['Modelo'].apply(contar_palabras_clave).tolist())
    # 2. Resultado: un nuevo DataFrame (df_palabras_clave) con la frecuencia de las palabras clave. 
    # Es decir, se crea una tabla donde cada producto crea un registro, y marca 1 o 0 por cada palabra clave que contenga. Este 1 o 0 se marca en la columna correspondiente a c/palabra clave
    #print(df_palabras_clave)
    # 3. Luego, se suman los registros de c/columna. De esta forma se obtiene la frecuencia total de cada columna (palabra clave)
    frecuencia_total_palabras_clave = df_palabras_clave.sum()
    #print(frecuencia_total_palabras_clave)

    results = {
        "top_ten_highest_prices": highest_prices,
        "mean_price": mean_price,
        "highest_price": max_price,
        "min_price": min_price,
        "estadisticas_por_categoria": estadisticas_por_categoria, 
        "categorias_extremas": categorias_extremas, 
        "frecuencia_marcas": frecuencia_marcas, 
        "frecuencia_categorías": frecuencia_categorías,
        "df_palabras_clave": df_palabras_clave,
        "frecuencia_total_palabras_clave": frecuencia_total_palabras_clave
    }
    return results
    

# Frecuencia de palabras clave en los productos
def contar_palabras_clave(nombre_producto):
    # Lista de palabras clave
    palabras_clave = ['frizz', 'edad', 'hidratante', 'tratamiento', 'facial', 'capilar']  
    nombre_producto_lower = nombre_producto.lower()
    # Contar la frecuencia de c/palabra clave, producto por producto
    frecuencia_palabras_clave = {palabra: nombre_producto_lower.count(palabra.lower()) for palabra in palabras_clave}
    return frecuencia_palabras_clave

 

if __name__ == "__main__":  
    base = "data/processed/scraped_all_data"
    data_path = f"{base}.csv"
    df = load_data(data_path)   
    nombre_producto = "Muss antifrizz"
    analyze_data(df)
    contar_palabras_clave(nombre_producto)
    
    