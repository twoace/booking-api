from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)


class UserUpdateSchema(Schema):
    name = fields.Str()


class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    capacity = fields.Int(required=True)
    available = fields.Int(required=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    capacity = fields.Int()
    available = fields.Int()


class PlainBookingSchema(Schema):
    id = fields.Str(dump_only=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)


class BookingUpdateSchema(Schema):
    start_date = fields.DateTime()
    end_date = fields.DateTime()


class BookingSchema(PlainBookingSchema):
    user_id = fields.Str(required=True)
    item_id = fields.Str(required=True)
    item = fields.Nested(PlainItemSchema(), dump_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)


class ItemSchema(PlainItemSchema):
    bookings = fields.List(fields.Nested(PlainBookingSchema()), dump_only=True)


class UserSchema(PlainUserSchema):
    bookings = fields.List(fields.Nested(PlainBookingSchema()), dump_only=True)


