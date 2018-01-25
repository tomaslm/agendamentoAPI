from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite>///tmp\\test.db'
db = SQLAlchemy(app)

class Agendamento(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    paciente = db.Column(db.String(120),nullable=False)
    procedimento = db.Column(db.String(120),nullable=True)

    def __repr_(self):
        return '<Agendamento >'

@app.route('/agendamentos', methods=['GET'])
def getAgendamentos():
	#request.args.get('page')
    return 'GET list, World!'

@app.route('/agendamentos', methods=['POST'])
def criaAgendamento():
    db.session.add(Agendamento(paciente='Tomas',procedimento='Nada'))
    return 'POST, World!'
	
@app.route('/agendamentos/<id>', methods=['GET'])
def consultaAgendamento():
	#request.view_args['id']
    return 'GET, World!'

@app.route('/agendamentos/<id>', methods=['PUT'])
def atualizaAgendamento():
	#request.view_args['id']
    return 'PUT, World!'

@app.route('/agendamentos/<id>', methods=['DELETE'])
def excluiAgendamento():
	#request.view_args['id']
    return Agendamento(paciente='Tomas',procedimento='Nada')
