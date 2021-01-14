from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

connect_db(app)


@app.route('/')
def show_home():
    """Renders HTML page of all cupcakes"""
    cupcakes = Cupcake.query.all()
    return render_template("home.html", cupcakes=cupcakes)


@app.route('/api/cupcakes')
def show_all_cupcakes():
    """Returns JSON with all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake and respond with JSON"""
    new_cake = Cupcake(flavor=request.json["flavor"], size=request.json["size"],
                       rating=request.json["rating"], image=request.json["image"])
    db.session.add(new_cake)
    db.session.commit()
    resp_json = jsonify(cupcake=new_cake.serialize())
    return (resp_json, 201)


@app.route('/api/cupcakes/<int:id>')
def show_one_cupcake(id):
    """Display JSON for one cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Update individual cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Delete cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Cupcake deleted.")
