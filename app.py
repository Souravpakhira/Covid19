from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
import json
import requests
from bs4 import BeautifulSoup
url = "https://www.mohfw.gov.in/"

app = Flask(__name__)
CORS(app)
# app.config['JSON_SORT_KEYS'] = False


@app.route('/')
def index():
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    myData = ""
    for tr in soup.find(id="cases").find_all('tr'):
        myData += tr.get_text()

    myData = myData.split('\n')

    res = []
    for i in range(len(myData)):
        if myData[i]:
            res.append(myData[i])

    final = []
    i = 5
    while i < len(res)-7:
        temp = []
        for j in range(5):
            temp.append(res[i+j])
        final.append(temp[:])
        i += 5

    label = ["Sr.no", "Name of State",
             "Total Confirmed cases (Indian National)", "Total Confirmed cases ( Foreign National )", "Cured", "Death"]

    l = []
    for i in final:
        d = dict(zip(label, i))
        l.append(d)
    return jsonify({"state": l})


if __name__ == '__main__':
    app.run(debug=True)
