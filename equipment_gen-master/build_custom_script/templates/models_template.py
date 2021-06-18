from config import db, ma

# [plural]
class [ModelName](db.Model):
    __tablename__ = "[plural]"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    description = db.Column(db.String(64))
    [additional_params]

class [ModelName]Schema(ma.ModelSchema):
    class Meta:
        model = [ModelName]
        sqla_session = db.session
