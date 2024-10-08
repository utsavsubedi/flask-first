from db import db 


class Store(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    items = db.relationship("Item", back_populates="stores", lazy="dynamic", cascade="all, delete")