from flask import Flask, render_template, request, jsonify, make_response, json
from flask_cors import CORS
from pusher import pusher
import pytz
import simplejson

app = Flask(__name__)
cors = CORS(app)
app.config['CORSHEADERS'] = 'Content-Type'

# configure pusher object
pusher = pusher.Pusher(
    app_id='764930',
    key='66f2adfe0cb37ef56ced',
    secret='890afe12b31fc6822793',
    cluster='ap3',
    ssl=True)


@app.template_filter('datetimefilter')
def datetimefilter(value, format='%b %d %I:%M %p'):
    # tz = pytz.timezone('Pakistan/Islamabad')  # timezone you want to convert to from UTC (America/Los_Angeles)
    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    # local_dt = value.astimezone(tz)
    return value.strftime(format)


@app.route('/')
def index():
    return render_template('indexs.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')


@app.route('/new/guest', methods=['POST'])
def guestUser():
    data = request.json
    pusher.trigger(u'general-channel', u'new-guest-details', {
        'name': data['name'],
        'email': data['email']
    })
    return json.dumps(data)


@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():
    auth = pusher.authenticate(channel=request.form['channel_name'], socket_id=request.form['socket_id'])
    return json.dumps(auth)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
