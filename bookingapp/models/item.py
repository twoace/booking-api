from bookingapp.db import db
from sqlalchemy.orm import validates


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Integer, nullable=False)

    @validates("available")
    def validate_available(self, key, available):
        if available < 0 or available > self.capacity:
            raise ValueError(f"Item available must be between 0 and {self.capacity}")
        return available

    bookings = db.relationship("BookingModel", back_populates="item", lazy="dynamic", cascade="all, delete")

