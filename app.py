from flask import Flask, redirect, url_for, request, render_template
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
    
    # getting contents of the api for a user
    httpob=requests.get("https://api.github.com/users/"+user_name+"/repos?per_page=100")
    # decoding the http object recieved
    decob=httpob.content.decode("utf-8")
    # converting to json
    jsonob=json.loads(decob)
    image = jsonob[0]['owner']['avatar_url']
    # appending only personal repos to the list
    for j in jsonob:
        if j["fork"] != True:
            repos.append(j["full_name"])
            repolink.append("https://www.github.com/"+j["full_name"])
            

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
    return "True"


if __name__ == "__main__":  # This is for local testing
    app.run(host='localhost', port=3453, debug=True)

# if __name__ == "__main__":  # This will come in use when
#     port = int(os.environ.get("PORT", 5000))  # the app is deployed on heroku
#     app.run(host='0.0.0.0', port=port)
