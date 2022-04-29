from flask import Flask, render_template, request
import sys

app = Flask(__name__)

weather_data = {
    'BOSTON': {
        'degrees': 9,
        'state': 'Chilly',
        'city': 'BOSTON'
    },
    'NEW YORK': {
        'degrees': 32,
        'state': 'Sunny',
        'city': 'NEW YORK'
    },
    'EDMONTON': {
        'degrees': -15,
        'state': 'Cold',
        'city': 'EDMONTON'
    }
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/city', methods=['GET', 'POST'])
def add_city():
    if request.method == 'POST':
        req = request.form
        if req['city_name']:
            city_name_ = str(req['city_name']).upper()
            return render_template('index.html', city=weather_data[city_name_])


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
