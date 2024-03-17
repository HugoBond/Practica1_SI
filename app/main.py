from flask import Flask, render_template

from utils.etl import ETL

app = Flask(__name__)
app.jinja_env.globals.update(type=type)
app.jinja_env.globals.update(lista=list)

etl = ETL()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/2')
def ejercicio2():
    data = etl.getEjercicio2Data()
    print(data)
    return render_template('plotDatos.html', data=data, num=2)

@app.route('/3')
def ejercicio3():
    data = etl.getEjercicio3Data()
    print(data)
    return render_template('plotDatos.html', data=data, num=3)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)