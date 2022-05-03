from flask import Flask, render_template, request, redirect, url_for
import sys
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
engine = create_engine("sqlite:///weather.db?check_same_thread=False")

Base = declarative_base()
weather_data = {
    'LONDON': {
        'degrees': 9,
        'state': 'Chilly',
        'city': 'LONDON'
    },
    'FAIRBANKS': {
        'degrees': 32,
        'state': 'Sunny',
        'city': 'FAIRBANKS'
    },
    'IDAHO': {
        'degrees': -15,
        'state': 'Cold',
        'city': 'IDAHO'
    }
}


class City(Base):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/')
def index():
    rendered_cities = dict()
    db_cities = session.query(City).all()
    for city in db_cities:
        rendered_cities.update({city.name: weather_data[city.name]})
    return render_template('index.html', cities=rendered_cities)


@app.route('/city', methods=['GET', 'POST'])
def add_city():
    if request.method == 'POST':
        req = request.form

        if req['city_name']:
            city_name_ = str(req['city_name']).upper()
            session.add(City(name=city_name_))
            session.commit()
    return redirect(url_for('index'))


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
