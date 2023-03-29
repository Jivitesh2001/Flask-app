from flask import render_template, flash, redirect, url_for,request,jsonify
from app import app,db
from app.forms import LoginForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, ImageUploadForm
from datetime import datetime
from app.forms import EditProfileForm
from app.torch_utils import transform_image, get_prediction

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
        ]
    return render_template('index.html', title='Home Page', posts=posts)


@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username= form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user,remember= form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html',title='Sign In',form = form)

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username= form.username.data, email= form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are new user!")
        return redirect(url_for('login'))
    return render_template('register.html', title = "Register",form =form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',user=user,posts=posts)

@app.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html',title='Edit Profile', form = form)

ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
def allowed_file(filename):
    # __.png
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict',methods=['POST','GET'])
@login_required
def predict():
    # print(url_for('predict',_methods='get'))
    form = ImageUploadForm()
    if request.method == 'GET':
        return render_template('mnist_predict.html',title= 'MNIST',form =form)
    if request.method == 'POST':
        file = request.files.get('file') or form.image.data
        print(type(file))
        if file is None or file.filename =='':
            flash('Please upload a file')
            return redirect(url_for('predict'))
        if not allowed_file(file.filename):
            flash('Please upload a file with jpg, jpeg, png format')
            return redirect(url_for('predict'))
        try:
            img_bytes = file.read()
            tensor = transform_image(img_bytes)
            prediction = get_prediction(tensor)
            data = {'prediction':prediction.item(),'class_name': str(prediction.item())}
            return render_template('predictions.html',title = 'Predictions',data = data)    
        except Exception as e:
            print(e)
            return render_template('500.html')
        

    return render_template('mnist_predict.html',title= 'MNIST',form =form)
    
