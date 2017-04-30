from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)   

@app.route('/<name>')
def main(name):
	return render_template('test.html',name = name)


if __name__ == "__main__":							# This if block is to run the app on our local machine
    app.run(host='localhost', port=3453,debug=True)


# if __name__ == "__main__":  						#This piece of code will come in use when
#     port = int(os.environ.get("PORT", 5000))    	#when the app is deployed on heroku and will replace the above if block
#     app.run(host='0.0.0.0', port=port)