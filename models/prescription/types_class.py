"""
Describes the types of administration of medical prescriptions
"""
from api.v1 import db
from models.base_model import BaseModel


class PrescribableItemType(BaseModel, db.Model):
    __tablename__ = 'prescribable_item_types'

    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    code = db.Column(db.String(20))  # SNOMED / ATC / custom
    code_system = db.Column(db.String(50))  # e.g., 'SNOMED', 'WHO-ATC'
