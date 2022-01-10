from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, SelectField,FieldList, FormField, TextField
from wtforms.validators import Required
from flask_wtf import FlaskForm


class SearchFrom (Form):
    resourcseFields = SelectField(u'Resourse', choices=[], validators=[Required()])
    keyFields = SelectField(u'Attribute', choices=[], validators=[Required()])
    condtion = SelectField(u'Operator', choices=[("equals", "equals"), ("not_equals", "not equals"), ("contains", "contains")
        , ("not_contains", "not contains"),
                                        ("gt", ">"),("gte", ">="), ("lt", "<"),
                                                 ("lte", "<=")], validators=[Required()])
    valueFields = TextField(u'Value',  validators=[Required()])



