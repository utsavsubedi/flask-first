from db import db 


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=True, unique=False)
    store = db.relationship("StoreModel", back_populates="items")
