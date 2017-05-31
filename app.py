from flask import Flask, redirect, url_for, request, render_template, Response
import os
import json
import requests

app = Flask(__name__)


@app.route('/<name>')
def main(name, position=None):
    url = "https://api.github.com/graphql"
    # headers = {"Authorization":os.environ[OUATH_KEY]}
    headers = {"Authorization": "Basic ZGlieWFkYXM6bmFuZGFEQVNAOTk="}
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
    headers = {"Access-Control-Allow-Origin": "*", 'Content-Type': 'text/html'}
    with open("templates/" + name + ".html", "w") as f:
        f.write(x)
    return "done"


@app.route('/generate')      # for generating the profiles of all at once
@app.route('/generate-<id>')    # for generating the profile of a single person
def generate(id=None):          # given their github id
    if id is not None:
        main(id)
    else:
        with open("data.json") as json_data_file:
            json_data = json.load(json_data_file)
            for i in json_data:
                for j in json_data[i]:
                    try:
                        main(j, i)
                    except Exception:
                        print("error")
                        print("id " + j)
    return "completed"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
