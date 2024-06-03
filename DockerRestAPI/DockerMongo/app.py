import os
from flask import Flask, redirect, url_for, request, render_template
import flask
from pymongo import MongoClient
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import logging

app = Flask(__name__)


#connects to mongoDB, 
#first parameter is the host (local host)
#second parameter is mongoDB port
client = MongoClient('db', 27017)
db = client.tododb



###
# Globals
###
app = Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY


@app.route("/")
@app.route("/index")
def index():
    #delete prior data
    #db.tododb.delete_many({})
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404



###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")

    # getting user input
    date = request.args.get('startDate', "", type = str)
    time = request.args.get('startTime', "", type = str)
    distance = request.args.get('distance', 0, type = int)

    km = request.args.get('km', 999, type=float)

    app.logger.debug("start date ={}".format(date))
    app.logger.debug("start time={}".format(time))
    app.logger.debug("distance={}".format(distance))
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km

    # combine date and time into one datetime object
    starting_time = arrow.get(date + " " + time, 'YYYY-MM-DD HH:mm')

    #fix open time and close time
    #figure it out with right parameters
    open_time = acp_times.open_time(km, distance, starting_time)
    close_time = acp_times.close_time(km, distance, starting_time)

    # Reformatting open and close times to display correctly
    result = {"open": arrow.get(open_time).format('ddd M/D H:mm'), "close": arrow.get(close_time).format('ddd M/D H:mm')}
    return flask.jsonify(result=result)


@app.route('/handle_action', methods=['POST'])
def handle_action():
    action = request.form['submit']
    app.logger.debug("Action: {}".format(action))
    print("Data from frontend:", request.form)
    if action == 'submit':
        return handle_submit()
    elif action == 'display':
        return handle_display()
    else:
        return "You didn't press sumbmit or display", 400


def handle_submit():

    print("KM data received:", request.form.getlist('km'))
    print("Open time data received:", request.form.getlist('open'))
    print("Close time data received:", request.form.getlist('close'))

    kmDistances = request.form.getlist('km')
    openTimes = request.form.getlist('open')
    closeTimes = request.form.getlist('close')
    milesDistances = request.form.getlist('miles')
    brevet_distance = request.form.get('distance')
    begin_date = request.form.get('begin_date')
    begin_time = request.form.get('begin_time')


    km_list = []
    open_list = []
    close_list = []
    miles_list = []
    count = 0

    print(len(kmDistances),type(kmDistances),type(kmDistances[1]))
    for k in kmDistances:
        print(k)
    print(len(request.form.getlist('open')))

    for i in range(len(request.form.getlist('open'))):
        if kmDistances[i] == "" or openTimes[i] == "" or closeTimes[i] == "":
            continue

        km_list.append(kmDistances[i])
        open_list.append(openTimes[i])
        close_list.append(closeTimes[i])
        miles_list.append(milesDistances[i])
        count +=1 
    
    if count == 0:
        return render_template('warning.html')
    
    brevet_doc = {
                  'brevet_distance': brevet_distance, 
                  'begin_date': begin_date, 
                  'begin_time': begin_time
    }
    db.tododb.insert_one(brevet_doc)
    
    for i in range(count):
        item_doc = {
                    'miles': miles_list[i],
                    'km': km_list[i],
                    'open': open_list[i],
                    'close': close_list[i]
        }
        res = db.tododb.insert_one(item_doc)
        print("Inserted:", item_doc, 'res: ',res)
    
    return redirect(url_for('index'))



def handle_display():
    _items = db.tododb.find()
    items = [item for item in _items]

    if len(items) == 0:
        return render_template('warning.html')

    brevet_distance = db.tododb.find_one({'brevet_distance': {'$exists': True}}, {'brevet_distance': 1, '_id': 0})  # Find and extract brevet_distance
    begin_time = db.tododb.find_one({'begin_time': {'$exists': True}}, {'begin_time': 1, '_id': 0})
    begin_date = db.tododb.find_one({'begin_date': {'$exists': True}}, {'begin_date': 1, '_id': 0})

    print(begin_time)
    print(begin_date)
    print(brevet_distance)
    print(_items, items)

    if brevet_distance and begin_time and begin_date:
        return_data = render_template('display.html', items=items, brevet=brevet_distance['brevet_distance'], begin_date = begin_date['begin_date'], begin_time = begin_time['begin_time'])
    else:
        return_data = render_template('display.html', items=items, brevet=brevet_distance.get('brevet_distance'), begin_date = begin_date.get('begin_date'), begin_time = begin_time.get('begin_time'))

    #return_data = render_template('display.html', items=items, brevet=brevet_distance['brevet_distance'], begin_date = begin_date['begin_date'], begin_time = begin_time['begin_time'])
    #After I hit display, I clear my database
    db.tododb.delete_many({}) 
    return return_data



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
