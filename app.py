from flask import Flask, render_template, request, jsonify
import random
import datetime
import requests

app = Flask(__name__)

# --- LÓGICA DEL GENERADOR ---
def generate_card(bin_pattern, month, year):
    # Limpiar el BIN: solo dejamos números
    bin_digits = "".join(filter(str.isdigit, bin_pattern))
    
    # Completamos a 15 dígitos para calcular el 16 con Luhn
    card_number = bin_digits
    while len(card_number) < 15:
        card_number += str(random.randint(0, 9))
    
    # Algoritmo de Luhn
    digits = list(map(int, card_number))
    total = 0
    for i, d in enumerate(digits):
        if (len(digits) - i) % 2 == 0:
            d *= 2
            if d > 9: d -= 9
        total += d
    
    check_digit = (10 - (total % 10)) % 10
    card_number += str(check_digit)
    
    # Fechas
    if month == "Rand":
        month = str(random.randint(1, 12)).zfill(2)
    if year == "Rand":
        year = str(random.randint(2024, 2040))
        
    cvv = str(random.randint(100, 999))
    return f"{card_number}|{month}|{year}|{cvv}"

# --- RUTAS ---
@app.route('/')
def index():
    current_year = datetime.datetime.now().year
    years = ["Rand"] + [str(y) for y in range(current_year, 2041)]
    months = ["Rand"] + [str(m).zfill(2) for m in range(1, 13)]
    return render_template('index.html', years=years, months=months)

@app.route('/generate', methods=['POST'])
def handle_generate():
    data = request.json
    bin_input = data.get('bin', '400022')
    month = data.get('month', 'Rand')
    year = data.get('year', 'Rand')
    quantity = int(data.get('quantity', 10))

    cards = []
    for _ in range(min(quantity, 100)):
        cards.append(generate_card(bin_input, month, year))
        
    return jsonify({'cards': cards})

@app.route('/check_bin', methods=['POST'])
def handle_check_bin():
    data = request.json
    # Solo tomamos los primeros 6-8 dígitos para la API
    bin_num = "".join(filter(str.isdigit, data.get('bin', '')))[:8]
    
    if len(bin_num) < 6:
        return jsonify({'error': 'Mínimo 6 dígitos'})

    try:
        # Consultamos base de datos real (binlist)
        response = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=5)
        if response.status_code == 200:
            info = response.json()
            return jsonify({
                'network': info.get('scheme', 'N/A').upper(),
                'type': info.get('type', 'N/A').upper(),
                'brand': info.get('brand', 'N/A'),
                'country': info.get('country', {}).get('name', 'N/A'),
                'bank': info.get('bank', {}).get('name', 'N/A'),
                'flag': info.get('country', {}).get('emoji', '')
            })
        return jsonify({'network': 'No encontrado', 'bank': 'N/A', 'country': 'N/A'})
    except:
        return jsonify({'error': 'Servidor de BINs ocupado'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)from flask import Flask, render_template, request, jsonify
import random
import datetime
import requests

app = Flask(__name__)

# --- LÓGICA DEL GENERADOR ---
def generate_card(bin_pattern, month, year):
    # Limpiar el BIN: solo dejamos números
    bin_digits = "".join(filter(str.isdigit, bin_pattern))
    
    # Completamos a 15 dígitos para calcular el 16 con Luhn
    card_number = bin_digits
    while len(card_number) < 15:
        card_number += str(random.randint(0, 9))
    
    # Algoritmo de Luhn
    digits = list(map(int, card_number))
    total = 0
    for i, d in enumerate(digits):
        if (len(digits) - i) % 2 == 0:
            d *= 2
            if d > 9: d -= 9
        total += d
    
    check_digit = (10 - (total % 10)) % 10
    card_number += str(check_digit)
    
    # Fechas
    if month == "Rand":
        month = str(random.randint(1, 12)).zfill(2)
    if year == "Rand":
        year = str(random.randint(2024, 2040))
        
    cvv = str(random.randint(100, 999))
    return f"{card_number}|{month}|{year}|{cvv}"

# --- RUTAS ---
@app.route('/')
def index():
    current_year = datetime.datetime.now().year
    years = ["Rand"] + [str(y) for y in range(current_year, 2041)]
    months = ["Rand"] + [str(m).zfill(2) for m in range(1, 13)]
    return render_template('index.html', years=years, months=months)

@app.route('/generate', methods=['POST'])
def handle_generate():
    data = request.json
    bin_input = data.get('bin', '400022')
    month = data.get('month', 'Rand')
    year = data.get('year', 'Rand')
    quantity = int(data.get('quantity', 10))

    cards = []
    for _ in range(min(quantity, 100)):
        cards.append(generate_card(bin_input, month, year))
        
    return jsonify({'cards': cards})

@app.route('/check_bin', methods=['POST'])
def handle_check_bin():
    data = request.json
    # Solo tomamos los primeros 6-8 dígitos para la API
    bin_num = "".join(filter(str.isdigit, data.get('bin', '')))[:8]
    
    if len(bin_num) < 6:
        return jsonify({'error': 'Mínimo 6 dígitos'})

    try:
        # Consultamos base de datos real (binlist)
        response = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=5)
        if response.status_code == 200:
            info = response.json()
            return jsonify({
                'network': info.get('scheme', 'N/A').upper(),
                'type': info.get('type', 'N/A').upper(),
                'brand': info.get('brand', 'N/A'),
                'country': info.get('country', {}).get('name', 'N/A'),
                'bank': info.get('bank', {}).get('name', 'N/A'),
                'flag': info.get('country', {}).get('emoji', '')
            })
        return jsonify({'network': 'No encontrado', 'bank': 'N/A', 'country': 'N/A'})
    except:
        return jsonify({'error': 'Servidor de BINs ocupado'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)v
