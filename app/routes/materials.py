from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Material

materials_bp = Blueprint("materials", __name__, url_prefix="/materials")


@materials_bp.route("/")
@login_required
def index():
    materials = Material.query.order_by(Material.description.asc()).all()
    return render_template("materials/index.html", materials=materials)


@materials_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    if not current_user.can_manage_materials:
        flash("Você não tem permissão para cadastrar materiais.", "error")
        return redirect(url_for("materials.index"))

    if request.method == "POST":
        code = request.form["code"].strip()
        material = Material(
            code=code,
            description=request.form["description"].strip(),
            unit=request.form["unit"].strip(),
            sector=request.form["sector"].strip(),
            consumption_per_unit=float(request.form["consumption_per_unit"]),
            active=True,
        )

        if Material.query.filter_by(code=code).first():
            flash("Já existe material com esse código.", "error")
            return render_template("materials/form.html")

        db.session.add(material)
        db.session.commit()
        flash("Material cadastrado com sucesso.", "success")
        return redirect(url_for("materials.index"))

    return render_template("materials/form.html")
