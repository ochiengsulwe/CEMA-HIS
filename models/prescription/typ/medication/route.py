"""
Describes administration routes
"""
from api.v1 import db
from models.base_model import BaseModel


class AdministrationRoute(BaseModel, db.Model):
    __tablename__ = 'administration_routes'

    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    code = db.Column(db.String(20))
    code_system = db.Column(db.String(50))
