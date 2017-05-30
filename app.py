from flask import Flask, redirect, url_for, request, render_template, Response
import os
import json
import requests

# global variables to store repo and repo links
# repos = []
# repolink = []
# image = ""

# module to generate repo and repo links


# def repogen(user_name):
#     global repos
#     global repolink
#     global image
#     repos = []
#     repolink = []
#     # getting contents of the api for a user
#     httpob = requests.get("https://api.github.com/users/" +
#                           user_name + "/repos?per_page=100")
#     owner = requests.get("https://api.github.com/users/" + user_name)
#     owner_data = json.loads(owner.content.decode("utf-8"))
#     decob = httpob.content.decode("utf-8")
#     jsonob = json.loads(decob)
#     image = jsonob[0]['owner']['avatar_url']
#     for j in jsonob:
#         if j["fork"] is not True:  # appending only personal repos to the list
#             repos.append(j["name"])
#             repolink.append(j["html_url"])


app = Flask(__name__)


@app.route('/<name>')
def main(name):
    # generating repo and repolink list before rendering the html file
    # list to be passed while rendering & some more credentials can be added
    # repogen(name)
    # repo_dict = dict(zip(repos, repolink))
    # owner = requests.get("https://api.github.com/users/" + name)
    # owner_data = json.loads(owner.content.decode("utf-8"))
    url = "https://api.github.com/graphql"
    headers = {"Authorization":"Basic ZGlieWFkYXM6bmFuZGFEQVNAOTk="}   # headers = {"Authorization":os.environ[OUATH_KEY]}
    query = json.dumps({"query":"query{user(login: \""+name+"\") { name email avatarUrl url bio websiteUrl pinnedRepositories(first: 6) { nodes { name url } } } }"})
    r = requests.post(url,headers=headers,data=query)
    data_dict = json.loads(r.content.decode("utf-8"),sorted)
    pinned_repos = data_dict['data']['user']['pinnedRepositories']['nodes']
    image = data_dict['data']['user']['avatarUrl']
    gh_link = data_dict['data']['user']['url']
    bio = data_dict['data']['user']['bio']
    full_name = data_dict['data']['user']['name']
    email = data_dict['data']['user']['email']
    blog = data_dict['data']['user']['websiteUrl']

    x = render_template('full_temp.html', name=name ,pinned_repos=pinned_repos, image=image,
                        gh_link=gh_link, bio=bio, full_name=full_name, email=email, blog=blog)
    headers = {"Access-Control-Allow-Origin": "*", 'Content-Type': 'text/html'}
    with open("templates/"+name+".html","w") as f:
        f.write(x)
    return Response(x, 200, headers=headers)
    # return str(data_dict)


# if __name__ == "__main__":  # This is for local testin
#     app.run(host='localhost', port=3453, debug=True)


if __name__ == "__main__":  # This will come in use when
    port = int(os.environ.get("PORT", 5000))  # the app is deployed on heroku
    app.run(host='0.0.0.0', port=port,debug=True)
