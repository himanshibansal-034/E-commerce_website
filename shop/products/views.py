from flask import render_template,session,request,redirect,url_for,Blueprint,flash,abort
from shop import app,db
from flask_login import current_user, login_required
from shop.models import User, Product, Cart, Order, OrderedProduct
from shop.forms import AddProductForm, OrderForm, UpdateProductForm
from shop.products.picture_handler import add_product_pic

products = Blueprint('products', __name__)

#add product
@app.route("/AddProduct",methods=['GET','POST'])
@login_required
def AddProduct():
    if current_user.user_type=='value':
        abort(403)
    form = AddProductForm()
    
    if form.validate_on_submit():
        product_name = form.product_name.data
        pic=add_product_pic(form.picture.data,product_name)
        product = Product(product_name=form.product_name.data,
                          product_desc=form.product_desc.data,
                          quantity=form.quantity.data,
                          price=form.price.data,
                          product_image = pic)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html',form=form)

#update product
@app.route("/<product_id>_UpdateProduct",methods=['GET','POST'])
@login_required
def UpdateProduct(product_id):
    if current_user.user_type=='value':
        abort(403)
    product=Product.query.filter_by(id=product_id).first_or_404()

    form = UpdateProductForm()
    
    if form.validate_on_submit():

        if form.picture.data:
            product_name = form.product_name.data
            pic=add_product_pic(form.picture.data,product_name)
            product.product_image = pic

        product.product_name = form.product_name.data
        product.product_desc = form.product_desc.data
        product.quantity=form.quantity.data
        product.price=form.price.data
        db.session.commit()
        return redirect(url_for('view_shop',username=current_user.username))

    elif request.method == 'GET':
        form.product_name.data = product.product_name
        form.product_desc.data = product.product_desc
        form.quantity.data = product.quantity
        form.price.data = product.price
        form.picture.data = url_for('static', filename='product_pics/' + product.product_image)

    return render_template('update_product.html',product=product,form=form)

#delete product
@app.route("/<product_id>_DeleteProduct",methods=['GET','POST'])
@login_required
def DeleteProduct(product_id):

    product=Product.query.filter_by(id=product_id).first_or_404()

    if product.sell_id != current_user.id:
        abort(403)
    product.quantity=0
    db.session.commit()
    return redirect(url_for('view_shop', username=current_user.username))

#view shop
@app.route("/<username>_shop",methods=['GET','POST'])
@login_required
def view_shop(username):
    if current_user.user_type=='value':
        abort(403)
    user=User.query.filter_by(username=username).first_or_404()
    shop=Product.query.filter_by(sell_id=current_user.id)
    return render_template('shop.html', shop=shop, user=user)





