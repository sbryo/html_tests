import os
import cmd
from pymongo import MongoClient
import flask
from flask import url_for,request,session,redirect
import subprocess
import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection
import json
import dropbox
import functools
import urllib
import urllib2
import requests
from flask_oauth import OAuth
from flask.ext.compress import Compress
import random
from bson.objectid import ObjectId
from validate_email import validate_email
from flask_mail import Mail
from flask_mail import Message
import string
import smtplib


app = flask.Flask(__name__)

@app.route("/accept_signup/<ID>", methods=['GET','POST'])
def accept(ID):
	client = MongoClient('ds019254.mlab.com', 19254)
    	client.users.authenticate('shakedinero','a57821688')
    	db = client.users
    	collection = db.users
    	cursor = db.users.find()
	for doc in cursor:
        	if doc['ID'] == ID:
            		mongo_id=doc['_id']
            		post = collection.find_one({"_id":mongo_id})
            		post['ID'] = "0"
            		collection.update({'_id':mongo_id}, {"$set": post}, upsert=False)
            		flask.session['username'] = doc['email']
            		return flask.redirect('/confirmed')
	return flask.redirect('/confirmed')

@app.route("/reset_password/<ID>", methods=['GET','POST'])
def reset_password(ID):
	client = MongoClient('ds019254.mlab.com', 19254)
    	client.users.authenticate('shakedinero','a57821688')
    	db = client.users
    	collection = db.users
    	cursor = db.users.find()
	for doc in cursor:
        	if str(doc['_id']) == str(ID):
                	email = str(doc['email'])
	return flask.render_template("reset_form.html",email=email)


@app.route("/reset/<EMAIL>",methods=['GET','POST'])
def reset(EMAIL):
    if ("password1" in flask.request.form) and ("password2" in flask.request.form):
        if (flask.request.form['password1']) == flask.request.form['password2']:
            password = flask.request.form['password1']
            for doc in cursor:
                if str(doc['email']) == str(EMAIL):
                    mongo_id=doc['_id']
                    post = collection.find_one({"_id":mongo_id})
                    post['password'] = password
                    collection.update({'_id':mongo_id}, {"$set": post}, upsert=False)
                    return flask.redirect('/reset_done')
        else:
            #return template "passwords not equal ! "
            return 
    else:
        #return template "please fill all the fields"
        return
    return flask.render_template("/reset_done")


@app.route("/confirmed")
def confirmed():
	return flask.render_template("confirm_signup.html")

@app.route("/reset_done")
def reset_done():
	return flask.render_template("reseted_pass.html")



if __name__ == "__main__":
    app.secret_key = "abcdefghijklmnoppqrstuvwxyz"
    app.run(port=1213, host="0.0.0.0", debug=True)

