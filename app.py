from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail, Message
import pandas as pd
import os
from io import BytesIO


app = Flask(__name__)
app.secret_key = 'shellife'  


# Configurações do Flask-Mail para Outlook
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'paulo.cunha@hortifruti.com.br'  # Substitua com seu e-mail Outlook
app.config['MAIL_PASSWORD'] = '@catete.366'              # Substitua com sua senha
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'next':
            # Salvando dados na sessão
            for key in request.form:
                if key != 'action':
                    session[key] = request.form[key]
            return redirect(url_for('form'))

        elif action == 'send':
            # Criar DataFrame e salvar como Excel
            df = pd.DataFrame([session])
            excel_file = BytesIO()
            with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False)
            excel_file.seek(0)

            # Enviar e-mail com o Excel anexado
            msg = Message('Dados do Formulário', sender='paulo.cunha@hortifruti.com.br', recipients=['contato.paulooliver9@gmail.com'])
            msg.body = 'Segue em anexo os dados do formulário.'
            msg.attach('dados_formulario.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', excel_file.read())
            mail.send(msg)

            # Limpar sessão
            session.clear()
            return 'E-mail enviado com sucesso!'

    return render_template('form.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)
