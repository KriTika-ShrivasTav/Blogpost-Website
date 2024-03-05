from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import flash
from flask_login import LoginManager, login_user, UserMixin, logout_user
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'thisissecret'
# SECRET_KEY = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
app.app_context().push()

# migrate = Migrate(app, db)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    lastname = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    # firstname = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    address= db.Column(db.String(20), nullable=False)

    def __repr__(self):
       return '<User %r>' % self.username
    

class Blog(db.Model):
    blog_id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    author = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    pub_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __repr__(self):
       return '<Blog %r>' % self.title

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))    
 
@app.route('/')
def index():
    data = Blog.query.all()
    return render_template('index.html', data=data)

@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        address = request.form.get('address')
        email = request.form.get('email')
        username= request.form.get('username')
        password = request.form.get('password')
        
        user = User(firstname=firstname,lastname=lastname,email=email,username=username,password=password,address=address)
        db.session.add(user)
        db.session.commit()
        flash('User credentials are successfully saved', 'success')
        return redirect('/login')
    

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':   
        username= request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and password == user.password:
            login_user(user)
            return redirect('/')
        else:
            return redirect('/login')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

@app.route('/blogpost', methods=['GET', 'POST'])
def blogpost():
    if request.method=='POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        blog = Blog(title = title, author = author, content = content)
        db.session.add(blog)
        db.session.commit()
        flash('your post has been submitted', 'success')
        return redirect('/')
    return render_template('/blog.html')

@app.route('/blog_detail/<int:id>', methods=['GET', 'POST'])
def blogdetail(id):
    blog = Blog.query.get(id)
    return render_template('/blog_detail.html', blog=blog)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash('post has been deleted', 'success')
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    blog = Blog.query.get(id)
    if request.method == 'POST':
        blog.title = request.form.get('title')
        blog.author = request.form.get('author')
        blog.content = request.form.get('content')
        db.session.commit()
        flash('post has been Updated', 'success')
        return redirect('/')
    return render_template('/edit.html', blog=blog)

if __name__ ==  '__main__':
    app.run(debug=True)