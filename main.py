from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:abc123@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "1234567"

#create blog class/table with 4 columns; name and type each variable
#owner_id is foreign key linking the user's id to the blog post
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(200))
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
    
#create a user class/table with 4 columns; name and type each variable
class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref ='owner')


    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/')
def index():
    allowed_routes = ['singleUser', 'blog']
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        username_error = ""
        password_error = ""

        # TODO - validate user's data

        if len(username) < 3:
            username_error = "Invalid username"
            flash("invalid username", " error")
            # return redirect('/sorry')


        if len(password) < 3:
            password_error = "Invalid password"
            flash("invalid password", "error")
            # return redirect('/sorry')

        if not username_error or not password_error:
            pass

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            #flash("username does not exist", " error")
            return redirect('/newpost')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')


#require log in 
@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'Blog_function', 'all_users']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

#create handler for login; check email and password
@app.route('/login', methods=['POST', 'GET'])
def login():
    #if request.method == 'GET':
       # return render_template('login.html')

    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        else:
            pass
            #flash('User password incorrect, or user does not exist', 'error')
    #         pass
    # return render_template('sorry.html')
    return render_template('login.html')

#create handler for logout
@app.route('/logout')
def logout():
    del session['username']
    return redirect('/login')

@app.route('/blog', methods=['GET'])
def Blog_function():
    id = request.args.get("id")
    #new_var = "user" from request
    ind_user = request.args.get("user")

    if id != None:
        
        blog = Blog.query.get(id)

        return render_template('blogentry.html', blog=blog)

    elif ind_user != None:# new_var does not equal none:
        #query for user
        user = User.query.filter_by(username=ind_user).first()
        #render template and pass user to template
        return render_template('newtemplate.html', user=user)

    else:   
        blog = Blog.query.all()

        return render_template('blog.html', title="Blogz", blogs=blog) 

@app.route('/home', methods=['GET'])
def all_users():
    users = User.query.all()
    return render_template('singleUser.html', users=users)


@app.route('/newpost', methods=['GET','POST'])
def add_blog():
    if request.method == 'GET':
        return render_template('newpost.html', title="Let's Make a Blog!")



    if request.method == 'POST':
        blog_title = request.form['title']
        blog_body = request.form['body']
        title_error = ""
        body_error = ""
        

        if len(blog_body) < 1:
            body_error = "Invalid body"
<<<<<<< HEAD

        if len(blog_title) < 1:
            title_error = "Invalid title"

        if not title_error and not body_error:
            new_blog = Blog(blog_title, blog_body)
=======
            flash('Invalid body')


        if len(blog_title) < 1:
            title_error = "Invalid title"
            flash('Invalid title')

        if not title_error and not body_error:
            
            currentUserName = session['username']
            blog_person = User.query.filter_by(username=currentUserName).first()
            #we need to get username from the session #then we need to get the id from the database with that username
            new_blog = Blog(title=blog_title, body=blog_body, owner=blog_person) #parameter name needs to match the assigned variable you want to pass in
>>>>>>> 63c232f9a48c8f52cc5903ab6d6e11b6227139b0
            db.session.add(new_blog)
            db.session.commit()
            query_param_url = "/blog?id=" + str(new_blog.id)
            return redirect(query_param_url)

    else:
        return render_template('newpost.html',title="Let's Make a Blog!"
                                        ,title_error=title_error
                                        ,body_error=body_error)


if __name__=='__main__':
    app.run()