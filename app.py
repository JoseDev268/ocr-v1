from flask import Flask, render_template, request, redirect, url_for, flash
import os
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'secret-key'


os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


ocr_model = ocr_predictor(pretrained=True,assume_straight_pages=False)

# Definimos patron para la busqueda
patterns = {
    "Cedula de indentidad": r"(?i)No?[:\s]*([\d]+)",
    "Nombres": r"(?i)Nombres?[:\s]*([A-Za-z\s]+)",
    "Apellidos": r"(?i)Apellidos?[:\s]*(\w+\s+\w+)",
    "Fecha de Nacimiento": r"(?i)Fecha De Nacimiento?[:\s]*([\d]{2}/[\d]{2}/[\d]{4})",
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Revisa si el archivo ya fue subido
        if 'file' not in request.files or request.files['file'].filename == '':
            flash('No file uploaded!', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file:
            # Guarda el documento
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            # Procesado de la imagen
            doc = DocumentFile.from_images(file_path)
            result = ocr_model(doc)

            # # Reconstruccion de la imagen 
            # synthetic_pages = result.synthesize()
            # plt.imshow(synthetic_pages[0]); plt.axis('off'); plt.show()


            pages = result.export()["pages"]
            text = ""
            for page in pages:
                for block in page["blocks"]:
                    for line in block["lines"]:
                        line_text = " ".join([word["value"] for word in line["words"]])
                        text += line_text + " "
                    # text += line_text.strip() + "\n"

            
            os.remove(file_path)

            # Filtrado de text en funcion a los patrones anteriormente definidos
            extracted_data = {}
            for key, pattern in patterns.items():
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    extracted_data[key] = match.group(1).strip()
                else:
                    extracted_data[key] = None

            
            return render_template('index.html', extracted_data=extracted_data)

    return render_template('index.html', extracted_data=None)

if __name__ == '__main__':
    app.run(debug=True)
