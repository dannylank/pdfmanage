import os
import PyPDF2
from fpdf import FPDF


class PDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agrega la fuente desde un archivo TTF
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf')
    
    def add_custom_text(self, text, font_size=10, line_height=5):
        self.set_font('DejaVu', size=font_size)
        # Usar multi_cell para agregar el texto. El primer parámetro (w=0) permite que el texto ocupe el ancho completo de la página.
        self.multi_cell(0, line_height, text)

def crear_pdf_con_texto(texto, ruta_salida, font_size, line_height):
    texto_modificado = texto.replace("© Universidad Internacional de La Rioja (UNIR)", "")
    
    pdf = PDF()
    pdf.add_page()
    pdf.add_custom_text(texto_modificado, font_size, line_height)
    pdf.output(ruta_salida)

def extraer_texto_de_pdf(directorio, nombre_archivo):
    # Construir la ruta completa del archivo
    ruta_del_archivo = os.path.join(directorio, nombre_archivo)
    
    # Abrir el archivo PDF en modo binario
    with open(ruta_del_archivo, 'rb') as archivo:
        # Crear un objeto PDF reader
        lector_pdf = PyPDF2.PdfReader(archivo)
        texto_completo = ''
        
        # Iterar sobre cada página del PDF
        for pagina in lector_pdf.pages:
            # Extraer el texto de la página
            texto_completo += pagina.extract_text() + '\n'
        
        return texto_completo

# Definir la carpeta donde está el archivo y el nombre del archivo PDF de entrada
directorio = r'D:\Files\Personal\Ingenieria\Aproximación al a investigación'
nombre_archivo = 'temas_merged.pdf'

# Usar la función para extraer el texto y crear un nuevo nombre de archivo para la salida
texto = extraer_texto_de_pdf(directorio, nombre_archivo)
nombre_archivo_salida = os.path.splitext(nombre_archivo)[0] + '_text.pdf'
ruta_salida = os.path.join(directorio, nombre_archivo_salida)

# Crear el nuevo PDF con el texto extraído
crear_pdf_con_texto(texto, ruta_salida, font_size=9, line_height=5)
