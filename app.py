from flask import Flask,render_template,request,redirect,url_for
import os
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    def __repr__(self) -> str:
        #return super().__repr__()
        return f'<Product {self.name} - available {self.quantity}>'

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        desc = request.form['description']
        img = request.form['image']


        new_product = Product(name=name, price=price, description=desc, quantity=quantity, image_url=img)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('list_products'))
    
    return render_template('add_products.html')


@app.route('/catalog')
def list_products():
    products = Product.query.all()  # Recupera todos los productos de la base de datos
    return render_template('list_products.html', products=products)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)  # Busca el producto por ID o devuelve un error 404 si no se encuentra
    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.description = request.form['description']
        product.image_url = request.form['image']
        product.quantity = request.form['quantity']
        
        db.session.commit()  # Guarda los cambios en la base de datos
        return redirect(url_for('list_products'))  # Redirige a la lista de productos después de actualizar
    
    return render_template('update_product.html', product=product)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)  # Busca el producto por ID o devuelve un error 404 si no se encuentra
    
    db.session.delete(product)  # Elimina el producto de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    
    return redirect(url_for('list_products'))  # Redirige a la lista de productos después de eliminar

#routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/client3')
def client():
    prod= Product.query.all()
    return render_template('client3.html',products=prod)

@app.route('/login')
def login():
    return render_template('login.html')
if __name__== '__main__' :
    app.run(debug=True)

