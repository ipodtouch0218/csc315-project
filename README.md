# Group 10 Project Goat Scoring Database
The repository's purpose is to create a PostgreSQL supported goat database and run scripts to populate the database with data in the Data folder. Instructions on how to run the scripts is shown below.

### Disclaimers

1. It is assumed that you are using and familiar with the Linus command line.
2. It is assumed that you have PostgreSQL installed on your machine, and are able to use PSQL commands on the command line.

## Instructions

1. Install python pip, psycopg2, pandas packages by typing these commands into the command line:

   `sudo pacman -Syu`
   
   `sudo pacman -S python-pip python-psycopg2 python-pandas`

2. The datainsertion.sql file should be populated already. If you need to populate it again for any reason, just run this command:

   `python dataextraction.py`

This should run a script that cleans up the initial data of the desired attributes, pivots the table into the desired format, and writes SQL insertion commands into the datainsertion.sql file.

3. Create a database by running this command: `createdb <database-name>`

   So for example, `createdb project-group10`

4. Create the database schema and tables by inserting the tablecreation.sql file into Postgres. To do this, run the command:

   `\i tablecreation.sql`

This should create the schema and tables needed for the data to be inserted.

5. Populate the tables by inserting the datainsertion.sql file into Postgres. To do this, run the command:

   `\i datainsertion.sql`

Now all of the data should be stored in the database.

If everything was done correctly, you should now have a working goat database with populated data.
   
