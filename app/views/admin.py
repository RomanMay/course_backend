from functools import wraps

from app.forms import OfferForm

from flask import redirect, request
from flask import Blueprint
from flask import render_template

from app.models import Offer, Order, User
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


@admin.route('/confirm_order', methods=['POST'])
@login_required
@admin_required
def confirm_order():
    order_id = request.form['order_id']
    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return 'Order does not exist.'
    if order.status == 'canceled':
        return 'Error. User not want this order'
    if order.status == 'accepted':
        return 'Error. Order already accepted'
    order.status = 'accepted'
    db_session.add(order)
    db_session.commit()
    return 'ok'


@admin.route('/reject_order', methods=['POST'])
@login_required
@admin_required
def reject_order():
    order_id = request.form['order_id']
    order = Order.query.filter_by(id=order_id).first()
    if not order:
        return 'Order does not exist.'
    if order.status == 'canceled':
        return 'Error. User not want this order'
    if order.status == 'rejected':
        return 'Error. Order already rejected'
    order.status = 'rejected'
    db_session.add(order)
    db_session.commit()
    return 'ok'


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
        return redirect('/admin_panel')
    return render_template('admin/add_offer.html', form=form)


@admin.route('/admin_panel')
@login_required
@admin_required
def admin_panel():
    all_orders = Order.query.all()
    cost = 0
    ab_name = ""
    res = []
    for order in all_orders:
        offer = Offer.query.filter_by(id=order.offer_id).first()
        count_of = Order.query.filter_by(offer_id=offer.id, status='accepted').count()
        tcost = count_of * offer.cost
        res.append({
            'user': User.query.filter_by(id=order.user_id).first(),
            'order': order,
            'offer': Offer.query.filter_by(id=order.offer_id).first(),
            'status': order.status
        })
        if tcost > cost:
            ab_name = offer.name
            cost = tcost
    return render_template('admin/admin_panel.html', offers=Offer.query.all(), orders=res, most_ab_name=ab_name, most_ab_cost=cost)


@admin.route('/archive')
@login_required
@admin_required
def archive():
    return render_template('admin/archive.html', orders=Order.query.all())
