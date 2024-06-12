import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os # Interacción con el sistema operativo
from ..decorators.decorators import timethis, logthis # Import de módulos internos: decoradores para loggin

def extract_categories(url):
    raw_menu = get_data(url)
    soup = BeautifulSoup(raw_menu.text, "html.parser")
    itemsList = []

    # Selecciona todos los elementos 'li' dentro del menú
    items = soup.select("#_desktop_top_menu #top-menu li")

    for item in items:
        # Selecciona el primer enlace 'a' dentro de cada elemento 'li'
        menu_item = item.select_one(".dropdown-item[data-depth='0']")

        if menu_item:
            # Obtiene el texto del enlace y lo agrega a la lista de items
            name = menu_item.get_text(strip=True)
            itemsList.append({"name": name})
        else:
            # Si no hay un enlace 'a', continúa con el siguiente elemento 'li'
            continue
    #print(itemsList)
    return itemsList

def process_menu_items(items):
    processed_menu_items = []
    pattern_to_remove = r'\\([A-Za-z0-9]+)\\(ue)'

    for item in items:
        name = item.get("name", "Item no disponible")
        name = name.replace(" ", "-")
        name = name.lower()
        lista = re.split(r'\\[A-Za-z0-9]+\\ue', str(name))
        #name = remove_pattern(name, pattern_to_remove)
        print(lista)
        #processed_menu_items.append(name)
    #print(processed_menu_items)
    #return processed_menu_items

""" def remove_pattern(text, pattern):
    # Compila el patrón regex
    regex = re.compile(pattern)
    # Sustituye el patrón con un string vacío
    cleaned_text = regex.sub('', text)
    return cleaned_text """



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
def scape_several_pages(base_url, category):
    items = []
    page = 1
    parsed_category = regex_help(category)

    while True:
       url = ""
       url = f"{base_url}{category}?page={page}"
       print("url", url)
       new_items = get_data(url)
       parsed_items = parse_product(new_items, parsed_category)
       """ if not new_items:
           break """
       if page == 5:
           break
       
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
            itemsList.append({"name": name, "price": price, "category": category}) # De esta forma sí estoy generando una lista de diccionarios, en vez de una lista de tuplas
    
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

@timethis
@logthis
def process_data(items):
    processed_data = []
    for item in items: # Esto es un refactor para iterar en la lista de dicts y extraer datos por keys
        name = item.get("name", "Nombre no disponible")
        price = item.get("price", "Precio no disponible")
        category = item.get("category", "Categoría no disponible")
        #price = price.replace('\xa0$', "") 
        price = price.strip("$ ")
        price = float(price.replace(",", ".")) # Convertir el str 'price' a decimal para luego poder analizar datos
        processed_data.append({"Modelo": name, "Precio": price, "Categoría": category})
    return processed_data


def save_to(df, outout_path):
    to_save = pd.DataFrame(df)
    if outout_path.endswith(".csv"):
        to_save.to_csv(f"{outout_path}", index=False)
    elif outout_path.endswith(".xlsx"):
        to_save.to_excel(f"{outout_path}", index=False)
    else:
        raise ValueError("Wrong file format. Please try again")
    
    print(f"Data saved to {outout_path}")




if __name__ == "__main__":
    #base_url = "https://coleguini.com/"
    base_url = "https://www.dipaso.com.ec/"
    section = "cat/"
    category = "336-tratamientos"
    output_path = f"data/processed/scraped_data_{category}.csv"

    #data = scape_several_pages(base_url+section, category)
    #os.makedirs("data/processed/", exist_ok=True) # Crea el directorio si no existe
    #save_to(data, output_path)
