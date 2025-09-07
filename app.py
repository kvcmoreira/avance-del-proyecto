# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from inventory import Inventario
from producto import Producto

app = Flask(__name__)
app.secret_key = 'una_clave_secreta_muy_segura'  # Cambia esto por una clave más segura

# Inicializar inventario
inventario = Inventario()

@app.route('/')
def index():
    productos = list(inventario.productos.values())
    return render_template('index.html', productos=productos)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            id_prod = int(request.form['id'])
            nombre = request.form['nombre']
            cantidad = int(request.form['cantidad'])
            precio = float(request.form['precio'])
            producto = Producto(id_prod, nombre, cantidad, precio)
            if inventario.añadir_producto(producto):
                flash(f"Producto '{nombre}' añadido exitosamente.", "success")
            else:
                flash(f"Error: Ya existe un producto con ID {id_prod}.", "danger")
        except Exception as e:
            flash(f"Error al añadir producto: {e}", "danger")
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:id_prod>')
def delete(id_prod):
    if inventario.eliminar_producto(id_prod):
        flash("Producto eliminado correctamente.", "success")
    else:
        flash("No se encontró el producto.", "danger")
    return redirect(url_for('index'))

@app.route('/update/<int:id_prod>', methods=['GET', 'POST'])
def update(id_prod):
    producto = inventario.productos.get(id_prod)
    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for('index'))

    if request.method == 'POST':
        try:
            nueva_cantidad = request.form.get('cantidad')
            nuevo_precio = request.form.get('precio')

            cantidad = int(nueva_cantidad) if nueva_cantidad else None
            precio = float(nuevo_precio) if nuevo_precio else None

            if inventario.actualizar_producto(id_prod, cantidad, precio):
                flash("Producto actualizado correctamente.", "success")
            else:
                flash("Error al actualizar producto.", "danger")
        except Exception as e:
            flash(f"Error: {e}", "danger")
        return redirect(url_for('index'))

    return render_template('update.html', producto=producto)

@app.route('/search', methods=['GET', 'POST'])
def search():
    resultados = []
    if request.method == 'POST':
        nombre = request.form['nombre']
        resultados = inventario.buscar_por_nombre(nombre)
    return render_template('search.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)