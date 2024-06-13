### Python SCRP Project
#### Python final project

##### Para instalar dependencias
Escribir en la terminal: `pip install -r dep.txt`

##### Para ejecutar el programa/main file usando rutas relativas en CLI
1. Verificar que estamos en la ruta raíz del proyecto
2. Escribir: `python3 -m [módulo].[carpeta].[archivo]` (sin extensiones). En este caso, nuestro menú principal se ejecuta así: 
    `python3 -m project`

##### Menú principal
###### Scraping
1. Scrape
`python3 -m project` (también puedes añadir `-go s`)
2. Reescritura de datos existentes
`python3 -m project -go rw`
###### Analisis
`python3 -m project -go a`
###### Análisis: Exportar resultados (HTML file)
`python3 -m project -go j`
###### Ayuda
`python3 -m project -h`

###### Nota Importante
Dado que el ecommerce elegido tiene muchas páginas de producto (hasta +20 en ciertas categorías), se estableció un límite de 8 páginas por categoría.