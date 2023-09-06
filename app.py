from flask import Flask, request, render_template, session, redirect, url_for
from flask_session import Session
import csv

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/', methods=['GET', 'POST'])
def form():
    if 'data' not in session:
        session['data'] = []

    if request.method == 'POST':
        # Coletar dados do formulário
        current_data = {
            'setor': request.form['setor'],
            'nt': request.form['nt'],
            'tempo_inicial': request.form['tempo_inicial'],
            'tempo_inicio_separacao': request.form['tempo_inicio_separacao'],
            'nivel': request.form['nivel'],
            'item_fora_da_rota': request.form['item_fora_da_rota'],
            'tempo_termino_separacao': request.form['tempo_termino_separacao'],
        }

        session['data'].append(current_data)
        session.modified = True

        if request.form['submit_button'] == 'Gerar':
            # Gravar em um arquivo CSV
            keys = current_data.keys()
            with open('responses.csv', 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(session['data'])

            session.clear()
            return 'Respostas registradas com sucesso!'

    return render_template('form.html')

if __name__ == '__main__':
       app.run(host='0.0.0.0', port=80,debug=True)