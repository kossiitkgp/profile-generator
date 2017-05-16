from flask import Flask, redirect, url_for, request, render_template, Response
from flask_mail import Mail, Message
import os
import json
import requests
from multiprocessing import Pool

# global variables to store repo and repo links
repos = []
repolink = []
image = ""

# module to generate repo and repo links


def repogen(user_name):
    global repos
    global repolink
    global image
    repos = []
    repolink = []
    # getting contents of the api for a user
    httpob = requests.get("https://api.github.com/users/" +
                          user_name + "/repos?per_page=100")
    owner = requests.get("https://api.github.com/users/" + user_name)
    owner_data = json.loads(owner.content.decode("utf-8"))
    decob = httpob.content.decode("utf-8")
    jsonob = json.loads(decob)
    image = jsonob[0]['owner']['avatar_url']
    for j in jsonob:
        if j["fork"] is not True:  # appending only personal repos to the list
            repos.append(j["name"])
            repolink.append(j["html_url"])


app = Flask(__name__)


@app.route('/<name>')
def main(name):
    # generating repo and repolink list before rendering the html file
    # list to be passed while rendering & some more credentials can be added
    repogen(name)
    repo_dict = dict(zip(repos, repolink))
    owner = requests.get("https://api.github.com/users/" + name)
    owner_data = json.loads(owner.content.decode("utf-8"))
    x = render_template('temp.html', name=name, image=image,
                        repo_dict=repo_dict, owner_data=owner_data)
    with open("templates/t2.html", "w") as f:
        f.write(x)
    headers = {"Access-Control-Allow-Origin": "*", 'Content-Type': 'text/html'}
    return Response(x, 200, headers=headers)


def send_mail(form_msg, form_name, form_email):
    print("inside async")
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587  # 465 for SSL
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False  # True
    app.config['MAIL_USERNAME'] = 'dibyadasiscool@gmail.com'
    app.config['MAIL_PASSWORD'] = 'samsunghp'
    print("all config done")
    mail = Mail(app)
    print("init mail app")
    form_data = form_msg  # request.form['msg']
    print("message taken")
    msg = Message('Query', sender='dibyadasiscool@gmail.com',
                  recipients=['dibyadas998@gmail.com'])
    print("message init")
    msg.body = "Query sent by:- " + form_name + "\n" + \
        form_data + "\n" + "Email-ID is:- " + form_email
    print("body made")
    print("going to send the msg")
    mail.send(msg)
    print("sent")
    return None


@app.route('/mail', methods=['POST'])
def mail():
    pool = Pool(processes=10)
    r = pool.apply_async(
        send_mail, [request.form['msg'],
                    request.form['name'],
                    request.form['email']])
    return ("sent", 200, {'Access-Control-Allow-Origin': '*'})

# if __name__ == "__main__":  # This is for local testin
#     app.run(host='localhost', port=3453, debug=True)


if __name__ == "__main__":  # This will come in use when
    port = int(os.environ.get("PORT", 5000))  # the app is deployed on heroku
    app.run(host='0.0.0.0', port=port)
