from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Reparation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    appareil = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_depot = db.Column(db.Date, nullable=False, default=date.today)
    statut = db.Column(db.String(50), nullable=False, default='A faire')

    @staticmethod
    def create_reparation(client_id, appareil, description):
        reparation = Reparation(client_id=client_id, appareil=appareil, description=description)
        db.session.add(reparation)
        db.session.commit()
        return reparation

    @staticmethod
    def fetch_reparations():
        return Reparation.query.all()

    @staticmethod
    def update_reparation(reparation_id, appareil=None, description=None, statut=None):
        reparation = Reparation.query.get(reparation_id)
        if reparation:
            if appareil is not None:
                reparation.appareil = appareil
            if description is not None:
                reparation.description = description
            if statut is not None:
                reparation.statut = statut
            db.session.commit()
            return reparation
        return None


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_nom = db.Column(db.String(100), nullable=False, unique=True)
    reparations = db.relationship('Reparation', backref='client', lazy=True)

    @staticmethod
    def create_client(client_nom):
        client = Client(client_nom=client_nom)
        db.session.add(client)
        db.session.commit()
        return client
