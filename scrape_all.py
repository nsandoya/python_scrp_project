import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os # Interacción con el sistema operativo
from src.scraping.scraper import get_data, scrape_several_pages
#from ..decorators.decorators import timethis, logthis

def verificar_archivo_categoria(categoria):
    data_path = "data/processed/"
    # Generar el nombre del archivo
    nombre_archivo = f"scraped_data_{categoria}.csv"
    ruta_completa = os.path.join(data_path, nombre_archivo)

    # Verificar si el archivo existe en el directorio actual
    if os.path.exists(ruta_completa):
        print("Sí existe")
        return True
    else:
        print("No existe")
        return False

def save_to(df_nuevo, output_path):
    # Lee el archivo CSV existente en un DataFrame
    if os.path.exists(output_path):
        # Si existe, lee el archivo CSV en un DataFrame
        df_existente = pd.read_csv(output_path)
        
        # Combina el DataFrame existente con el nuevo
        df_combinado = pd.concat([df_existente, df_nuevo], ignore_index=True)
        
        # Guarda el DataFrame combinado en el archivo CSV
        df_combinado.to_csv(output_path, index=False)
        
        print(f"Data saved to {output_path}")
    else:
        # Si el archivo no existe, guarda el nuevo DataFrame directamente en el archivo CSV
        to_save = pd.DataFrame(df_nuevo)
        if output_path.endswith(".csv"):
            to_save.to_csv(output_path, index=False)
        else:
            raise ValueError("Wrong file format. Please try again")
        
        print(f"Data saved to {output_path}")
    # Agrega la información de una nueva fuente a otro DataFrame
    # Por ejemplo, lee datos de otra fuente y almacénalos en df_nuevo

    # Concatena los DataFrames existentes con los nuevos

def scrape_all(base_url, category, category_list, output_path):
    for category in category_list:
        """ if verificar_archivo_categoria(category):
            data = scrape_several_pages(base_url, category)
        else:
            continue """
        data = scrape_several_pages(base_url, category)
        save_to(data, output_path)



#verificar_archivo_categoria("336-tratamientos")  
if __name__ == "__main__":
    #base_url = "https://coleguini.com/"
    base_url = "https://www.dipaso.com.ec/"
    section = "cat/"
    category = "336-tratamientos"
    output_path = "data/processed/scraped_all_data.csv"
    category_list = ["336-tratamientos", "334-capilar", "25-maquillaje", "323-cuidado-facial", "28-unas", "566-joyerias-y-novedades"]

    data = scrape_all(base_url+section, category, category_list, output_path)
    os.makedirs("data/processed/", exist_ok=True) # Crea el directorio si no existe
    #save_to(data, output_path)