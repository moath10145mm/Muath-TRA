from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_country_data(name):
    url = f"https://api.nationalize.io?name={name}"
    response = requests.get(url)

    if response.status_code != 200:
        return []

    data = response.json()
    results = []

    for country in data.get('country', []):
        code = country['country_id']
        probability = country['probability']

        # Get full country name
        country_url = f"https://restcountries.com/v3.1/alpha/{code}"
        res = requests.get(country_url)

        if res.status_code == 200:
            country_name = res.json()[0]['name']['common']
        else:
            country_name = f"Unknown ({code})"

        results.append({
            "name": country_name,
            "percentage": round(probability * 100, 2)
        })

    # Sort results
    results.sort(key=lambda x: x["percentage"], reverse=True)
    return results


@app.route("/", methods=["GET", "POST"])
def index():
    countries = []
    name = ""

    if request.method == "POST":
        name = request.form.get("name")
        if name:
            countries = get_country_data(name)

    return render_template("index.html", countries=countries, name=name)


if __name__ == "__main__":
    app.run(debug=True)
