import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os # Interacción con el sistema operativo
import argparse

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

from src.decorators.decorators import timethis, logthis
from src.scraping.scraper import get_data, scrape_several_pages
from src.analysis.analysis import analyze_data, load_data
from notebooks.export_notebook import export_notebook_to_html

# CLI UI
parser = argparse.ArgumentParser(description="This is a tool specially made for Dipaso ecommerce. You can extract data from there, analyze it and see brands, categories, prices and other market tendencies in a group of friendly stadistic graphics (in a Jupyter file).") # Se crea una instancia de clase
parser.add_argument("-go", default="s", help="Write 's' to scrape data, 'a' to analyze data, 'rw' to delete the existing data and scrape again, or 'j' to export an html file from notebook! :D. Ex: -go s, -go a, -go rw, -go j", type=str) # Creamos argumentos/parámetros
args = parser.parse_args() # Se crea un objeto cuyas keys guardan los argumentos creados por nosotros (que luego serán los parámetros que el usuario ingrese)

def file_exists(data_path):
    return os.path.exists(data_path)

def seek_and_save_to(df_nuevo, output_path):
    # Lee el archivo CSV existente en un DataFrame
    if file_exists(output_path):
        # Si existe, lee el archivo CSV en un DataFrame
        df_existente = pd.read_csv(output_path)
        # Combina el DataFrame existente con el nuevo
        df_combinado = pd.concat([df_existente, df_nuevo], ignore_index=True)
        # Guarda el DataFrame combinado en el archivo CSV
        df_combinado.to_csv(output_path, index=False)
        
        print(f"Data saved to {output_path}")
    else:
        # Si el archivo no existe, guarda el nuevo DataFrame directamente en un nuevo archivo .csv
        to_save = pd.DataFrame(df_nuevo)
        if output_path.endswith(".csv"):
            to_save.to_csv(output_path, index=False)
        else:
            raise ValueError("Wrong file format. Please try again")
    
    print(f"Data saved to {output_path}")

@timethis
@logthis
def scrape_all(base_url, category, category_list, output_path):
    for category in category_list:
        data = scrape_several_pages(base_url, category)
        seek_and_save_to(data, output_path)

@timethis
@logthis
def analyze_all(df):
    results = analyze_data(df)
    mean_price = results['mean_price']
    highest_price = results['highest_price']
    min_price = results['min_price']
    top_ten_highest_prices = results['top_ten_highest_prices']

    # Análisis general
    print("\n")
    print("Precio promedio", mean_price)
    print("Precio más alto", highest_price)
    print("Precio mínimo", min_price)
    print("\n")
    print("Top 10, precios más altos")
    print(top_ten_highest_prices)


if __name__ == "__main__":
    #base_url = "https://coleguini.com/"
    base_url = "https://www.dipaso.com.ec/"
    section = "cat/"
    category = "336-tratamientos"
    output_path = "data/processed/scraped_all_data.csv"
    jupyter_path = "notebooks/explorations.ipynb"
    html_path = "notebooks/explorations.html"
    category_list = ["336-tratamientos", "334-capilar", "25-maquillaje", "323-cuidado-facial", "28-unas", "566-joyerias-y-novedades"]

    try:
        if args.go == "s":
            if not file_exists(output_path):
                data = scrape_all(base_url+section, category, category_list, output_path)
                os.makedirs("data/processed/", exist_ok=True) # Crea el directorio si no existe
            else:
                print("Data already exists. Let's analize it :)")
                exit()

        elif args.go == "a":
            df = load_data(output_path)
            analyze_all(df)
        elif args.go == "rw":
            os.remove(output_path)
            print(f"{output_path} has been removed. Now let's scrape again!")
            data = scrape_all(base_url+section, category, category_list, output_path)
            os.makedirs("data/processed/", exist_ok=True) # Crea el directorio si no existe
        elif args.go == "j":
            export_notebook_to_html(jupyter_path, html_path)
    except Exception as e:
        print(f"Error: {e}")
        exit()
        