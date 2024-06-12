import pandas as pd
import os # Interacción con el sistema operativo
from src.decorators.decorators import timethis, logthis # Import de módulos internos: decoradores para loggin

""" @timethis
@logthis """
def load_data(data_path):
    if data_path.endswith(".csv"):
        df = pd.read_csv(data_path)
    elif data_path.endswith(".xlsx"):
        df = pd.read_excel(data_path)
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
    
    print(f"Precio promedio: ${df['Precio'].mean():.2f}")
    print(f"Precio más alto: ${df['Precio'].max():.2f}")
    print(f"Precio mínimo: ${df['Precio'].min():.2f}")
    
    print("\n")

    print("\n Productos: top 10, precios más altos")
    print(highest_prices)
    
    

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
    analyze_data(df)
    
    