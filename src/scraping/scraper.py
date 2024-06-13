import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os # Interacción con el sistema operativo
from ..decorators.decorators import timethis, logthis # Import de módulos internos: decoradores para loggin

@timethis
@logthis
def get_data(url):
    response = requests.get(url)
    # Petición exitosa
    if response.status_code == 200: 
        return response
    else:
        # En caso de error, responder:
        raise Exception(f"Failed to get data from: {url}. Try again later. Atte: The scraper ;)")

@timethis
@logthis
def scrape_several_pages(base_url, category):
    items = []
    page = 1
    parsed_category = regex_help(category)

    while True:
       url = ""
       url = f"{base_url}{category}?page={page}"
       #print("url", url)
       new_items = get_data(url)
       parsed_items = parse_product(new_items, parsed_category)
       if not new_items:
           break
       """ if page == 5:
           break """
       
       items.extend(parsed_items) # Junta la lista original con la nueva lista
       page = page + 1
    
    items = process_data(items)
    return pd.DataFrame(items)


def parse_product(products, category):
    soup = BeautifulSoup(products.text, "html.parser")
    itemsList = []

   # items = soup.select(".product-meta") 
    items = soup.select(".product_item") # Selecciona todos los elementos que tengan esta clase
    #print(items)
    # Pase de selección, html tags
    for item in items:
        #name_element = item.select_one(".p-name h3 a")
        name_element = item.select_one(".product-description h3 a")
        #price_element = item.select_one(".p-price .product-price-and-shipping .price > span:nth-child(2)")
        price_element = item.select_one(".product-price-and-shipping .price")

        # Comprobar que ambos elementos existan, antes de intentar usarlos
        if name_element and price_element:
            #name = name_element["title"] # Obtener en concreto el html tag 'title'
            name = name_element.get_text(strip=True)
            price = price_element.get_text(strip=True)
            #print("Zapatos",{name, price})
            brand = brand_filter(name)
            itemsList.append({"name": name, "price": price, "category": category, "brand": brand}) # De esta forma sí estoy generando una lista de diccionarios, en vez de una lista de tuplas
    
        # Control de flujo
        if not name_element or not price_element:
            print("Error al tratar de obtener datos")
            continue
    
    return itemsList

def regex_help(string):
    pattern = r"(\d+)-(.*)"

# Aplicar la regex para dividir el string
    result = re.match(pattern, string)

    if result:
        # La primera parte es el número, la segunda parte es el resto del string
        n = result.group(1)
        category = result.group(2)
        #print("Número:", n)
        print("Category:", category)
    else:
        print("No se encontró el patrón en el texto.")

    return category

def brand_filter(item):
    brandList = [
        "Mia Secret",
        "Salon Line",
        "Beauty Creations",
        "L.A. Girl",
        "Milani",
        "Wahl",
        "Maxybelt",
        "Echos Line",
        "Generation Makeup",
        "L.A. Colors",
        "MakeUp-Pro",
        "Byotea",
        "Glam Beauty",
        "Dompel",
        "Revuele",
        "Prolux",
        "Hot Tools",
        "CBD",
        "G9",
        "The fruit lab",
        "Staleks"
]
    # Función para asignar la marca al producto
    # Iterar sobre la lista de marcas predefinidas y buscar coincidencias en el nombre del producto
    for brand in brandList:
        if brand.lower() in item.lower():
            return brand
    return "N/A"  # Si no se encuentra ninguna coincidencia, devolver None

# Aplicar la función de asignar_marca a la columna 'Producto' y crear una nueva columna 'Marca'


@timethis
@logthis
def process_data(items):
    processed_data = []
    for item in items: # Esto es un refactor para iterar en la lista de dicts y extraer datos por keys
        name = item.get("name", "Nombre no disponible")
        price = item.get("price", "Precio no disponible")
        category = item.get("category", "Categoría no disponible")
        brand = item.get("brand", "Marca no disponible")
        #price = price.replace('\xa0$', "") 
        price = price.strip("$ ")
        price = float(price.replace(",", ".")) # Convertir el str 'price' a decimal para luego poder analizar datos
        processed_data.append({"Modelo": name, "Precio": price, "Categoría": category, "Marca": brand})
    return processed_data


def save_to(df, output_path):
    to_save = pd.DataFrame(df)
    if output_path.endswith(".csv"):
        to_save.to_csv(f"{output_path}", index=False)
    elif output_path.endswith(".xlsx"):
        to_save.to_excel(f"{output_path}", index=False)
    else:
        raise ValueError("Wrong file format. Please try again")
    
    print(f"Data saved to {output_path}")


if __name__ == "__main__":
    #base_url = "https://coleguini.com/"
    base_url = "https://www.dipaso.com.ec/"
    section = "cat/"
    category = "336-tratamientos"
    output_path = f"data/processed/scraped_data_{category}.csv"

    data = scrape_several_pages(base_url+section, category)
    os.makedirs("data/processed/", exist_ok=True) # Crea el directorio si no existe
    save_to(data, output_path)
