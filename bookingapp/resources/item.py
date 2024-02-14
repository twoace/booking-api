from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bookingapp.schemas import ItemSchema, ItemUpdateSchema
from bookingapp.models import ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from bookingapp.db import db

bp = Blueprint("items", __name__, url_prefix="/item", description="Item related operations")


@bp.route("/")
class ItemList(MethodView):
    @bp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @bp.arguments(ItemSchema)
    @bp.response(201, ItemSchema)
    def post(self, new_item):
        item = ItemModel(**new_item)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Item name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred inserting the item")
        return item
    
    
@bp.route("/<item_id>")
class Item(MethodView):
    @bp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @bp.arguments(ItemUpdateSchema)
    @bp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        if item:
            item.name = item_data["name"]
            item.capacity = item_data["capacity"]
            item.available = item_data["available"]
        else:
            item = ItemModel(id=item_id, **item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Item name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred updating the item")
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred deleting the item")
        return {"message": "Item has been deleted successfully"}
    