#! /usr/bin/python3

"""
This is an example Flask | Python | Psycopg2 | PostgreSQL
application that connects to the 7dbs database from Chapter 2 of
_Seven Databases in Seven Weeks Second Edition_
by Luc Perkins with Eric Redmond and Jim R. Wilson.
The CSC 315 Virtual Machine is assumed.

John DeGood
degoodj@tcnj.edu
The College of New Jersey
Spring 2020

----

One-Time Installation

You must perform this one-time installation in the CSC 315 VM:

# install python pip and psycopg2 packages
sudo pacman -Syu
sudo pacman -S python-pip python-psycopg2 python-flask

----

Usage

To run the Flask application, simply execute:

export FLASK_APP=app.py 
flask run
# then browse to http://127.0.0.1:5000/

----

References

Flask documentation:  
https://flask.palletsprojects.com/  

Psycopg documentation:
https://www.psycopg.org/

This example code is derived from:
https://www.postgresqltutorial.com/postgresql-python/
https://scoutapm.com/blog/python-flask-tutorial-getting-started-with-flask
https://www.geeksforgeeks.org/python-using-for-loop-in-flask/
"""

import psycopg2
from config import config
from flask import Flask, render_template, request

# Connect to the PostgreSQL database server
def connect(query):
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the %s database...' % (params['database']))
        conn = psycopg2.connect(**params)
        print('Connected.')
      
        # create a cursor
        cur = conn.cursor()
        
        # execute a query using fetchall()
        cur.execute(query)
        rows = cur.fetchall()

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    # return the query result from fetchall()
    return rows
 
# app.py
app = Flask(__name__)

command = '''
SELECT animal_id,tag,SUM(score),AVG(score),status_score 
FROM doe_status_scores NATURAL JOIN (
        SELECT animal_id,tag,session_id,
            {conditions}
            AS score
        FROM alive_sessions     
    )
    GROUP BY animal_id,tag, status_score
    ORDER BY AVG(score) DESC;
'''

conditions = {
    "birth_weight": "CASE WHEN birth_weight > 6 THEN 5 ELSE 3 END",
    "mothering": "CASE WHEN mothering = 'Good Mom' THEN 5 ELSE 1 END",
    "milk_rating": "CASE WHEN milk_rating = '1 Good Milk' THEN 5 ELSE 1 END",
    "num_of_kids": "CASE WHEN num_of_kids = '2 Twins' THEN 4 WHEN num_of_kids = '3 Triplets' THEN 3 ELSE 2 END",
    "observations": "CASE WHEN observations = '1 No Problems' THEN 5 ELSE 1 END",
    "kid_ease": "CASE WHEN kid_ease = '1 No Assist' THEN 5 ELSE 1 END",
    "mother_score": "CASE WHEN mother_score = '1 Doe stays close' THEN 5 ELSE 1 END"
}

# serve form web page
@app.route('/')
def form():
    
    # create the command that will get the rankings
    conds = conditions.values()
    cmd = command.format(conditions='+'.join(conds))
    rows = connect(cmd)

    return render_template('my-form.html', rows=rows, filters=conditions.keys())

# handle query POST and serve result web page

#@app.route('/', methods=['POST'])
#def query_handler():
#    print(f'{request.form.get("birth_weight","mothering","milk_rating","num_of_kids","observations","kid_ease","mother_score")}')
#    rows = connect(request.form.get("birth_weight","mothering","milk_rating","num_of_kids","observations","kid_ease","mother_score"))
#    return render_template('my-result.html', rows=rows)

@app.route('/', methods=['POST'])
def checkbox_handler():
    filter = []
    if request.method == 'POST':
        has_filter = False
        
        for key in request.form.to_dict().keys():
            filter.append(conditions[key])
            has_filter = True

        if not has_filter:
            return render_template('my-form.html')

        fquery = '''
        SELECT animal_id,tag,SUM(score),AVG(score),status_score 
        FROM doe_status_scores NATURAL JOIN (
            SELECT animal_id,tag,session_id,
                {conditions}
                AS score
            FROM alive_sessions)
        GROUP BY animal_id,tag, status_score
        ORDER BY AVG(score) DESC;
        '''
        fquery = fquery.format(conditions='+'.join(filter))

        rows = connect(fquery)

        return render_template('my-form.html', rows=rows, filters=request.form.to_dict().keys())

if __name__ == '__main__':
    app.run(debug = True, static_url_path='/static')
