from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    cotacoes = requests.get('https://economia.awesomeapi.com.br/json/all')
    cot_dic = cotacoes.json()
    
    moedas = []
    for moeda, dados in cot_dic.items():
        # Excluir apenas o dólar turismo
        if moeda == "USDT":
            continue
        nome = dados['name'].split('/')[0]  # Pegando apenas o nome da moeda
        valor = dados['bid']
        moedas.append({'code': moeda, 'nome': nome, 'valor': valor})

    # Adicionando o Real manualmente
    moedas.append({'code': 'BRL', 'nome': 'Real Brasileiro', 'valor': '1.0'})

    return render_template('index.html', moedas=moedas)

@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.form['from_currency']
    amount = float(request.form['amount'])
    
    cotacoes = requests.get('https://economia.awesomeapi.com.br/json/all')
    cot_dic = cotacoes.json()

    conversions = {}
    
    if from_currency == 'BRL':
        from_value = 1.0
    else:
        from_value = float(cot_dic[from_currency]['bid'])

    # Adicionando conversão para o Real
    conversions['BRL'] = amount * from_value

    for moeda, dados in cot_dic.items():
        if moeda == "USDT" or moeda == from_currency:  # Skip the dólar turismo and the from_currency
            continue
        to_value = float(dados['bid'])
        if from_currency == 'BRL':
            converted_amount = amount / to_value
        else:
            converted_amount = (amount * from_value) / to_value
        conversions[moeda] = converted_amount
    
    return jsonify(conversions)

# if __name__ == '__main__':
#     app.run(debug=True)
