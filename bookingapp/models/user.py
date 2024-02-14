from bookingapp.db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    bookings = db.relationship("BookingModel", back_populates="user", lazy="dynamic", cascade="all, delete")
