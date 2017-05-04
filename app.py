from flask import Flask, redirect, url_for, request, render_template
from flask_mail import Mail, Message
app = Flask(__name__)


@app.route('/<name>')
def main(name):
    return render_template('test.html', name=name)


@app.route('/mail', methods=['POST'])
def mail():
	app.config['MAIL_SERVER']='smtp.gmail.com'
	app.config['MAIL_PORT'] = 465
	app.config['MAIL_USE_TLS'] = False
	app.config['MAIL_USE_SSL']= True
	app.config['MAIL_USERNAME'] = 'dibyadascool@gmail.com'
	app.config['MAIL_PASSWORD'] = 'test'
	mail = Mail(app)
	form_data = request.form['msg']
	msg = Message('Query',sender = 'dibyadascool@gmail.com', recipients = ['dibyadas998@gmail.com'])
	msg.body = form_data
	mail.send(msg)
	return "Sent"

if __name__ == "__main__":  # This is for local testin
    app.run(host='localhost', port=3453, debug=True)

# if __name__ == "__main__":  # This will come in use when
#     port = int(os.environ.get("PORT", 5000))  # the app is deployed on heroku
#     app.run(host='0.0.0.0', port=port)
