import pandas as pd
import os # Interacción con el sistema operativo

def load_data(data_path):
    if data_path.endswith(".csv"):
        df = pd.read_csv(data_path)
    elif data_path.endswith(".xlsx"):
        df = pd.read_excel(data_path)
    else:
        raise ValueError("Invalid file format")
    
    print("File required for analysis: ✅")
    return df

def analyze_data(df):
    # Análisis básico de los datos
    print("Basic data analysis/Summary:")
    print(df.describe())
    print("\n Products with highest prices:")
    highest_prices = df.nlargest(5, "Precio")
    print(highest_prices)
    



if __name__ == "__main__":
    data_path = "data/raw/scraped_data_"
    category = "14-carteras"

    df = load_data(data_path)
    analyze_data(df)
    os.makedirs()