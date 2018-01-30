# Agendamento de pacientes

Projeto de agendamento de procedimentos para pacientes, feito em Python utilizando Django e Django Rest Framework.

## Iniciando

Clone o projeto

```
git clone https://github.com/tomaslm/agendamentoAPI
```

### Instalação

Instalar o Django e o Django Rest Framework (globalmente ou em um ambiente virtual)

```
pip install Django
pip install djangorestframework
```

Navege para a pasta do projeto

```
cd agendamentoAPI
```

Construa o banco de dados

```
python manage.py makemigrations
```

## Executando os testes

Teste o projeto

```
 python -Wall manage.py test
```

## Executando o projeto

Execute o projeto na porta padrão (8000)

```
python manage.py runserver
```

Ou em uma porta específica

```
python manage.py runserver {PORT}
```

## Referências

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Django Rest Framework](http://www.django-rest-framework.org/)
* [SQLite](https://www.sqlite.org/)
