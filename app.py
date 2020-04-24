from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
import json
import requests
from bs4 import BeautifulSoup
url = "https://www.mohfw.gov.in/"

app = Flask(__name__)
CORS(app)  # for cross site request
# app.config['JSON_SORT_KEYS'] = False

final = []
total = []
l = []
t = []


def scrape():
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    myData = ""
    for tr in soup.find(id="state-data").find_all('tr'):
        myData += tr.get_text()

    myData = myData.split('\n')

    res = []
    for i in range(len(myData)):
        if myData[i]:
            res.append(myData[i])

    global final
    final = []
    global total
    total = []
    i = 5
    while i < len(res)-7:
        temp = []
        for j in range(5):
            temp.append(res[i+j])
        final.append(temp[-4:])  # to get only last 4 element
        i += 5
    # For the last element which contain total no
    total.append(res[-5:])

    label = [
        "Name", "Confirmed", "Cured", "Death"]

    global l
    l = []
    for i in final:
        d = dict(zip(label, i))
        l.append(d)

    tlabel = ["Total_Confirmed", "Total_Cured", "Total_Death"]

    global t
    t = []
    for i in total:
        d = dict(zip(tlabel, i))
        t.append(d)


@app.route('/')
def index():
    return "use "+request.url + "state <br>" "use " + request.url + "state/[name] <br>" "use " + request.url+"total"


@app.route('/api/state')
def state_f():
    scrape()
    return jsonify({"state": l})


@app.route("/api/state/<name>")
def state(name):
    scrape()
    for i in final:
        for j in i:
            if j.lower() == name.lower():
                return jsonify({"Name": i[0], "Confirmed": i[1], "Cured": i[2], "Death": i[3]})
    return "Bad Request"


@app.route("/api")
def t_value():
    scrape()
    for i in total:
        return jsonify({"Confirmed": i[0], "Cured": i[1], "Death": i[2]})


if __name__ == '__main__':
    app.run(debug=True)
