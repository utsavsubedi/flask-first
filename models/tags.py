from db import db 

class Items(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    store_id = db.Column(db.ForeignKey("stores.id"), back_populates="stores", nullable=False)
    store = db.relationship("Store", back_populates="tags")
