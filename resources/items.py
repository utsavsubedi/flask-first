from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import Item
from ..schemas import ItemSchema

blp = Blueprint("Items", __name__, description="Operations on Item")

@blp.route("/item/<int:item_id>")
class ItemResource(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = Item.query.get_or_404(item_id, description="The requested item couldn't be found.")
        return item

    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = Item.query.get_or_404(item_id, description="The requested item couldn't be found.")

        item.name = item_data['name']
        item.price = item_data['price']
        item.store_id = item_data['store_id']
        
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred: {str(e)}")
        return item, 200

    @blp.response(204)
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id, description="The requested item couldn't be found.")

        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred: {str(e)}")
        return {"message": "Item was deleted successfully."}, 204

@blp.route("/items")
class ItemListResource(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return Item.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = Item(name=item_data['name'], price=item_data['price'], store_id=item_data['store_id'])

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred: {str(e)}")
        return item, 201
