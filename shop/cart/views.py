from flask import render_template,session,request,redirect,url_for,Blueprint,flash,abort
from shop import app, db
from flask_login import current_user, login_required
from shop.models import User, Product, Cart, Order, OrderedProduct
from shop.forms import OrderForm, QuantityForm,QuantityEditForm

cart = Blueprint('cart', __name__)

#add to cart
@app.route('/<product_id>_cart',methods=['GET','POST'])
@login_required
def add_to_cart(product_id):
    if current_user.user_type=='value_two':
        abort(403)
    product=Product.query.filter_by(id=product_id).first_or_404()
    exists=Cart.query.filter_by(productid=product_id, userid=current_user.id).first()

    form=QuantityForm()

    if form.validate_on_submit():
        if exists:
            exists.quantity+=form.quantity.data
        else:
            cart=Cart(userid=current_user.id,
                      productid=product_id,
                      quantity=form.quantity.data
                     )
            db.session.add(cart)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html',form=form)

#view cart
total=0
@app.route("/<username>_AddtoCart",methods=['GET','POST'])
@login_required
def AddtoCart(username):
    if current_user.user_type=='value_two':
        abort(403)
    qform=QuantityEditForm()
    oform=OrderForm()

    user = User.query.filter_by(username=username).first_or_404()
    cart = Cart.query.filter_by(userid=current_user.id).all()
    global total
    for product in cart:
        total+=product.prod.price*product.quantity
    return render_template('cart.html',user=user,cart=cart,total=total,qform=qform,oform=oform)

#edit cart
@app.route("/<product_id>_edit_cart",methods=['GET','POST'])
@login_required
def edit_cart(product_id):
    if current_user.user_type=='value_two':
        abort(403)
    editpro=Cart.query.filter_by(userid=current_user.id, productid=product_id).first()

    qform=QuantityEditForm()
    
    if qform.validate_on_submit():
        editpro.quantity=qform.quantity.data
        db.session.commit()
        return redirect(url_for('AddtoCart', username=current_user.username))

#checkout
@app.route("/checkout",methods=['GET','POST'])
@login_required
def checkout():
    if current_user.user_type=='value_two':
        abort(403)
    qer=Cart.query.filter_by(userid=current_user.id).first()
    pro=Product.query.filter_by(id=qer.productid).first()
    oform = OrderForm()
    global total

    if oform.validate_on_submit():
        order=Order(total_price=total,
                    name=oform.name.data,
                    address=oform.address.data,
                    phone=oform.phone.data,
                    sell_id=pro.sell_id)
        db.session.add(order)
        db.session.commit()
        prod=Cart.query.filter_by(userid=current_user.id).all()
        last_order=Order.query.filter_by(userid=current_user.id).first()
        for pr in prod:
            dec=Product.query.filter_by(id=pr.productid).first()
            dec.quantity-=pr.quantity
            ordproduct=OrderedProduct(orderid=last_order.id,
                                     productid=pr.productid,
                                     quantity=pr.quantity)
            db.session.add(ordproduct)
            db.session.delete(pr)
            db.session.commit()
        total=0
        
    return redirect(url_for('index'))
