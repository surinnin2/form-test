import os, redis, asyncio
from twilio.rest import Client
from flask import Flask, render_template, request, flash, redirect, session, g
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from celery import Celery
from forms import PhoneForm, UserAddForm, LoginForm, MessageForm
from models import db, User, Message, connect_db 

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///badger'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
#toolbar = DebugToolbarExtension(app)


@app.route('/', methods=['GET', 'POST'])
def homepage():

    form = MessageForm()
    template_form = PhoneForm(prefix='phone-_-') 
    
    if request.method == 'POST':
        if form.validate_on_submit():

            import pdb;
            pdb.set_trace()

            msg = Message(
                text = form.text.data,
                timestamp = datetime.utcnow(),
                queued_time = form.datetime.data
                )

            import pdb;
            pdb.set_trace()

            return render_template('test.html', form=form, msg=msg, _template=template_form)
        else: 
            return render_template('test.html', form=form, msg=form.errors, _template=template_form)
    else:
        return render_template('test.html', form=form, _template=template_form)