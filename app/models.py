from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="operador")
    password_hash = db.Column(db.String(255), nullable=False)

    requisitions = db.relationship("Requisition", back_populates="requester")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def can_manage_materials(self):
        return self.role in ["supervisor", "almoxarifado"]

    @property
    def can_update_status(self):
        return self.role in ["supervisor", "almoxarifado"]


class Material(db.Model):
    __tablename__ = "materials"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(200), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    consumption_per_unit = db.Column(db.Float, nullable=False, default=1)
    active = db.Column(db.Boolean, default=True, nullable=False)

    items = db.relationship("RequisitionItem", back_populates="material")


class Requisition(db.Model):
    __tablename__ = "requisitions"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    requester_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    line = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    production_goal = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    status = db.Column(db.String(30), nullable=False, default="Pendente")

    requester = db.relationship("User", back_populates="requisitions")
    items = db.relationship("RequisitionItem", back_populates="requisition", cascade="all, delete-orphan")


class RequisitionItem(db.Model):
    __tablename__ = "requisition_items"

    id = db.Column(db.Integer, primary_key=True)
    requisition_id = db.Column(db.Integer, db.ForeignKey("requisitions.id"), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey("materials.id"), nullable=False)
    available_qty = db.Column(db.Float, nullable=False)
    needed_qty = db.Column(db.Float, nullable=False)
    request_qty = db.Column(db.Float, nullable=False)

    requisition = db.relationship("Requisition", back_populates="items")
    material = db.relationship("Material", back_populates="items")
