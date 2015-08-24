#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run

    python server.py

Go to http://localhost:8111 in your browser

eugene wu 2015
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# XXX: set this to your database
#
DATABASEURI = "sqlite:///test.db"


#
# after these statements, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               will list the tables in the database
#     .schema <tablename>   print CREATE TABLE statement for table
#
engine = create_engine(DATABASEURI)
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
)""")

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/', methods=["POST", "GET"])
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
  print request.args

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # context are the variables that are passed to the index.html template.
  # for example, "data" below will be accessible as a variable in index.html:
  #
  #     # will print str(data)
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict( data = [1, 2] )


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file is template/index.html
  #
  return render_template("index.html", **context)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
