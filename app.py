from flask import Flask, render_template, request, jsonify
import prediction

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

# api ouvindo solicitações POST e prevendo sentimentos


@app.route('/predict', methods=['POST'])
def predict():

    response = ""
    review = request.json.get('customer_review')
    if not review:
        response = {'status': 'error',
                    'message': 'Avaliação em Branco'}

    else:

        # chamando o método predict do módulo de previsão.py
        sentiment, path = prediction.predict(review)
        response = {'status': 'success',
                    'message': 'Got it',
                    'sentiment': sentiment,
                    'path': path}

    return jsonify(response)


# Criando uma API para salvar a avaliação. O usuário clica no botão Salvar
@app.route('/save', methods=['POST'])
def save():

    # extraindo data , nome do produto , avaliação e sentimento associado aos dados JSON
    date = request.json.get('date')
    product = request.json.get('product')
    review = request.json.get('review')
    sentiment = request.json.get('sentiment')

    # criando uma variável final separada por vírgulas
    # data_entry = date + "," + product + "," + review + "," + sentiment
    # data_entry = sentiment + "," + review + "," + product + "," + date
    #data_entry = date + "," + product + "," + sentiment + "," + review

    review = review.replace("\n", " ")

    data_entry = f'{date}, {product}, {sentiment}, {review}\n'

    # abra o arquivo no modo 'append'
    with open('./static/assets/datafiles/saved_reviews.csv', 'a') as f:
        # Registre os dados no arquivo
        f.write(data_entry)

    # retorne uma mensagem de sucesso
    return jsonify({'status': 'success',
                    'message': 'Dados Registrados'})


if __name__ == "__main__":
    app.run(debug=True)
