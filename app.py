# db.py
from flask import Flask, render_template, request, redirect, url_for,session, flash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import webbrowser
from datetime import datetime  # Importa datetime
from werkzeug.security import generate_password_hash
import mysql.connector


app = Flask(__name__)

miConexion = mysql.connector.connect( host='localhost', user='root', password='', db='solunadb' )
cur =miConexion.cursor()

app.secret_key = 'mysecretkey'


#Pagina de inicio

@app.route('/')
def home():
    return render_template('Registrousuario.html')

#Registrar Usuario
@app.route('/AgregarAdmin', methods=["GET", "POST"])
def AgregarAdmin():
    if request.method == 'POST':
        try:
            usuario = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            rol = request.form.get('role')
            fecha_actual = datetime.now()  # Genera la fecha actual

            if not all([usuario, email, password, rol]):
                return "Todos los campos son obligatorios", 400

            cur = miConexion.cursor()
            cur.execute(
                "INSERT INTO usuarios (nombre_usuario, email, password, fecha_registro, rol) VALUES (%s,%s, %s, %s, %s)",
                (usuario, email, generate_password_hash(password), fecha_actual, rol)
            )
            miConexion.commit()
            cur.close()
            print("Datos Registrados")
            return render_template('Registrousuario.html') # Redirige a una página de éxito
        except Exception as e:
            print(f"Error en la base de datos: {e}")
            miConexion.rollback()
            return "Error interno del servidor", 500



if __name__ == '__main__':
     app.run(port = 3000, debug = True) 