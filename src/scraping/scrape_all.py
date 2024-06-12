import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os # Interacción con el sistema operativo
#from scraper import get_data, scape_several_pages, save_to
from ..decorators.decorators import timethis, logthis


def verificar_archivo_categoria(categoria, data_path):
    """
    Verifica si ya existe un archivo con el nombre de la categoría especificada.

    Args:
    - categoria: Nombre de la categoría.

    Returns:
    - True si el archivo existe, False de lo contrario.
    """
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

# Ejemplo de uso
""" categoria = "ropa"
if verificar_archivo_categoria(categoria):
    print(f"El archivo para la categoría '{categoria}' ya existe.")
else:
    print(f"No se encontró archivo para la categoría '{categoria}'.")


def scrape_all(base_url, category, category_list):
    for category in category_list:
        data = scape_several_pages(base_url, category) """

verificar_archivo_categoria("336-tratamientos", "data/processed/")  


""" if __name__ == "__main__":
    #base_url = "https://coleguini.com/"
    base_url = "https://www.dipaso.com.ec/"
    section = "cat/"
    category = "336-tratamientos"
    output_path = f"data/processed/scraped_data_{category}.csv"

    data = scape_several_pages(base_url+section, category)
    os.makedirs("data/processed/", exist_ok=True) # Crea el directorio si no existe
    save_to(data, output_path) """