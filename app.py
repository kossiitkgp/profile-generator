from flask import Flask, redirect, url_for, request, render_template
from urllib.request import urlopen
import json


data = {"arindambiswas":{"name":"Arindam Biswas", "gh_handle":"aribis369" ,"fb_link":"https://facebook.com/aribis369", "bio":"to be written by the member", "pic_src":"link"}, "dibyaprakashdas":{"name":"Dibya Prakash Das", "gh_handle":"dibyadas", "fb_link":"https://facebook.com/user_name", "bio":"whatever you like", "pic_src":"link"}}


app = Flask(__name__)


@app.route('/<name>')
def main():
    mname = data[name]["gh_handle"]
    repos = []
    repolink = []
    blog = str()
    content={}
    gh_link = "https://github.com/"+mname

    httpob = urlopen("https://api.github.com/users/"+mname+"/repos")
    decob = httpob.read().decode("utf-8")
    jsonob = json.loads(decob)
    for j in jsonob:
        if str(j["fork"])=="False":
            repos.append(j["name"])
            repolink.append("https://www.github.com/"+j["full_name"])
    
    httpob = urlopen("https://api.github.com/users/"+mname)
    decob = httpob.read().decode("utf-8")
    jsonob = json.loads(decob)
    blog = jsonob["blog"]

    content = {"name":data[name]["name"], "gh_handle":data[name]["gh_handle"], "fblink":data[name]["fb_link"], "bio":data[name]["bio"], "picsrc":data[name]["pic_src"], "mrepos":repos, "mrepolink":repolink, "mblog":blog}

   # return render_template('test.html', mem_name=data[name]["name"], gh_handle=data[name]["gh_handle"], fblink=data[name]["fb_link"], bio=data[name]["bio"], picsrc=data[name]["pic_src"], mrepos=repos, mrepolink=repolink, mblog=blog)
    return render_template('test.html', content=content) 


if __name__ == "__main__":  # This is for local testing
    app.run(host='localhost', port=3453, debug=True)

# if __name__ == "__main__":  # This will come in use when
#     port = int(os.environ.get("PORT", 5000))  # the app is deployed on heroku
#     app.run(host='0.0.0.0', port=port)
