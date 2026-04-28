from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Requisition

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def dashboard():
    total = Requisition.query.count()
    pending = Requisition.query.filter_by(status="Pendente").count()
    delivered = Requisition.query.filter_by(status="Entregue").count()
    recent = Requisition.query.order_by(Requisition.id.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        total=total,
        pending=pending,
        delivered=delivered,
        recent=recent,
    )
