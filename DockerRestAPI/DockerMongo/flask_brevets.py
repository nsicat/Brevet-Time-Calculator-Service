"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
#app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
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


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
