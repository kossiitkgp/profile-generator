from flask import Flask, redirect, url_for, request, render_template
from urllib.request import urlopen
import json

repos=[]
repolink=[]
def repogen(user_name):
    global repos
    global repolink
    httpob=urlopen("https://api.github.com/users/"+user_name+"/repos")
    decob=httpob.read().decode("utf-8")
    jsonob=json.loads(decob)
    #print(jsonob)
    for j in jsonob:
        if str(j["fork"])=="False":
            #print(j["full_name"]+"\n")
            #print("https://www.github.com/"+j["full_name"])
            repos.append(j["full_name"])
            repolink.append("https://www.github.com/"+j["full_name"])

app = Flask(__name__)


@app.route('/<name>')
def main(name):
    global repos
    global repolink
    repogen(name)
    return render_template('test.html', name=name)


if __name__ == "__main__":  # This is for local testing
    app.run(host='localhost', port=3453, debug=True)

# if __name__ == "__main__":  # This will come in use when
#     port = int(os.environ.get("PORT", 5000))  # the app is deployed on heroku
#     app.run(host='0.0.0.0', port=port)
