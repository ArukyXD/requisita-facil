from app import create_app
from app.extensions import db
from app.seed import seed_data

app = create_app()

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
        seed_data()
        print("Banco inicializado com sucesso.")
