import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "http://coleguini.com/"

def get_data(url):
    response = requests.get(url)
    # Petición exitosa
    if response.status_code == 200: 
        return response
    else:
        # En caso de error, responder:
        raise Exception(f"Failed to get data from: {url}. Try again later. Atte: Coleguini ;)")

def scape_several_pages(base_url, categoria):
    items = []
    page = 1
    while True:
       #url = f"{url}/catalogue/page-{page}.html"
       url = ""
       url = f"{base_url}{categoria}?page={page}"
       print("url", url)
       new_items = get_data(url)
       parsed_items = parse_product(new_items)
       """ if not nuevos_items:
           break """
       if page == 5:
           break
       items.extend(parsed_items) # Junta la lista original con la nueva lista
       page = page + 1
    #print(items)
    return items

def parse_product(products):
    soup = BeautifulSoup(products.text, "html.parser")
    itemsList = []

    items = soup.select(".product-meta") # Selecciona todos los elementos que tengan esta clase
    #print(items)
    # Pase de selección, html tags
    for item in items:
        name_element = item.select_one(".p-name h3 a")
        price_element = item.select_one(".p-price .product-price-and-shipping .price > span:nth-child(2)")

        # Comprobar que ambos elementos existan, antes de intentar usarlos
        if name_element and price_element:
            #name = name_element["title"] # Obtener en concreto el html tag 'title'
            name = name_element.get_text(strip=True)
            price = price_element.get_text(strip=True)
            #print("Zapatos",{name, price})
            itemsList.append({"name": name, "price": price}) # De esta forma sí estoy generando una lista de diccionarios, en vez de una lista de tuplas
    
        # Control de flujo
        if not name_element or not price_element:
            print("Error al tratar de obtener datos")
            continue

    return itemsList

def process_data(items):
    processed_data = []
    for item in items: # Esto es un refactor para iterar en la lista de dicts y extraer datos por keys
        name = item.get("name", "Nombre no disponible")
        price = item.get("price", "Precio no disponible")
        price = price.replace('\xa0$', "") 
        price = float(price.replace(",", ".")) # Convertir el str 'price' a decimal para luego poder analizar datos
        processed_data.append({"Modelo": name, "Precio": price})

        # Control de flujo (para mostrar solo los primeros 10)
        """ if len(datos_procesados)>= 10:
            break """
    #print(f"Lista recibida:{books}")
    #print(f"Lista a exportar:{datos_procesados}")
    return processed_data


data = scape_several_pages(base_url, "24-flats-y-deportivos")
#parsed_data = parse_product(data)
processed_data = process_data(data)
print(processed_data)