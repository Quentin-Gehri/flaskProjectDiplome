from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import CSRFProtect
from form import ReparationForm, ClientForm, ReparationFormUpdate
from model import db, Client, Reparation

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reparations.db'
app.config['SECRET_KEY'] = 'reparateur'
csrf = CSRFProtect(app)
csrf.init_app(app)
db.init_app(app)
app.app_context().push()
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html', client_form=ClientForm(), reparation_form=ReparationForm(),
                           reparations=Reparation.fetch_reparations(), reparation_form_update=ReparationFormUpdate())


@app.route('/ajouter_client', methods=['POST'])
def ajouter_client():
    form = ClientForm()
    if form.validate_on_submit():
        client_nom = form.client_nom.data
        if not client_nom:
            flash('Le nom du client ne peut pas être vide', 'error')
            return redirect(url_for('index'))
        Client.create_client(client_nom)
    else:
        flash('Échec de validation du formulaire', 'error')
    return redirect(url_for('index'))


@app.route('/ajouter_reparation', methods=['POST'])
def ajouter_reparation():
    form = ReparationForm()
    if form.validate_on_submit():
        client_id = form.clients.data
        if not client_id:
            flash('Le nom du client ne peut pas être vide', 'error')
            return redirect(url_for('index'))
        if client_id is None:
            flash('Le client n\'existe pas', 'error')
            return redirect(url_for('index'))
        appareil = form.appareil.data
        description = form.description.data
        if not appareil or not description:
            flash('L\'appareil et la description ne peuvent pas être vides', 'error')
            return redirect(url_for('index'))
        Reparation.create_reparation(client_id, appareil, description)
    else:
        flash('Échec de validation du formulaire', 'error')
    return redirect(url_for('index'))


@app.route('/update_repair/<int:reparation_id>', methods=['POST'])
def update_repair(reparation_id):
    form = ReparationFormUpdate(request.form)
    if form.validate_on_submit():
        appareil = form.appareil.data
        description = form.description.data
        statut = form.statut.data
        if Reparation.update_reparation(reparation_id, appareil, description, statut) is not None:
            return redirect(url_for('index'))
        else:
            flash('Échec de validation du formulaire', 'error')
    else:
        flash('Échec de validation du formulaire', 'error')
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
