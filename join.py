import os
from PyPDF2 import PdfReader, PdfWriter

# Cambia la ruta al directorio de tu carpeta en Windows
folder_path = r'D:\Files\Personal\Ingenieria\Computación Bioinspirada'

# Filtrar archivos para solo seleccionar los PDFs
pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

# Crear un objeto PdfWriter para generar el PDF combinado
writer = PdfWriter()

# Iterar sobre cada archivo PDF y agregar sus páginas al nuevo documento
for pdf_file in pdf_files:
    pdf_path = os.path.join(folder_path, pdf_file)
    reader = PdfReader(pdf_path)
    for page in reader.pages:
        writer.add_page(page)

# Guardar el PDF combinado en un nuevo archivo
output_path = os.path.join(folder_path, 'merged_output.pdf')
with open(output_path, 'wb') as output_file:
    writer.write(output_file)
