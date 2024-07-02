from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField, HiddenField
from wtforms.validators import InputRequired, Email, ValidationError
from model import Client

CHOIX_STATUT = [
    ('À faire', 'À faire'),
    ('En cours', 'En cours'),
    ('Terminé', 'Terminé'),
    ('Repris par le client', 'Repris par le client')
]


def validate_statut(form, field):
    if field.data not in [choice[0] for choice in CHOIX_STATUT]:
        raise ValidationError('Statut invalide')


class ClientForm(FlaskForm):
    client_nom = StringField('Nom',
                             validators=[
                                 InputRequired(message="Le nom est obligatoire")
                             ],
                             render_kw={"placeholder": "Nom"})
    client_email = StringField('Email',
                               validators=[
                                   InputRequired(message="Le mail est obligatoire"),
                                   Email(message="Le mail est invalide")
                               ],
                               render_kw={"placeholder": "Email"})
    statut_filtre = HiddenField(validators=[
                                 InputRequired(message="Le statut est obligatoire."), validate_statut
                             ],)
    submit = SubmitField("Ajouter")


class ReparationForm(FlaskForm):
    clients = SelectField('Client',
                          validators=[InputRequired(message="Le client est obligatoire.")],
                          coerce=int)
    appareil = StringField('Appareil',
                           validators=[
                               InputRequired(message="L'appareil est obligatoire.")
                           ],
                           render_kw={"placeholder": "Appareil"})
    description = TextAreaField('Description',
                                validators=[
                                    InputRequired(message="La description est obligatoire.")
                                ],
                                render_kw={"placeholder": "Description"})
    statut_filtre = HiddenField(validators=[
                                 InputRequired(message="Le statut est obligatoire."), validate_statut
                             ],)
    submit = SubmitField("Ajouter")

    def __init__(self, *args, **kwargs):
        super(ReparationForm, self).__init__(*args, **kwargs)
        self.clients.choices = [(client.id, client.client_email) for client in Client.query.all()]


class ReparationFormUpdate(FlaskForm):
    appareil = StringField('Appareil', validators=[InputRequired(message="L'appareil est obligatoire.")],
                           render_kw={"placeholder": "Appareil"})
    description = TextAreaField('Description', validators=[InputRequired(message="La description est obligatoire.")],
                                render_kw={"placeholder": "Description"})
    statut = SelectField('Statut', choices=CHOIX_STATUT, validators=[
        InputRequired(message="Le statut est obligatoire.")
    ])
    statut_filtre = HiddenField(validators=[
                                 InputRequired(message="Le statut est obligatoire."), validate_statut
                             ],)
    submit = SubmitField("Mettre à jour")


class FiltreReparationForm(FlaskForm):
    statuts = SelectField('Statut', choices=CHOIX_STATUT, validators=[InputRequired(message="Le statut est obligatoire.")])
    submit = SubmitField("Filtrer")