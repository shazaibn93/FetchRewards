from app import app
from .models import Transaction
from .forms import TransactionForm, SpendForm
from datetime import datetime as dt 
from flask import render_template, render_template, request

# Homepage
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

# Page with a form that allows you to enter payer and points. Submitting creates a transaction.
# Transactions are saved in a list (Environment Variable) and are displayed under the form on the same page
@app.route('/transactions', methods=['GET','POST'])
def transactions():
    t=Transaction()
    form=TransactionForm()
    if request.method == 'POST' and form.validate_on_submit():
        tempdict = {
            'payer':request.form.get('payer'),
            'points':int(request.form.get('pointsgained')),
            'now':dt.now().strftime("%d/%m/%Y, %H:%M:%S"),

        }
        t.list.append(tempdict)
        app.config['ENVIRONMENT_VAR'] = t.list
        return render_template('transactions.html.j2', form=form, transactions = t.list )
    return render_template('transactions.html.j2', form=form)

# This route sums the points of all transactions saved in Environment Var
@app.route('/sum', methods=['GET'])
def sum():
    totalpoints = 0
    for t in app.config['ENVIRONMENT_VAR']:
        totalpoints += int(t['points'])
    return render_template('sum.html.j2', tp = totalpoints)

# This route iterates through the Environment Var and gets total points by payee. The payee and their total are 
# saved to a new Environment Var
@app.route('/breakout', methods=['GET'])
def breakout():
    individuals = {}
    for payer in app.config['ENVIRONMENT_VAR']:
        totalpoints = 0
        for test in app.config['ENVIRONMENT_VAR']:
            if payer['payer'] == test['payer']:
                totalpoints += test['points']
        individuals[payer['payer']] = totalpoints
    app.config['TOTALS_DICT'] = individuals
    return render_template('breakout.html.j2', individuals = individuals)

# This route goes through the transactions and "spends" the points. I didn't want to touch the transactions and so I 
# subtracted totals from the payee in the second Environment Var. It should have been a list but I was working through 
# it as a dictionary
@app.route('/spend', methods=['GET','POST'])
def spend():
    form = SpendForm()
    if request.method == 'POST' and form.validate_on_submit():
        spend_amount = int(request.form.get('pointsspent'))
        while spend_amount > 0:
            for i in app.config['ENVIRONMENT_VAR']:
                if int(i['points']) > 0:
                    if spend_amount >= int(i['points']):
                        spend_amount-=int(i['points'])
                        app.config['TOTALS_DICT'][i['payer']] -= i['points']
                    else:
                        app.config['TOTALS_DICT'][i['payer']] -= spend_amount
                        spend_amount-=spend_amount
            return render_template('spend.html.j2', new = app.config['TOTALS_DICT'], form = form)
    return render_template('spend.html.j2', form = form)