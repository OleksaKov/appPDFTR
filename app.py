from flask import Flask, render_template, request, send_file
import fitz  # PyMuPDF
from googletrans import Translator
from reportlab.pdfgen import canvas
import os
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    file = request.files['pdf']
    if not file:
        return "No file uploaded", 400

    pdf = fitz.open(stream=file.read(), filetype="pdf")
    translator = Translator()

    translated_pages = []
    for page in pdf:
        text = page.get_text()
        translated = translator.translate(text, src='en', dest='uk').text
        translated_pages.append(translated)

    # Generate new PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer)
    for page_text in translated_pages:
        for i, line in enumerate(page_text.split('\n')):
            c.drawString(40, 800 - 15 * i, line)
        c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="translated.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
