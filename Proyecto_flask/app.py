from flask import Flask, render_template, request, session
from database import conectar

app = Flask(__name__)
app.secret_key = "clave-secreta"

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/par-impar", methods=["GET", "POST"])
def par_impar():
    resultado = ""
    tipo = ""
    mensaje = ""

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM par_impar
        WHERE resultado = 'PAR'
    """)
    pares = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM par_impar
        WHERE resultado = 'IMPAR'
    """)
    impares = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM par_impar")
    total = cursor.fetchone()[0]
    if request.method == "POST":
        numero = int(request.form["numero"])
        if numero % 2 == 0:
            resultado = f"{numero} es PAR"
            tipo = "par"
            if pares < 5:
                cursor.execute("""
                    INSERT INTO par_impar (numero, resultado)
                    VALUES (%s, %s)
                """, (numero, "PAR"))
                conexion.commit()
                pares += 1
                total += 1
                mensaje = "Número par guardado correctamente."
            else:
                mensaje = "Ya tienes 5 números pares guardados."
        else:
            resultado = f"{numero} es IMPAR"
            tipo = "impar"
            if impares < 5:
                cursor.execute("""
                    INSERT INTO par_impar (numero, resultado)
                    VALUES (%s, %s)
                """, (numero, "IMPAR"))
                conexion.commit()
                impares += 1
                total += 1
                mensaje = "Número impar guardado correctamente."
            else:
                mensaje = "Ya tienes 5 números impares guardados."
    cursor.close()
    conexion.close()

    return render_template(
        "par_impar.html",
        resultado=resultado,
        tipo=tipo,
        mensaje=mensaje,
        pares=pares,
        impares=impares,
        total=total
    )

@app.route("/multiplicacion", methods=["GET", "POST"])
def multiplicacion():
    tabla = []
    numero = ""
    mensaje = ""

    if request.method == "POST":
        numero = int(request.form["numero"])

        for i in range(1, 11):
            resultado = numero * i
            tabla.append(f"{numero} x {i} = {resultado}")

        conexion = conectar()
        cursor = conexion.cursor()

        resultado_tabla = "\n".join(tabla)

        cursor.execute("""
            INSERT INTO multiplicacion (numero, resultado)
            VALUES (%s, %s)
        """, (numero, resultado_tabla))

        conexion.commit()

        cursor.close()
        conexion.close()

        mensaje = "Tabla guardada correctamente."

    return render_template(
        "multiplicacion.html",
        tabla=tabla,
        numero=numero,
        mensaje=mensaje
    )

@app.route("/adivina", methods=["GET", "POST"])
def adivina():
    mensaje = ""
    numero_secreto = 64

    if request.method == "GET":
        session["intentos"] = 0

    if "intentos" not in session:
        session["intentos"] = 0

    if request.method == "POST":
        intento = int(request.form["intento"])
        session["intentos"] += 1

        if intento < numero_secreto:
            mensaje = "Es mayor vale"
            resultado = "Menor"

        elif intento > numero_secreto:
            mensaje = "Es menor vale"
            resultado = "Mayor"

        else:
            mensaje = "¡Joa por fin! Adivinaste el número"
            resultado = "Correcto"

        conexion = conectar()
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO adivina
            (numero_secreto, intento, cantidad_intentos, resultado)
            VALUES (%s, %s, %s, %s)
        """, (
            numero_secreto,
            intento,
            session["intentos"],
            resultado
        ))
        conexion.commit()
        cursor.close()
        conexion.close()

    return render_template(
        "adivina.html",
        mensaje=mensaje,
        intentos=session["intentos"]
    )


if __name__ == "__main__":
    app.run(debug=True)