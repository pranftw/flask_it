from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import DataRequired,Length

class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(min=1,max=100)])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Post')

class UpdatePostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(min=1,max=100)])
    content = TextAreaField('Content',validators=[DataRequired()])
    submit = SubmitField('Update')
