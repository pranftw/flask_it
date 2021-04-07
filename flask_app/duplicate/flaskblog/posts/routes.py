from flask import url_for,render_template,Blueprint,flash,redirect,request,abort
from flaskblog.models import Post
from flaskblog import db
from flask_login import current_user,login_required
from flaskblog.posts.forms import PostForm,UpdatePostForm


posts = Blueprint('posts',__name__)

@posts.route("/<username>/post/new",methods=['GET','POST'])
@login_required
def new_post(username):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post created!","success")
        return redirect(url_for('main.home'))
    return render_template("new_post.html",title="New Post",form=form)

@posts.route("/<username>/post/<id>")
def post_page(username,id):
    post = Post.query.filter_by(id=id).first()
    return render_template("post_page.html",title="Post",post=post)

@posts.route("/<username>/post/update/<id>",methods=['GET','POST'])
@login_required
def update_page(username,id):
    post = Post.query.filter_by(id=id).first()
    if(post is not None):
        if((post.author.username != current_user.username)):
            abort(403)
        elif(post.author.username!=username):
            abort(403)
        form = UpdatePostForm()
        if(form.validate_on_submit()):
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("Post updated!","success")
            return redirect(url_for('posts.post_page',username=post.author.username,id=post.id))
        elif(request.method=='GET'):
            form.title.data = post.title
            form.content.data = post.content
        return render_template("update_page.html",title="Update",post=post,form=form)
    else:
        flash("Post unavailable!")
        return redirect(url_for('main.home'))

@posts.route("/<username>/post/delete/<id>")
@login_required
def delete_page(username,id):
    post = Post.query.filter_by(id=id).first()
    if(post is not None):
        if((post.author.username != current_user.username)):
            abort(403)
        elif(post.author.username!=username):
            abort(403)
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted!","success")
        return redirect(url_for('main.home'))
    else:
        flash("Post unavailable!")
        return redirect(url_for('main.home'))
