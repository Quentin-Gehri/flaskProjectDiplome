from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired, Length
from model import Client


class ClientForm(FlaskForm):
    client_nom = StringField('Nom du Client', validators=[InputRequired(), Length(min=1, max=100)],
                             render_kw={"placeholder": "Nom du Client"})
    submit = SubmitField("Ajouter")


class ReparationForm(FlaskForm):
    clients = SelectField('Client', validators=[InputRequired()], coerce=int)
    appareil = StringField('Appareil', validators=[InputRequired(), Length(min=1, max=100)],
                           render_kw={"placeholder": "Appareil"})
    description = TextAreaField('Description', validators=[InputRequired(), Length(min=1, max=200)],
                                render_kw={"placeholder": "Description"})
    submit = SubmitField("Ajouter")

    def __init__(self, *args, **kwargs):
        super(ReparationForm, self).__init__(*args, **kwargs)
        self.clients.choices = [(client.id, client.client_nom) for client in Client.query.all()]


class ReparationFormUpdate(FlaskForm):
    appareil = StringField('Appareil', validators=[InputRequired(), Length(min=1, max=100)],
                           render_kw={"placeholder": "Appareil"})
    description = TextAreaField('Description', validators=[Length(max=200)],
                                render_kw={"placeholder": "Description"})
    statut = SelectField('Statut', choices=[
        ('A faire', 'À faire'),
        ('En cours', 'En cours'),
        ('Terminé', 'Terminé'),
        ('Repris par le client', 'Repris par le client')
    ], validators=[InputRequired()])
    submit = SubmitField("Mettre à jour")

