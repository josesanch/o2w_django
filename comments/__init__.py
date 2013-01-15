from models import CommentWithRatings
from forms import CommentFormWithRatings
#from my_comment_app.forms import CommentFormWithTitle

def get_model():
    return CommentWithRatings

def get_form():
    return CommentFormWithRatings
