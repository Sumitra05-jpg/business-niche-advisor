from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)
model = joblib.load(os.path.join('model', 'business_model.pkl'))

@app.route("/", methods=["GET", "POST"])
def home():
    prediction = ""
    if request.method == "POST":
        population = int(request.form['population'])
        income = int(request.form['income'])
        
        pred = model.predict([[population, income]])[0]
        mapping = {0: "Modern Business", 1: "Agriculture", 2: "Service Sector"}
        prediction = mapping.get(pred, "Unknown")
        
    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
