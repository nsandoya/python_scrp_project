# Python SCRP Project
###### Python final project

## Lenguajes y Librerías
| #   | Tecnología        | Descripción                                   | URL                                                                                                       |
| --- | ----------------- | --------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `1` | Python | Codificación | [Ver](https://www.python.org/doc/)                                                                            |
| `2` | Pandas          | Manipulación y análisis de datos                   | [Ver](https://pandas.pydata.org/docs/getting_started/index.html#getting-started) |
| `3` | Jupyter   | Visualización de datos                 | [Ver](https://docs.jupyter.org/en/latest/)                                                            |
| `4` | beautifulsoup4              | Recopilación de datos desde la web                    | [Ver](https://beautiful-soup-4.readthedocs.io/en/latest/)                                                                          |


## ⏬ Instalar dependencias
Escribir en la terminal: `pip install -r dep.txt`

## ▶ Ejecutar (en CLI)
1. Verificar posición en la ruta raíz del proyecto.
2. Escribir: `python3 -m [archivo]`. El archivo principal se ejecuta así: 
    `python3 -m project`

## Menú principal
### 🤖 Scraping
1. Scrape
`python3 -m project` (también es posible añadir `-go s`)
2. Reescritura de datos existentes
`python3 -m project -go rw`

### 🔎 Analisis
Genera y muestra en consola los insights principales de los datos obtenidos.
`python3 -m project -go a`
Para más análisis, y visualización de los datos obtenidos, consultar el **jupyter notebook** del proyecto: `notebooks/explorations.ipynb`

### 🟠 Análisis: Exportar resultados (HTML file)
¿No sería genial guardar todos los análisis en un archivo independiente y de fácil acceso? 
`python3 -m project -go j`
🙋🏻‍♀️ Consultar informe generado: `notebooks/explorations.html`

### 🙌 Ayuda
En caso de dudas, consultar la pequeña guía del proyecto:
`python3 -m project -h`

## 📍 Nota Importante
Para el proceso de obtención de datos, se estableció un límite de 8 páginas por categoría.