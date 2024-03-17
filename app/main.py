from flask import Flask, render_template

from utils.etl import ETL

app = Flask(__name__)
app.jinja_env.globals.update(type=type)
app.jinja_env.globals.update(lista=list)
app.jinja_env.globals.update(enumerate=enumerate)

etl = ETL()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/1')
def ejercicio1():
    return render_template('ejercicio1.html')

@app.route('/2')
def ejercicio2():
    data = etl.getEjercicio2Data()
    return render_template('plotDatos.html', data=data, num=2)

@app.route('/3')
def ejercicio3():
    data = etl.getEjercicio3Data()
    return render_template('plotDatos.html', data=data, num=3)

@app.route('/4')
def ejercicio4():
    data, especial = etl.getEjercicio4Data()
    return render_template('plotGrafico.html', data=data, special=especial)

@app.route('/uml')
def uml():
    return render_template('uml.html')

@app.route('/bpmn')
def bpmn():
    return render_template('bpmn.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)