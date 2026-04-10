from flask import Flask, render_template, request
import random

app = Flask(__name__)

def generar_logica(entrada):
    # Separamos la entrada PAN|MES|AÑO|CVV
    partes = entrada.split('|')
    while len(partes) < 4: partes.append("x")
    raw_pan, raw_mes, raw_anio, raw_cvv = partes
    
    # Procesamos el PAN (Luhn)
    lista = [random.randint(0,9) if c.lower()=='x' else int(c) for c in raw_pan if c.isdigit() or c.lower()=='x']
    while len(lista) < 15: lista.append(random.randint(0,9))
    lista = lista[:15]
    
    # Algoritmo de Luhn para el dígito 16
    suma = sum((d*2-9 if d*2>9 else d*2) if i%2==0 else d for i,d in enumerate(reversed(lista)))
    lista.append((10 - (suma % 10)) % 10)
    
    pan_final = "".join(map(str, lista))
    
    # Fecha y CVV
    mes_f = raw_mes.zfill(2) if 'x' not in raw_mes.lower() and raw_mes != 'x' else str(random.randint(1,12)).zfill(2)
    anio_f = raw_anio if 'x' not in raw_anio.lower() and raw_anio != 'x' else "2026"
    cvv_f = raw_cvv if 'x' not in raw_cvv.lower() and raw_cvv != 'x' else str(random.randint(100,999))
    
    return f"{pan_final}|{mes_f}|{anio_f}|{cvv_f}"

@app.route('/', methods=['GET', 'POST'])
def home():
    resultados = []
    if request.method == 'POST':
        datos = request.form.get('datos')
        cantidad = int(request.form.get('cantidad', 10))
        for _ in range(cantidad):
            resultados.append(generar_logica(datos))
    return render_template('index.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=False)