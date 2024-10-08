from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import Store
from ..schemas import StoreSchema

blp = Blueprint("Stores", __name__, description="Operations on Store")

@blp.route("/store/<int:store_id>")
class StoreResource(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = Store.query.get_or_404(store_id, description="The requested store couldn't be found.")
        return store

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = Store.query.get_or_404(store_id, description="The requested store couldn't be found.")

        store.name = store_data['name']
        store.description = store_data['description']
        
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred: {str(e)}")
        return store, 200

    @blp.response(204)
    def delete(self, store_id):
        store = Store.query.get_or_404(store_id, description="The requested store couldn't be found.")

        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred: {str(e)}")
        return {"message": "Store was deleted successfully."}, 204

@blp.route("/stores")
class StoreListResource(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return Store.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = Store(name=store_data['name'], description=store_data['description'])

        try:
            db.session.add(store)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occurred: {str(e)}")
        return store, 201
