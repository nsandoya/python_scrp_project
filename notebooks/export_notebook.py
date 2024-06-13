from nbconvert import PDFExporter

def export_notebook_to_pdf(notebook_path, output_path):
    pdf_exporter = PDFExporter()
    (body, resources) = pdf_exporter.from_filename(notebook_path)
    with open(output_path, "wb") as f:
        f.write(body)

if __name__ == "__main__":
    notebook_path = 'notebooks/explorations.ipynb'
    output_path = 'notebooks/explorations.pdf'
    export_notebook_to_pdf(notebook_path, output_path)