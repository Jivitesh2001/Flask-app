from app import app,db
from app import mnist_fcn
from app.models import User,Post

@app.shell_context_processor
def make_shell_processor():
    return {'db':db, 'User': User, 'Post' : Post}