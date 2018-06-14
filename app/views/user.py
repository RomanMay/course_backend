from flask import redirect, request
from flask import Blueprint
from flask import render_template

from app.models import User, Offer, Order
from app.database import db_session

from flask_login import login_required, current_user, logout_user

user = Blueprint('user', __name__, template_folder='templates', static_folder='static', static_url_path='/static')


@user.route('/personal_room')
@login_required
def personal_room():
    orders = Order.query.filter_by(user_id=current_user.id)
    res = []
    for order in orders:
        res.append({
            'status': order.status,
            'offer': Offer.query.filter_by(id=order.offer_id).first()
        })
    return render_template('user/personal_room.html',
                           offers=Offer.query.all(), my_abonnements=res, user=current_user)


@user.route('/add_order', methods=['POST'])
@login_required
def add_order():
    offer_id = int(request.form['offer_id'])
    offer = Offer.query.filter_by(id=offer_id).first()

    if not offer:
        return 'Offer not exists'
    order = Order.query.filter_by(offer_id=offer.id, user_id=current_user.id).first()

    if order:
        if order.status == 'pending':
            return 'ok'
        if order.status == 'confirmed':
            return 'Order already confirmed'
        if order.status == 'canceled':
            order.status = 'pending'
            db_session.add(order)
            db_session.commit()
        if order.status == 'rejected':
            return 'Error. Order rejected'
        return 'ok'
    db_session.add(Order(current_user.id, offer.id, 'pending'))
    db_session.commit()
    return 'ok'


@user.route('/cancel_order', methods=['POST'])
@login_required
def cancel_order():
    offer_id = int(request.form['offer_id'])
    user_order = Order.query.filter_by(user_id=current_user.id, offer_id=offer_id).first()

    if not user_order:
        return 'Error. Not found order'
    if user_order.status == 'canceled':
        return 'ok'
    if user_order.status == 'rejected':
        return 'Error. Order rejected'

    user_order.status = 'canceled'
    db_session.add(user_order)
    db_session.commit()
    return 'ok'


@user.route('/check_user', methods=['GET'])
@login_required
def check_user():
    return "Hello user: " + str(current_user.username) + " : " + str(current_user.email)


@user.route('/logout', methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db_session.add(user)
    db_session.commit()
    logout_user()
    return redirect('/')
