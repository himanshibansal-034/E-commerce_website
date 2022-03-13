from flask import render_template,session,request,redirect,url_for,Blueprint,flash,abort
from shop import app, db
from flask_login import login_user, login_required, logout_user, current_user
from shop.models import User, Product
from shop.forms import RegistrationForm, LoginForm, QuantityForm, UpdateUserForm
from shop.pro_picture_handler import add_profile_pic
from shop.cart.views import *
from shop.products.views import *

shop = Blueprint('shop', __name__)

#index
@app.route('/')
def index():
    products = Product.query.order_by(Product.id.desc())
    form=QuantityForm()
    return render_template('index.html',products=products,form=form)

#register
@app.route("/register", methods=['POST','GET'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=form.password.data,
                    user_type=form.user_type.data
                    )

        db.session.add(user)
        db.session.commit()
        flash("Thank you for registering " +form.username.data+ ". Please login.")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

#login
@app.route("/login", methods=['POST','GET'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            if user.user_type == 'value':
                return AddtoCart(username=user.username)
            else:
                return view_shop(username=user.username)
    return render_template('login.html', form=form)

@app.route("/account",methods=['POST','GET'])
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.picture.data = url_for('static',filename='profile_pics/'+ current_user.profile_image)
    return render_template('account.html',form=form)
    


#logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


