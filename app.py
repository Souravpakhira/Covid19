from flask import Flask, jsonify, redirect, request
import json
import requests
from bs4 import BeautifulSoup
url = "https://www.mohfw.gov.in/"

app = Flask(__name__)


@app.route('/api')
def index():
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    myData = ""
    for tr in soup.find(id="cases").find_all('tr'):
        myData += tr.get_text()
    itemList = myData.split('\n\n')

    data = []
    for item in itemList[1:28]:
        data.append(item.split('\n'))

    label = ["Sr.no", "Name of State",
             "Total Confirmed cases (Indian National)", "Total Confirmed cases ( Foreign National )", "Cured", "Death"]

    l = []
    for i in data:
        d = dict(zip(label, i))
        l.append(d)
    return jsonify({"state": l})


if __name__ == '__main__':
    app.run(port='5000', debug=True)
