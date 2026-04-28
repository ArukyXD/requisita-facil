from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Material, Requisition, RequisitionItem

requisitions_bp = Blueprint("requisitions", __name__, url_prefix="/requisitions")

VALID_STATUSES = ["Pendente", "Aprovada", "Separada", "Entregue", "Cancelada"]


@requisitions_bp.route("/")
@login_required
def index():
    requisitions = Requisition.query.order_by(Requisition.id.desc()).all()
    return render_template("requisitions/index.html", requisitions=requisitions)


@requisitions_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    materials = Material.query.filter_by(active=True).order_by(Material.description.asc()).all()

    if request.method == "POST":
        production_goal = float(request.form["production_goal"])

        requisition = Requisition(
            requester_id=current_user.id,
            line=request.form["line"].strip(),
            sector=request.form["sector"].strip(),
            production_goal=production_goal,
            notes=request.form.get("notes", "").strip(),
            status="Pendente",
        )

        db.session.add(requisition)
        db.session.flush()

        for material in materials:
            raw_available = request.form.get(f"available_{material.id}")
            if raw_available is None or raw_available == "":
                continue

            available_qty = float(raw_available)
            needed_qty = production_goal * material.consumption_per_unit
            request_qty = max(needed_qty - available_qty, 0)

            if request_qty > 0:
                db.session.add(RequisitionItem(
                    requisition_id=requisition.id,
                    material_id=material.id,
                    available_qty=available_qty,
                    needed_qty=needed_qty,
                    request_qty=request_qty,
                ))

        db.session.commit()
        flash("Requisição criada com sucesso.", "success")
        return redirect(url_for("requisitions.show", requisition_id=requisition.id))

    return render_template("requisitions/form.html", materials=materials)


@requisitions_bp.route("/<int:requisition_id>")
@login_required
def show(requisition_id):
    requisition = Requisition.query.get_or_404(requisition_id)
    return render_template("requisitions/show.html", requisition=requisition)


@requisitions_bp.route("/<int:requisition_id>/status", methods=["POST"])
@login_required
def update_status(requisition_id):
    if not current_user.can_update_status:
        flash("Você não tem permissão para alterar status.", "error")
        return redirect(url_for("requisitions.show", requisition_id=requisition_id))

    requisition = Requisition.query.get_or_404(requisition_id)
    status = request.form.get("status")

    if status not in VALID_STATUSES:
        flash("Status inválido.", "error")
        return redirect(url_for("requisitions.show", requisition_id=requisition_id))

    requisition.status = status
    db.session.commit()

    flash("Status atualizado com sucesso.", "success")
    return redirect(url_for("requisitions.show", requisition_id=requisition_id))
