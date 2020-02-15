from flask import Flask, render_template, redirect, url_for, request, jsonify
import pyrebase
import requests
import json
import pprint

config = {
  "apiKey": "AIzaSyBFSeIw9rHMwh59tlEbAM3fcjVPL2ieu70",
  "authDomain": "cpai-bf71c.firebaseapp.com",
  "databaseURL": "https://cpai-bf71c.firebaseio.com",
  "projectId": "cpai-bf71c",
  "storageBucket": "cpai-bf71c.appspot.com",
  "messagingSenderId": "305447636105",
  "appId": "1:305447636105:web:195858d535ea28ffb10a58",
  "measurementId": "G-C71QZDCC4E"
}


app = Flask(__name__)
firebase = pyrebase.initialize_app(config)
db = firebase.database()



@app.route('/')
def home():
    return "Welcome to CPai!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/user')
def create_new_user():
    print("Hello")
    return "hello"

@app.route('/explain_term', methods=['POST'])
def star1t():
    # maintain last city mentioned in last_city
    global last_city

    # get payload
    content = request.json

    # for print debugging
    pprint.pprint(content)
    return jsonify(content)


@app.route('/', methods=['POST'])
def start():
    # maintain last city mentioned in last_city
    global last_city

    # get payload
    content = request.json

    # for print debugging
    pprint.pprint(content)
    # resolve the slot (if it's not resolved, the platform may complain in the response)
    content['slots']['_TERMINOLOGY_']['values'][0]['resolved'] = 1

    # map it (in this case, the slot is mapped to the token)
    extract = content['slots']['_TERMINOLOGY_']['values'][0]['tokens']
    db.child("TERMINOLOGY").push({extract: "money you can get refunded if you are in a lower income bracket and/or have kids"})
    content['slots']['_TERMINOLOGY_']['values'][0]['value'] = "money you can get refunded if you are in a lower income bracket and/or have kids"

    return jsonify(content)


'''
def business_logic_explain_term():
    if request.method == 'POST':
        content = request.JSON
        pprint.pprint(content)
        # resolve the slot (if it's not resolved, the platform may complain in the response)
        #content['slots']['_TERMINOLOGY_']['values'][0]['resolved'] = -1

        # map it (in this case, the slot is mapped to the token)
        #content['slots']['_TERMINOLOGY_']['values'][0]['tokens'] = 'see_vinod_it_works'
        #content['slots']['_TERMINOLOGY_']['values'][0]['value'] = 'see_vinod_it_works'

        #content['state'] = 'explain_instructions'


        the_city = 'debbie_downer'
        # resolve the slot (if it's not resolved, the platform may complain in the response)
        content['slots']['_TERMINOLOGY_']['values'][0]['resolved'] = 1


        # map it (in this case, the slot is mapped to the token)
        content['slots']['_TERMINOLOGY_']['values'][0]['value'] = the_city
        content['slots']['_TERMINOLOGY_']['values'][0]['tokens'] = 'bro_whatever'

        return jsonify(content)
'''
@app.route('/term')
def add_tax_terminology():
    term = 'deduction'
    def_attempt = retrieve_tax_definition(term).pyres
    if def_attempt == None:
        db.child('terminology').push({term: 'savings'})
    else:
        print("Term already in database")

    return "Term " + term + " in database"

def retrieve_tax_definition(term):
    if db.child('terminology').get() == None:
        print("Tax definition not in database")
        return None
    else:
        return db.child('terminology').get()

if __name__ == "__main__":
    app.run(port=5000, debug=True)
