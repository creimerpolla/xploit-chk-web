from flask import Flask, render_template, request, jsonify
import random
import datetime

app = Flask(__name__)

# --- LÓGICA MATEMÁTICA (Algoritmo de Luhn) ---
def generate_card(bin_pattern, month, year):
    # Limpiar el BIN de cualquier cosa que no sea número
    bin_digits = "".join(filter(str.isdigit, bin_pattern))
    
    # Si el BIN es corto, lo completamos hasta 15 dígitos
    card_number = bin_digits
    while len(card_number) < 15:
        card_number += str(random.randint(0, 9))
    
    # Algoritmo de Luhn para el dígito 16 (Dígito de verificación)
    digits = list(map(int, card_number))
    total = 0
    for i, d in enumerate(digits):
        if (len(digits) - i) % 2 == 0:
            d *= 2
            if d > 9: d -= 9
        total += d
    
    check_digit = (10 - (total % 10)) % 10
    card_number += str(check_digit)
    
    # Manejo de fechas aleatorias
    if month == "Rand":
        month = str(random.randint(1, 12)).zfill(2)
    if year == "Rand":
        year = str(random.randint(2024, 2040))
        
    cvv = str(random.randint(100, 999))
    return f"{card_number}|{month}|{year}|{cvv}"

# --- RUTAS ---
@app.route('/')
def index():
    # Generamos las listas para los selectores del HTML
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
    bin_num = data.get('bin', '')
    
    # Buscador de red simple
    network = "Desconocida"
    if bin_num.startswith('4'): network = "Visa"
    elif bin_num.startswith('5'): network = "Mastercard"
    elif bin_num.startswith('3'): network = "American Express"
    
    return jsonify({
        'network': network,
        'type': "Crédito/Débito",
        'country': "México"
    })

if __name__ == '__main__':
    # Importante: debug=False para que funcione bien en Render
    app.run(debug=False, host='0.0.0.0', port=5000)v
