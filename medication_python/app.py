from flask import Flask, request, render_template  
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/medicine", methods=["GET"])
def get_medicine():
    medicine = request.args.get("medicine")
    if not medicine:
        return {"error": "Medicine name is required"}, 400
    url = f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:{medicine}&limit=1"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    app.run(debug=True)