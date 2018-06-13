from functools import wraps

from app.forms import OfferForm

from flask import redirect, request
from flask import Blueprint
from flask import render_template

from app.models import Offer, Order
from app.database import db_session

from flask_login import login_required, current_user

from flask import current_app

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static', static_url_path='/static')


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_user.username not in current_app.config['ADMINS']:
            return 'You are not admin'
        else:
            return f(*args, **kwargs)

    return decorated


@admin.route('/delete_offer', methods=['POST'])
@login_required
@admin_required
def delete_offer():
    offer_name = request.form['offer_name']
    offer = Offer.query.filter_by(name=offer_name).first()
    if offer:
        db_session.delete(offer)
        db_session.commit()
        return 'ok'
    return 'Offer does not exist.'


@admin.route('/add_offer', methods=['GET', 'POST'])
@login_required
@admin_required
def add_offer():
    form = OfferForm()
    if form.validate_on_submit():
        offer = Offer.query.filter_by(name=form.name.data).first()
        if not offer:
            db_session.add(Offer(form.name.data, form.cost.data, form.description.data, form.capacity.data))
            db_session.commit()
        return redirect('/all_offers')
    return render_template('admin/add_offer.html', form=form)


@admin.route('/all_offers')
@login_required
@admin_required
def all_offers():
    return render_template('admin/all_offers.html', offers=Offer.query.all())


@admin.route('/archive')
@login_required
@admin_required
def archive():
    return render_template('admin/archive.html', orders=Order.query.all())