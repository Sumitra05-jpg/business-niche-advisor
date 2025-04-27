from flask import Flask, render_template, request
import joblib
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
app = Flask(__name__)
model = joblib.load(os.path.join('model', 'business_model.pkl'))

@app.route("/", methods=["GET", "POST"])
def home( ):
   prediction = None
   pie_base64 = None
   bar_base64 = None


if request.method == "POST":
        population = int(request.form['population'])
        income = int(request.form['income'])

        pred = model.predict([[population, income]])[0]
        mapping = {0: "Modern Business", 1: "Agriculture", 2: "Service Sector"}
        prediction = mapping.get(pred, "Unknown")


         # Create a pie chart
        labels = ['Population', 'Income']
        sizes = [population, income]
        colors = ['#ff9999', '#66b3ff']
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')

        # Save pie chart to buffer
        pie_buf = io.BytesIO()
        plt.savefig(pie_buf, format='png')
        pie_buf.seek(0)
        pie_base64 = base64.b64encode(pie_buf.getvalue()).decode('utf-8')
        plt.close()

        # Create a bar graph
        fig2, ax2 = plt.subplots()
        ax2.bar(labels, sizes, color=colors)
        ax2.set_ylabel('Values')
        ax2.set_title('Population vs Income')

        # Save bar chart to buffer
        bar_buf = io.BytesIO()
        plt.savefig(bar_buf, format='png')
        bar_buf.seek(0)
        bar_base64 = base64.b64encode(bar_buf.getvalue()).decode('utf-8')
        plt.close()
    
 


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)



