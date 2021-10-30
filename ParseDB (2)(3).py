import sqlite3
import json,requests
#from flask import Flask,request,Response,jsonify,render_template
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.response import file

db2 = sqlite3.connect("./ConsultaNome.db",check_same_thread=False)
tim = sqlite3.connect("./dbTim.db",check_same_thread=False)
app = Sanic(__name__)

def ConsultaTim(tel):
    c = tim.cursor()
    c.execute("select * from TIM where tel = ?",[tel])   
    try:al = c.fetchall()[0]
    except: return "[]"
    
    sexo = al[0]
    cpf = al[1]
    nome = al[2]
    tipolgd = al[3]
    logradouro = al[4] 
    numero = al[5]
    complemento = al[6]
    bairro = al[7]
    cidade = al[8]
    cep = al[9]
    tel = al[10]
    
    res = {"Sexo":sexo,
           "CPF":cpf,
           "Nome":nome,
           "Tipolgd":tipolgd,
           "Logradouro":logradouro,
           "Numero":numero,
           "Complemento":complemento,
           "Bairro":bairro,
           "Cidade":cidade,
           "CEP":cep,
           "Telefone":tel}
    
    return json.dumps(res)

def ConsultaTimCpf(cpf):
    c = tim.cursor()
    c.execute("select * from TIM where cpf = ?",[cpf])   
    try:al = c.fetchall()[0]
    except: return "[]"
    
    sexo = al[0]
    cpf = al[1]
    nome = al[2]
    tipolgd = al[3]
    logradouro = al[4] 
    numero = al[5]
    complemento = al[6]
    bairro = al[7]
    cidade = al[8]
    cep = al[9]
    tel = al[10]
    
    res = {"Sexo":sexo,
           "CPF":cpf,
           "Nome":nome,
           "Tipolgd":tipolgd,
           "Logradouro":logradouro,
           "Numero":numero,
           "Complemento":complemento,
           "Bairro":bairro,
           "Cidade":cidade,
           "CEP":cep,
           "Telefone":tel}
    
    return json.dumps(res)

def ConsultaCPFSimples(cpf:str):
    cur = db2.cursor()
    cur.execute('select * from Brasil where Cpf=?',[cpf])
    try:
        dados = cur.fetchall()[0]
        dadosSimples = {'Nome':dados[0],
                        'Cpf':dados[1],
                        'Genero':dados[2],
                        'Nascimento':dados[3][:-1]}
    except:
        dadosSimples = {"erro":"cpf n existe"}
    cur.close()
    return json.dumps(dadosSimples)

def ConsultaNome(nome:str):
    c = db2.cursor()
    nome = nome + '%'
    c.execute("select * from Brasil where Nome LIKE ? limit 1000",[nome])
    results = c.fetchall()
    c.close()

    response = []
    for i in results:
        dados = {"Nome":i[0],
                    "Cpf":i[1],
                    "Genero":i[2],
                    "Nascimento":i[3][:-1]}
        response.append(dados)

    return json.dumps(response)

@app.route("/",methods = ['POST',"GET"])
def Server(request:Request):
    parameters = request.args

    if "nome" in parameters:
        nome = parameters.get("nome")
        return text(ConsultaNome(nome))

    if "cpfSimples" in parameters:
        cpf = parameters.get("cpfSimples")
        return text(ConsultaCPFSimples(cpf))
    
    if "tim" in parameters:
        tel = parameters.get("tim")
        return text(ConsultaTim(tel))
    
    if "timCpf" in parameters:
        cpf = parameters.get("timCpf")
        return text(ConsultaTimCpf(cpf))
    
    if "foto" in parameters:
        cpf = parameters.get("foto")
        try: return file(location='./db foto/%s.jpg' % cpf,mime_type='image')
        except: return text("None")
        
app.run(host="0.0.0.0", port=8888,debug=False)