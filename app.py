from flask import Flask, redirect, url_for, request, render_template, Response
import os
import json
import requests
from collections import OrderedDict

app = Flask(__name__)


@app.route('/<name>')
def profile(name, position=None):
    url = "https://api.github.com/graphql"
    headers = {"Authorization": os.environ[OUATH_KEY]}
    query = json.dumps({"query": "query{user(login: \"" + name +
                        "\") { name email avatarUrl url bio websiteUrl"
                        " pinnedRepositories(first: 6) "
                        "{ nodes { name url description } } } }"})
    r = requests.post(url, headers=headers, data=query)
    data_dict = json.loads(r.content.decode("utf-8"), sorted)
    pinned_repos = data_dict['data']['user']['pinnedRepositories']['nodes']
    image = data_dict['data']['user']['avatarUrl']
    gh_link = data_dict['data']['user']['url']
    bio = data_dict['data']['user']['bio']
    full_name = data_dict['data']['user']['name']
    email = data_dict['data']['user']['email']
    blog = data_dict['data']['user']['websiteUrl']

    x = render_template('template.tmpl', name=name,
                        pinned_repos=pinned_repos,
                        image=image,
                        gh_link=gh_link,
                        bio=bio,
                        full_name=full_name,
                        email=email,
                        blog=blog,
                        position=position
                        )
    with open("pages/" + name + ".html", "w") as f:
        f.write(x)
    return "done"


def card(name, position=None):
    print("in card")
    url = "https://api.github.com/graphql"
    headers = {"Authorization": os.environ[OUATH_KEY]}
    query = json.dumps({"query": "query{user(login: \"" + name +
                        "\") { name avatarUrl"
                        " } }"})
    r = requests.post(url, headers=headers, data=query)
    data_dict = json.loads(r.content.decode("utf-8"), sorted)
    image = data_dict['data']['user']['avatarUrl']
    full_name = data_dict['data']['user']['name']
    x = render_template('cards.tmpl', image=image,
                        full_name=full_name,
                        position=position,
                        name=name
                        )
    with open("cards/all.html", "a") as f:
        f.write(x)
    return "done"


@app.route('/generate')      # for generating the profiles of all at once
@app.route('/generate-<id>')    # for generating the profile of a single person
def generate(id=None):          # given their github id
    if id is not None:
        profile(id, position="Member")
    else:
        with open("data.json") as json_data_file:
            json_data = json.load(json_data_file)
            for i in json_data:
                for j in json_data[i]:
                    try:
                        profile(j, i)
                    except Exception:
                        print("Error generating profile for :- ")
                        print("ID - " + j)
    return "Completed"


@app.route('/card')
@app.route('/card-<id>')
def generate_card(id=None):
    if id is not None:
        card(id, position="Member")
    else:
        try:
            os.remove("cards/all.html")
        except Exception:
            pass
        os.system("touch cards/all.html")
        with open("data.json") as json_data_file:
            json_data = json.load(json_data_file,
                                  object_pairs_hook=OrderedDict
                                  )
            for i in json_data:
                for j in json_data[i]:
                    try:
                        card(j, i)
                    except Exception:
                        print("Error generating profile for :- ")
                        print("ID - " + j)
    return "Completed"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
