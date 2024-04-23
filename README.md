# Group 10 Project Goat Scoring Database
The repository's purpose is to create a PostgreSQL supported goat database and run scripts to populate the database with data in the Data folder. Instructions on how to run the scripts is shown below.

### Disclaimers

1. It is assumed that you are using and familiar with the Linux command line.
2. It is assumed that you have PostgreSQL installed on your local machine, and are able to use PSQL commands on the command line.
3. It is assumed that you know how to clone this repository into your home folder on your local machine.

## Instructions

1. Install python pip, psycopg2, pandas, Flask packages by typing these commands into the command line:

   `sudo pacman -Syu`
   
   `sudo pacman -S python-pip python-psycopg2 python-pandas python-flask`

2. From your home directory, change directory to the project-group10 folder with the command:
   
   `cd project-group10`

3. The datainsertion.sql file should be populated already. If you need to populate it again for any reason, just run this command:

   `python dataextraction.py`

   This should run a script that cleans up the initial data of the desired attributes, pivots the table into the desired format, and writes SQL insertion commands into the datainsertion.sql file.

4. Create a database by running this command:

   `createdb <database-name>`

   So for example, `createdb project-group10`

5. Access the database by running the command:

   `psql project-group10`

   Now you should be in the psql terminal for the database.

6. Create the database schema and tables by inserting the tablecreation.sql file into Postgres. To do this, run the command:

   `\i tablecreation.sql`

   This should create the schema and tables needed for the data to be inserted.

7. Populate the tables by inserting the datainsertion.sql file into Postgres. To do this, run the command:

   `\i datainsertion.sql`

   Now all of the data should be stored in the database.

If everything was done correctly, you should now have a working goat database with populated data.

8. Configure and run the Flask application with these two commands:

   `FLASK_APP=app.py`
   `flask run`

   Then paste this URL into a web browser: `http://127.0.0.1:5000/`

The Flask application should now be running on localhost.
