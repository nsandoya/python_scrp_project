from nbconvert import PDFExporter
import nbformat
import os
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter

from src.decorators.decorators import timethis, logthis

@timethis
@logthis
def export_notebook_to_html(data_path, html_path):
    try:
        # Leer el contenido del archivo .ipynb
        with open(data_path, "r", encoding="utf-8") as f:
            contenido = f.read()

        # Eliminar la variable conflictiva (mandaba a buscar el notebook un nivel más arriba, y eso es conflictivo desde el archivo principal del programa)
        nuevo_contenido = contenido.replace("sys.path.append('../')", "")

        # Guardar el contenido modificado en un nuevo archivo .ipynb
        nuevo_archivo = os.path.splitext(data_path)[0] + "_modificado.ipynb"
        with open(nuevo_archivo, "w", encoding="utf-8") as f:
            f.write(nuevo_contenido)

        print(f"El path 'sys.path.append('../')' se ha eliminado")


        # Exportar el notebook a HTML
        html_exportador = HTMLExporter()
        with open(nuevo_archivo, "r", encoding="utf-8") as f:
            notebook = nbformat.read(f, as_version=4)
        html_exportador.exclude_input = True  # Excluir el código del notebook
        cuerpo, _ = html_exportador.from_notebook_node(notebook)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(cuerpo)

        return nuevo_archivo
    
    except Exception as e:
        print(f"Error al reemplazar la variable en el archivo .ipynb: {e}")
        return None

def export_notebook_to_pdf(notebook_path, output_path):
    # No se pudo usar porque hace falta instalar una app aparte... 
    pdf_exporter = PDFExporter()
    (body, resources) = pdf_exporter.from_filename(notebook_path)
    with open(output_path, "wb") as f:
        f.write(body)

if __name__ == "__main__":
    notebook_path = 'notebooks/explorations.ipynb'
    output_path = 'notebooks/explorations.pdf'
    export_notebook_to_html(notebook_path, output_path)