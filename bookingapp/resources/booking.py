from flask.views import MethodView
from flask_smorest import Blueprint, abort
from bookingapp.schemas import BookingSchema, BookingUpdateSchema
from bookingapp.models import BookingModel, ItemModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from bookingapp.db import db

bp = Blueprint("bookings", __name__, url_prefix="/booking", description="Booking related operations")


@bp.route("/")
class BookingList(MethodView):
    @bp.response(200, BookingSchema(many=True))
    def get(self):
        return BookingModel.query.all()

    @bp.arguments(BookingSchema)
    @bp.response(201, BookingSchema)
    def post(self, new_booking):
        try:
            booking = BookingModel(**new_booking)
            db.session.add(booking)
            db.session.commit()
        except ValueError as ve:
            abort(400, message=str(ve))
        except SQLAlchemyError:
            abort(500, message="An error occurred inserting the booking")
        return booking


@bp.route("/<booking_id>")
class Booking(MethodView):
    @bp.response(200, BookingSchema)
    def get(self, booking_id):
        booking = BookingModel.query.get_or_404(booking_id)
        return booking

    @bp.arguments(BookingUpdateSchema)
    @bp.response(200, BookingSchema)
    def put(self, booking_data, booking_id):
        booking = BookingModel.query.get_or_404(booking_id)
        try:
            if booking:
                booking.user_id = booking_data.get("user_id", booking.user_id)
                booking.item_id = booking_data.get("item_id", booking.item_id)
                booking.start_date = booking_data.get("start_date", booking.start_date)
                booking.end_date = booking_data.get("end_date", booking.end_date)
            else:
                booking = BookingModel(id=booking_id, **booking_data)

                db.session.add(booking)
                db.session.commit()
        except IntegrityError:
            abort(400, message="Please ensure required booking data is included in the request")
        except SQLAlchemyError:
            abort(500, message="An error occurred updating the booking")
        return booking

    def delete(self, booking_id):
        booking = BookingModel.query.get_or_404(booking_id)
        item = ItemModel.query.get_or_404(booking.item_id)
        try:
            item.available += 1
            db.session.delete(booking)
            db.session.add(item)
            db.session.commit()
        except ValueError as ve:
            abort(400, message=str(ve))
        except SQLAlchemyError:
            abort(500, message="An error occurred deleting the booking")
        return {"message": "Booking has been deleted successfully"}
