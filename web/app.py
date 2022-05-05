import os

from flask import Flask, render_template, request, redirect, url_for, flash
import sys
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config.update(SECRET_KEY=os.urandom(24))
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
        weather_data[city.name].update({"id": city.id})
        rendered_cities.update({city.name: weather_data[city.name]})
        print(rendered_cities)
    return render_template('index.html', cities=rendered_cities)


@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = session.query(City).filter_by(id=city_id).first()
    if not city:
        flash("The city doesn't exist!")
    else:
        session.delete(city)
        session.commit()
    return redirect('/')


@app.route('/city', methods=['GET', 'POST'])
def add_city():
    if request.method == 'POST':
        req = request.form

        if req['city_name']:
            city_name_ = str(req['city_name']).upper()
            if city_name_ in weather_data:
                if not session.query(City).filter_by(name=city_name_).first():
                    session.add(City(name=city_name_))
                    session.commit()
                else:
                    flash("The city has already been added to the list!")
            else:
                flash("The city doesn't exist!")

    return redirect(url_for('index'))


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
