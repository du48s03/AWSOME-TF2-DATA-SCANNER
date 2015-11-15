#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.

eugene wu 2015
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, jsonify
import utils

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@w4111db1.cloudapp.net:5432/proj1part2
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db1.cloudapp.net:5432/proj1part2"
#
DATABASEURI = "postgresql://lch2135:395@w4111db1.cloudapp.net:5432/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above
#
engine = create_engine(DATABASEURI)


#
# START SQLITE SETUP CODE
#
# after these statements run, you should see a file test.db in your webserver/ directory
# this is a sqlite database that you can query like psql typing in the shell command line:
# 
#     sqlite3 test.db
#
# The following sqlite3 commands may be useful:
# 
#     .tables               -- will list the tables in the database
#     .schema <tablename>   -- print CREATE TABLE statement for table
# 
# The setup code should be deleted once you switch to using the Part 2 postgresql database
#
#engine.execute("""DROP TABLE IF EXISTS test;""")
#engine.execute("""CREATE TABLE IF NOT EXISTS test (
#  id serial,
#  name text
#);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")
#
# END SQLITE SETUP CODE
#



@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route("/team_query/", methods=["POST", "GET"])
def view_team_query():
  if(request.method=="GET"):# The user accesses the page
    return render_template('team_query.html')
  else:#The user queries for a team by either team name or team ID
    result = {'errmsg':'', 'playerlist':[], 'stats':{}}
    #Get the team ID
    print "team name = "+utils.sanitize(request.form['attr_val'])
    qrystr = """
SELECT id
FROM team
WHERE team.name='"""+utils.sanitize(request.form['attr_val'])+"""';"""
    print "Query string = "+ qrystr
    team = g.conn.execute(qrystr).fetchone()#Assumes there are no teams with the same name. 
    if(team is None):
      #The team doesn't exist
      return jsonify({'errmsg':'The team name does not exist in the database'})
    else:
      teamID = team[0]
    print "team ID = "+ str(teamID) 
    #---Get the player list---
    qrystr = """
SELECT P.id, P.name, PF.class, PF.kills, PF.assists, PF.deaths, PF.kad, PF.healspermin, PF.damagepermin, PF.ubers, PF.drops 
FROM player AS P, playson AS PT, 
	(SELECT playsformat.*
	 FROM playsformat, teamformat
	 WHERE teamformat.team="""+str(teamID)+""" AND playsformat.format=teamformat.format
	) AS PF
WHERE PT.team="""+str(teamID)+""" AND P.id=PT.player AND PF.player=PT.player;""" 
    player_it = g.conn.execute(qrystr)
    for player in player_it:
      print player
      result['playerlist'].append(dict(zip(['id','name','class','kills','assists',\
  					 'deaths','kad','healspermin','damagepermin','ubers','drops'],player)))
      
    #---Get the team stats --- 
    qrystr = """
    
  """ 
    return jsonify(result)    

@app.route("/player_stats/", methods=["POST", "GET"])
def view_player_stats():
  if(request.method == "POST"):
    attr = request.form['attr']
    if(attr == 'name'):
      qrystr = """
SELECT P.name, F.class, F.format, F.kills, F.assists, F.deaths, F.kad, F.healspermin, F.damagepermin, F.ubers, F.drops
FROM player as P, playsformat as F
WHERE	p.id = F.player
	AND p.name = '"""+utils.sanitize(request.form['attr_val'])+"""';"""
    elif(attr == 'id'):
      qrystr =  """SELECT P.name, F.class, F.format, F.kills, F.assists, F.deaths, F.kad, F.healspermin, F.damagepermin, F.ubers, F.drops
FROM player as P, playsformat as F
WHERE	p.id = F.player
	AND p.id = '"""+utils.sanitize(request.form['attr_val'])+"""';"""
    else:
      print "Error: unrecognized attribute "+attr
      return render_template('player_stats.html')

    rit = g.conn.execute(qrystr)
    # We assume that the result won't be too big
    result = {'data':[], 'errmsg':''}
    for r in rit:
      print r
      result['data'].append({'name':r[0],
                             'class':r[1],
                             'format':r[2],
                             'kills':r[3],
                             'assists':r[4],
                             'deaths':r[5],
                             'kad':r[6],
                             'healspermin':r[7],
                             'damagepermin':r[8],
                             'ubers':r[9],
                             'drops':r[10]})
    return jsonify(result)
  else: 
    return render_template('player_stats.html')

 
@app.route("/complex_query/league_compare", methods=["POST", "GET"])
def view_league_compare():
  #keys(request.args) = ['attr', 'attr_val', 'entity', 'results']
  context = dict([])
  context['data']= []
  if(request.method == "POST"):
    cls = utils.sanitize(request.form['cls'])
    print 'cls = ' + cls 
    qrystr = """SELECT TopPlayers.league, AVG(PlaysFormat.damagepermin) 
FROM PlaysFormat, 
	(SELECT PlaysOn.player AS player,TopTeams.league AS league
	FROM PlaysOn, (
                SELECT TD.team AS team, TD.league AS league
                FROM TeamDivision as TD, LeagueDivision as LD
                WHERE LD.rank=1 AND TD.league=LD.league AND TD.division = LD.division) AS TopTeams
	WHERE PlaysOn.team=TopTeams.team) AS TopPlayers
WHERE PlaysFormat.player=TopPlayers.player AND PlaysFormat.class = '"""+cls+"""' AND PlaysFormat.damagePerMin IS NOT NULL
GROUP BY TopPlayers.league;"""
    print qrystr
    result = g.conn.execute(qrystr)
    for record in result:
      print record
      context['data'].append({'league':str(record[0]), 'val':str(record[1])})
  return render_template('league_compare.html', **context)


#Compare performance of medics between formats (Performance = HealsPerMin, Ubers, Drops)
@app.route("/complex_query/format_compare/", methods=["POST", "GET"])
def view_format_compare():
  result = {'errmsg':'', 'formatlist':[]}
  if(request.method == "GET"):
    return render_template('format_compare.html', **result)
  else:
    cls = utils.sanitize(request.form['cls'])
    if(cls=='medic'):
      qrystr = """SELECT PF.format, AVG(PF.healsPerMin) as avg_HPM, AVG(CAST(PF.ubers AS decimal)/CAST(PF.drops AS decimal)) as avg_UD_rate
FROM PlaysFormat PF
WHERE class='"""+cls+"""' AND PF.drops <> 0
GROUP BY PF.format;"""
      formatlist_ptr = g.conn.execute(qrystr)
      for record in formatlist_ptr:
        print record
        result['formatlist'].append(dict(zip(['format', 'avg_hpm', 'avg_udrate'], [record[0], record[1], float(record[2])] )))
    else:
      qrystr = """SELECT PF.format, AVG(PF.kad) as avg_KAD, AVG(PF.damagepermin) as avg_DPM
FROM PlaysFormat AS PF
WHERE class='"""+cls+"""' AND PF.deaths <> 0 
GROUP BY PF.format;"""
      formatlist_ptr = g.conn.execute(qrystr)
      for record in formatlist_ptr:
        print record
        result['formatlist'].append(dict(zip(['format', 'avg_kad', 'avg_dpm'], record)))
    
    return render_template('format_compare.html', **result)
    


@app.route('/test/', methods=["POST", "GET"])
def return_test():
  """
  """
  print "Squeaky sent her regards" 

  print request.form 
  return "Hello Squeaky"



@app.route('/', methods=["POST", "GET"])
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """
 
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another/
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#
@app.route('/another/', methods=["POST", "GET"])
def another():
  return render_template("anotherfile.html")

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
