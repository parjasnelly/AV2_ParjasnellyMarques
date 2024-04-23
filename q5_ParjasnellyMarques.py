
from flask import Flask, render_template, redirect, url_for, request,render_template_string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import base64
import csv
# Utilizei a questão 4 como base para a questão 5!!
from q4_ParjasnellyMarques import gen_inner_join, GAMES, VIDEOGAMES, COMPANY


# escrever chaves de encriptação e decriptação caso o arquivo encriptionkeys.txt esteja vazio
def escrever_chaves():
    csv.writer(open('encriptionkeys.txt', 'w')).writerow([base64.b64encode(get_random_bytes(16)).decode('utf-8'), base64.b64encode(get_random_bytes(16)).decode('utf-8')])
    return ler_chaves()


# ler chaves de encriptação e decriptação para que não sejam geradas novas chaves a cada execução do programa e assim não perder os dados encriptados no arquivo credenciais.txt
ler_chaves = lambda: next(csv.reader(open('encriptionkeys.txt', 'r'))) if (len(list(csv.reader(open('encriptionkeys.txt', 'r')))) == 2)else escrever_chaves()


# funções de encriptação e decriptação
cipher = lambda: AES.new(base64.b64decode(ler_chaves()[0]), AES.MODE_CBC, base64.b64decode(ler_chaves()[1]))
decipher = lambda: AES.new(base64.b64decode(ler_chaves()[0]), AES.MODE_CBC, base64.b64decode(ler_chaves()[1]))

app = Flask(__name__, template_folder='templates')

escrever_login_senha = lambda login, senha: csv.writer(open('credenciais.txt', 'a')).writerow([login, base64.b64encode(senha).decode('utf-8')])
ler_logins_senhas = lambda: [[row[0], decipher().decrypt(base64.b64decode(row[1]))] for row in csv.reader(open('credenciais.txt', 'r')) if len(row) == 2]
verify_credentials = lambda username, password: any([username == row[0] and password == row[1] for row in ler_logins_senhas()])

# Página de login
login = lambda: verify_login() if request.method == 'POST' else render_template('index.html')

# Pagina de cadastro
register = lambda: render_template('register.html') if request.method == 'GET' else cadastrar()


def cadastrar():
    escrever_login_senha(request.form['username'], cipher().encrypt(pad(bytes(request.form['password'], encoding='utf-8'), 16)))
    return redirect(url_for('index'))


# Se as credenciais estiverem corretas vai para a página de inner join da questão 4, senão continua na página de login
verify_login = lambda: render_template('index.html') if not verify_credentials(request.form['username'], pad(bytes(request.form['password'], encoding='utf-8'), 16)) else render_template_string(gen_inner_join([GAMES(), VIDEOGAMES(), COMPANY()], "*",""))

app.add_url_rule('/', 'index', login, methods=['GET', 'POST'])
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.run()
