import pandas as pd
import os # Interacción con el sistema operativo
from ..decorators.decorators import timethis, logthis # Import de módulos internos: decoradores para loggin

@logthis
@timethis
def load_data(data_path):
    if data_path.endswith(".csv"):
        df = pd.read_csv(data_path)
    elif data_path.endswith(".xlsx"):
        df = pd.read_excel(data_path)
    else:
        raise ValueError("Invalid file format")
    
    print("File required for analysis: ✅")
    return df

@logthis
@timethis
def analyze_data(df):
    # Análisis básico de los datos
    print("\n Productos: top 5, precios más altos")
    highest_prices = df.nlargest(5, "Precio")
    print(highest_prices)
    
    print("\n")
    
    print(f"Precio promedio: ${df['Precio'].mean():.2f}")
    print(f"Precio más alto: ${df['Precio'].max():.2f}")
    print(f"Precio mínimo: ${df['Precio'].min():.2f}")



if __name__ == "__main__":
    base_url = "data/processed/scraped_data_"
    category = "14-carteras"
    data_path = f"{base_url}{category}.csv"

    df = load_data(data_path)
    analyze_data(df)