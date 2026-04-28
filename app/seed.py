from app.extensions import db
from app.models import User, Material


def seed_data():
    users = [
        ("admin", "Administrador", "supervisor", "admin123"),
        ("operador", "Operador da Linha", "operador", "operador123"),
        ("almox", "Almoxarifado", "almoxarifado", "almox123"),
    ]

    for username, name, role, password in users:
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, name=name, role=role)
            user.set_password(password)
            db.session.add(user)

    materials = [
        ("MAT-001", "Parafuso M6", "un", "Montagem", 4),
        ("MAT-002", "Arruela 6mm", "un", "Montagem", 4),
        ("MAT-003", "Etiqueta de identificação", "un", "Embalagem", 1),
        ("MAT-004", "Caixa de embalagem", "un", "Embalagem", 1),
        ("MAT-005", "Fita adesiva", "m", "Embalagem", 0.5),
    ]

    for code, description, unit, sector, consumption in materials:
        material = Material.query.filter_by(code=code).first()
        if not material:
            db.session.add(Material(
                code=code,
                description=description,
                unit=unit,
                sector=sector,
                consumption_per_unit=consumption,
            ))

    db.session.commit()
