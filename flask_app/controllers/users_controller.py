from flask import render_template,request,redirect
from flask_app import app

from flask_app.models.user import User


@app.route("/")
def index():
    # call the get all classmethod to get all friends
    users = User.get_all()
    print(users)
    return render_template("index.html", all_users = users)

@app.route('/user/new')
def display_new():
    return render_template("add_new_user.html")

@app.route('/create_user', methods=["POST"])
def create_user():
    #add validation after reading validation part
    if not User.is_valid_user(request.form):
        print("Validation Fail")
        return redirect('/user/new')
    print(request.form)
    id = User.save(request.form)
    return redirect(f"/user/{id}")

@app.route('/user/show_edit/<int:user_id>')
def show_edit(user_id):
    one_user = User.get_one(user_id)
    print(one_user)
    return render_template("edit_user.html", one_user=one_user)

@app.route('/edit_user', methods=["POST"])
def edit_user():
    print(request.form)
    # there is a hidden attribute being transferred through the html form
    user_id = request.form['id']
    User.update(request.form)
    return redirect(f'/user/{user_id}')


@app.route('/user/<int:user_id>')
def get_oneUser(user_id):
    
    one_user = User.get_one(user_id)
    print(one_user)
    return render_template("showOne.html", one_user=one_user)

@app.route('/user/delete/<int:user_id>')
def destroy(user_id):
    User.delete(user_id)
    return redirect('/')