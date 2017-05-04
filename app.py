from flask import Flask, redirect, url_for, request, render_template
from urllib.request import urlopen
import json

# global variables to store repo and repo links
repos=[]
repolink=[]

# module to generate repo and repo links
def repogen(user_name):
    global repos
    global repolink
    # getting contents of the api for a user
    httpob=urlopen("https://api.github.com/users/"+user_name+"/repos")
    # decoding the http object recieved
    decob=httpob.read().decode("utf-8")
    # converting to json
    jsonob=json.loads(decob)
    # appending only personal repos to the list
    for j in jsonob:
        if str(j["fork"])=="False":
            repos.append(j["full_name"])
            repolink.append("https://www.github.com/"+j["full_name"])

app = Flask(__name__)


@app.route('/<name>')
def main(name):
    global repos
    global repolink
    # generating repo and repolink list before rendering the html file
    # list to be passed while rendering & some more credentials can be added 
    repogen(name)
    return render_template('test.html', name=name)


if __name__ == "__main__":  # This is for local testing
    app.run(host='localhost', port=3453, debug=True)

# if __name__ == "__main__":  # This will come in use when
#     port = int(os.environ.get("PORT", 5000))  # the app is deployed on heroku
#     app.run(host='0.0.0.0', port=port)
