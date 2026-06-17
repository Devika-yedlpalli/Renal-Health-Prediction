from flask import Flask, render_template, request, redirect, url_for, session
import pickle
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key

# Load the machine learning model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# User data for authentication
users = {
    'admin': generate_password_hash('admin')  # Hashed password for admin
}

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template('home.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':  # Hardcoded admin credentials
            session['username'] = username
            return redirect(url_for('input_page'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route("/input", methods=["POST", "GET"])
def input_page():
    if 'username' not in session:
        return redirect(url_for('login'))  # Ensure user is logged in

    result = None
    if request.method == "POST":
        try:
            # Collect input from the form
            Age = int(request.form["Age"])
            Bp = int(request.form['Bp'])
            Su = int(request.form['Su'])
            Rbc = int(request.form['Rbc'])
            pc = int(request.form['pc'])
            pcc = int(request.form['Thalch'])
            ba = int(request.form['Exang'])
            bgr = float(request.form['Oldpeak'])
            bu = int(request.form['Slope'])
            sod = int(request.form['Ca'])
            pot = float(request.form['Thal'])
            hemo = float(request.form['Hemo'])
            pcv = int(request.form['Pcv'])
            wc = int(request.form['Wc'])
            rc = float(request.form['Rc'])
            dm = int(request.form['Dm'])
            appet = int(request.form['Appet'])
            pe = int(request.form['Pe'])
            ane = int(request.form['Ane'])

            # Make prediction using the model
            prediction = model.predict([[Age, Bp, Su, Rbc, pc, pcc, ba, bgr, bu, sod, pot, hemo, pcv, wc, rc, dm, appet, pe, ane]])

            # Fix result mapping
            result = "High Chance of chronic kidney" if prediction[0] == 1 else "Low Chance of chronic kidney"

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("input.html", result=result)

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)
