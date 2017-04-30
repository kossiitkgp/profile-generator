from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)


@app.route('/<name>')
def main(name):
    return render_template('test.html', name=name)


if __name__ == "__main__":  # This is for local testin
    app.run(host='localhost', port=3453, debug=True)

# if __name__ == "__main__":  # This will come in use when
#     port = int(os.environ.get("PORT", 5000))  # the app is deployed on heroku
#     app.run(host='0.0.0.0', port=port)
