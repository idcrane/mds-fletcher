from flask_wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class DataUploadForm(Form):
    url = StringField('url', validators=[DataRequired()])
    rss_bool = BooleanField('rss_bool', default=False)
