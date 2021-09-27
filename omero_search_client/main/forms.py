from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, SelectField,FieldList, FormField
from wtforms.validators import Required
from flask_wtf import FlaskForm


class SearchFrom (Form):
    resourcseFields = SelectField(u'Resourse', choices=[], validators=[Required()])
    keyFields = SelectField(u'Attribute', choices=[], validators=[Required()])
    valueFields = SelectField(u'Value', choices=[], validators=[Required()])
    condtion = SelectField(u'Condition', choices=[('and', 'AND'),('not', 'NOT'),('or', 'OR')], validators=[Required()])
    #submit = SubmitField('Add condition')

