from flask import Flask, render_template, request, jsonify
import random
import datetime

app = Flask(__name__)

# --- LÓGICA DE GENERACIÓN (Algoritmo de Luhn) ---
def luhn_checksum(card_number):
    """Calcula el dígito de control de Luhn."""
    digits = list(map(int, card_number))
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for d in even_digits:
        total += sum(list(map(int, str(d * 2))))
    return total % 10

def generate_card(bin_pattern, month, year):
    """Genera un número de tarjeta sintético válido."""
    # Completar el BIN hasta 15 dígitos con números aleatorios
    card_number = bin_pattern
    while len(card_number) < 15:
        card_number += str(random.randint(0, 9))
    
    # Calcular el dígito 16 (Luhn)
    digits = list(map(int, card_number))
    total = 0
    for i, d in enumerate(digits):
        if (len(digits) - i) % 2 == 0:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    
    check_digit = (10 - (total % 10)) % 10
    card_number += str(check_digit)
    
    # Formatear fecha
    if month == "Rand":
        month = str(random.randint(1, 12)).zfill(2)
    if year == "Rand":
        year = str(random.randint(2024, 2040))
        
    # Generar CVV aleatorio
    cvv = str(random.randint(100, 999))
    
    return f"{card_number}|{month}|{year}|{cvv}"

# --- LÓGICA DE BUSCADOR DE BIN ---
def get_bin_info(bin_num):
    """Buscador de BIN básico basado en red."""
    if not bin_num or len(bin_num) < 1:
        return "N/A", "N/A", "N/A"
    
    first_digit = bin_num[0]
    network = "Desconocida"
    
    if first_digit == '4':
        network = "Visa"
    elif first_digit == '5':
        network = "Mastercard"
    elif first_digit == '3':
        if len(bin_num) >= 2 and bin_num[0:2] in ['34', '37']:
            network = "Amex"
        else:
            network = "JCB/Other"
    elif first_digit == '6':
        network = "Discover"
        
    # En una versión pro, aquí consultarías una base de datos real
    card_type = "Crédito/Débito (Simulado)"
    country = "Simulado"
    
    return network, card_type, country

# --- RUTAS DE FLASK ---
@app.route('/')
def index():
    # Generar lista de años hasta 2040 para los selectores
    current_year = datetime.datetime.now().year
    years = ["Rand"] + [str(y) for y in range(current_year, 2041)]
    months = ["Rand"] + [str(m).zfill(2) for m in range(1, 13)]
    
    return render_template('index.html', years=years, months=months)

@app.route('/generate', methods=['POST'])
def handle_generate():
    data = request.json
    bin_input = data.get('bin', '').replace(' ', '')
    month = data.get('month', 'Rand')
    year = data.get('year', 'Rand')
    quantity = int(data.get('quantity', 10))
    
    # Validación básica del BIN
    if not bin_input or not bin_input.isdigit():
        bin_pattern = "400000" # BIN por defecto si falla
    else:
        bin_pattern = bin_input[:6] # Usamos solo los primeros 6-8

    cards = []
    for _ in range(min(quantity, 100)): # Límite de 100 por seguridad
        cards.append(generate_card(bin_pattern, month, year))
        
    return jsonify({'cards': cards})

@app.route('/check_bin', methods=['POST'])
def handle_check_bin():
    data = request.json
    bin_num = data.get('bin', '').replace(' ', '')
    
    network, card_type, country = get_bin_info(bin_num)
    
    return jsonify({
        'bin': bin_num[:6],
        'network': network,
        'type': card_type,
        'country': country
    })

if __name__ == '__main__':
    # Importante: debug=False para producción en Render
    app.run(debug=False, host='0.0.0.0', port=5000)
