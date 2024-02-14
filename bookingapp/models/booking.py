from bookingapp.db import db
from sqlalchemy.orm import validates
from bookingapp.models.item import ItemModel


class BookingModel(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    item = db.relationship("ItemModel", back_populates="bookings")
    user = db.relationship("UserModel", back_populates="bookings")

    @validates('item_id')
    def validate_booking(self, key, item_id):

        # Holen des Items für Update-Sperre
        item = ItemModel.query.get_or_404(item_id)

        # Reduziere den Bestand um 1
        item.available -= 1

        # Speichere die Änderungen am Item
        db.session.add(item)

        # Die Buchung wird erst nach erfolgreicher Validierung des Items hinzugefügt
        return item_id
