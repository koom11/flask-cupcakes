from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_IMG_URL = 'https://tinyurl.com/demo-cupcake'


class Cupcake(db.Model):
    """Cupcake Model"""

    __tablename__ = "cupcakes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text,  nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, default=DEFAULT_IMG_URL)

    def serialize(self):
        """Returns a dict rep of cupcake which is jsonifiable"""
        return{
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }

    def __repr__(self):
        return f"<{self.flavor} Cupcake: Size - {self.size} Rating - {self.rating} >"
