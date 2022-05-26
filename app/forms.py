from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# A form to let user enter in transactions info
class TransactionForm(FlaskForm):
    payer= StringField('Payer',validators = [DataRequired()])
    pointsgained= StringField('Points Earned',validators = [DataRequired()])
    submit = SubmitField('Submit')

# A form to let user enter in amount to spend
class SpendForm(FlaskForm):
    pointsspent = StringField('Points to Spend',validators = [DataRequired()])
    submit = SubmitField('Spend')