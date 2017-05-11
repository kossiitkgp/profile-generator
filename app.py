from flask import Flask, redirect, url_for, request, render_template,Response
import requests
import json

# global variables to store repo and repo links
repos=[]
repolink=[]
image=""

# module to generate repo and repo links
def repogen(user_name):
    global repos
    global repolink
    global image
    repos=[]
    repolink=[]
    auth = ("dibyadas","nandaDAS@99")
    httpob=requests.get("https://api.github.com/users/"+user_name+"/repos?per_page=100",auth=auth)  # getting contents of the api for a user
    decob=httpob.content.decode("utf-8")
    jsonob=json.loads(decob)
    image = jsonob[0]['owner']['avatar_url']
    for j in jsonob:
        if j["fork"] != True:       # appending only personal repos to the list
            repos.append(j["name"])
            repolink.append(j["html_url"])
            

app = Flask(__name__)


@app.route('/<name>')
def main(name):
    # generating repo and repolink list before rendering the html file
    # list to be passed while rendering & some more credentials can be added 
    repogen(name)
    repo_dict = dict(zip(repos,repolink))
    x = render_template('temp.html', name=name ,image=image, repo_dict=repo_dict)
    with open("templates/t2.html","w") as f:
        f.write(x)
    r = Response(x,200,headers={"Access-Control-Allow-Origin":"*",'Content-Type': 'text/html'})
    return r


if __name__ == "__main__":  # This is for local testing
    app.run(host='localhost', port=3453, debug=True)

# if __name__ == "__main__":  # This will come in use when
#     port = int(os.environ.get("PORT", 5000))  # the app is deployed on heroku
#     app.run(host='0.0.0.0', port=port)
