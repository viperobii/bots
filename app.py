import os
import io
from flask import Flask, request, render_template, send_file, abort
from bot.obfuscator import obfuscate

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/obfuscate', methods=['POST'])
def do_obfuscate():
    file = request.files.get('file')
    if not file or not file.filename.lower().endswith(('.lua', '.txt')):
        abort(400, "Invalid file type. Only .lua or .txt allowed.")
    
    src = file.read().decode('utf-8', errors='ignore')
    obf = obfuscate(src)
    
    buffer = io.BytesIO(obf.encode('utf-8'))
    return send_file(
        buffer,
        as_attachment=True,
        download_name='Velonix_Obfuscated.lua',
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))