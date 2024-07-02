from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import CSRFProtect
from form import ReparationForm, ClientForm, ReparationFormUpdate, FiltreReparationForm
from model import db, Client, Reparation
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reparations.db'
app.config['SECRET_KEY'] = 'reparateur'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
csrf = CSRFProtect(app)

db.init_app(app)
app.app_context().push()
with app.app_context():
    db.create_all()


@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route('/')
def index():
    statut = session.pop('statut', 'À faire')
    return render_template('index.html', client_form=ClientForm(), reparation_form=ReparationForm(),
                           reparations=Reparation.fetch_reparations(statut=statut), filtre_form=FiltreReparationForm(),
                           reparation_form_update=ReparationFormUpdate(), statut=statut)


@app.route('/filtrer', methods=['POST'])
def filtrer():
    form = FiltreReparationForm()
    if form.validate_on_submit():
        session['statut'] = form.statuts.data
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)
    return redirect(url_for('index'))


@app.route('/ajouter_client', methods=['POST'])
def ajouter_client():
    form = ClientForm()
    if form.validate_on_submit():
        client_nom = form.client_nom.data
        client_email = form.client_email.data
        if Client.create_client(client_nom, client_email):
            flash('Client ajouté avec succès', 'success')
        else:
            flash('Ce client existe déjà', 'error')
        session['statut'] = form.statut_filtre.data
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)
    return redirect(url_for('index'))


@app.route('/ajouter_reparation', methods=['POST'])
def ajouter_reparation():
    form = ReparationForm()
    if form.validate_on_submit():
        client_id = form.clients.data
        appareil = form.appareil.data
        description = form.description.data
        Reparation.create_reparation(client_id, appareil, description)
        flash('Réparation ajoutée avec succès', 'success')
        session['statut'] = form.statut_filtre.data
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)
    return redirect(url_for('index'))


@app.route('/update_repair/<int:reparation_id>', methods=['POST'])
def update_repair(reparation_id):
    form = ReparationFormUpdate(request.form)
    if form.validate_on_submit():
        appareil = form.appareil.data
        description = form.description.data
        statut = form.statut.data
        if Reparation.update_reparation(reparation_id, appareil, description, statut) is not None:
            flash('Réparation mise à jour avec succès', 'success')
        else:
            flash('Échec de mise à jour de la réparation', 'error')
        session['statut'] = form.statut_filtre.data
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error)
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
