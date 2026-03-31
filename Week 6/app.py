from flask import Flask, render_template, request, redirect, url_for
import pickle
import pandas as pd

app = Flask(__name__)

model = pickle.load(open("earthquake_model.pkl","rb"))
encoder = pickle.load(open("label_encoder.pkl","rb"))
scaler = pickle.load(open("scaler.pkl","rb"))


@app.route('/')
@app.route('/home')
def home():
   return render_template("home.html")

# Login page
@app.route('/login')
def login():
    return render_template('login.html')

# Prediction Page
@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    
    if request.method == "POST":
        cdi = float(request.form["cdi"])
        mmi = float(request.form["mmi"])
        magnitude = float(request.form["magnitude"])
        depth = float(request.form["depth"])
        sig = float(request.form["sig"])

        data = pd.DataFrame([[magnitude, depth, cdi, mmi, sig]],
                              columns=["magnitude", "depth", "cdi", "mmi", "sig"])
    
        scaled_data = scaler.transform(data)
        prediction = model.predict(scaled_data)
        alert = encoder.inverse_transform(prediction)[0].lower()

        return render_template("index.html", prediction=alert)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)