from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, Email
from wtforms import ValidationError
from wtforms.fields.html5 import DecimalRangeField
from flask_wtf.file import FileAllowed,FileField
from shop.models import User,Product,Cart

class RegistrationForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message="Passwords must Match!")])
    pass_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    user_type = RadioField('User Type', choices=[('value','Customer'),('value_two','Seller')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def check_email(self,email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Your email has been registered already!')
    
    def check_username(self,username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Your username has been registered already!')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddProductForm(FlaskForm):
    product_name = StringField('Product Name',validators=[DataRequired()])
    product_desc = StringField('Product Description',validators=[DataRequired()])
    quantity = IntegerField('Quantity',validators=[DataRequired()])
    price = IntegerField('Price',validators=[DataRequired()])
    picture = FileField('Product Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Item')

class QuantityForm(FlaskForm):
    quantity=IntegerField('Quantity', validators=[DataRequired()])
    submit=SubmitField('Add to cart')

class OrderForm(FlaskForm):
    name=StringField('Receiver Name', validators=[DataRequired()])
    address=TextAreaField('Address', validators=[DataRequired()])
    phone=StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Checkout')

class QuantityEditForm(FlaskForm):
    quantity=IntegerField('Quantity', validators=[DataRequired()])
    submit=SubmitField('Change Quantity')

class UpdateProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    product_desc = TextAreaField('Product Description', validators=[DataRequired()])
    quantity= IntegerField('Quantity', validators=[DataRequired()])
    price= IntegerField('Price', validators=[DataRequired()])
    picture = FileField('Update Product Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Item')

class UpdateUserForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update Account')


