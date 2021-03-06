"""
CS121 Final
(Client version)

Authors: Derek Ing, Daniel Li
Emails: ding@caltech.edu, dzli@caltech.edu

Our database is a FIFA World Cup dataset containing information about all past World Cups. 
Some of the information contained consists of the winning team, hosting country, goals scored, etc..  
Our application program is ranking the performances of players and countries in the World Cup 
by goals scored and number of titles, respectively.
"""
import sys
import mysql.connector
import mysql.connector.errorcode as errorcode

DEBUG = False

# ----------------------------------------------------------------------
# SQL Utility Functions
# ----------------------------------------------------------------------
def get_conn():
    """"
    Returns a connected MySQL connector instance, if connection is successful.
    If unsuccessful, exits.
    """
    try:
        conn = mysql.connector.connect(
          host='localhost',
          user='fan',
          port='3306',
          password='fanpw',
          database='fifa'
        )
        print('Successfully connected.')
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR and DEBUG:
            sys.stderr('Incorrect username or password when connecting to DB.')
        elif err.errno == errorcode.ER_BAD_DB_ERROR and DEBUG:
            sys.stderr('Database does not exist.')
        elif DEBUG:
            sys.stderr(err)
        else:
            sys.stderr('An error occurred, please contact the administrator.')
        sys.exit(1)

# ----------------------------------------------------------------------
# Functions for Command-Line Options/Query Execution
# ----------------------------------------------------------------------
def player_goals_query():
    """
    Shows a list of players with their total number of World Cup goals.
    Results are sorted by total goals in descending order.
    """
    cursor = conn.cursor()
    sql = """
SELECT player_name, COUNT(*) AS total_goals 
FROM match_goals NATURAL JOIN player 
GROUP BY player_name ORDER BY total_goals DESC;
"""
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            (player_name, total_goals) = row
            print('  ', f'"{player_name}"', ':', f'({total_goals})', 'goals')
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred, give something useful for clients...')

def year_wins_query():
    """
    Shows a list of World Cup years with World Cup winner that year.
    Results are sorted by year in ascending order.
    """
    cursor = conn.cursor()
    sql = "SELECT year, winner FROM tournaments ORDER BY year ASC;"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            (year, winner) = row
            print('  ', f'"{year}"', 'Winner:', f'({winner})')
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred.')

def team_wins_query():
    """
    Shows a list of countries with their total number of World Cup titles.
    Results are sorted by total titles in descending order.
    """
    cursor = conn.cursor()
    sql = """
SELECT winner AS country, COUNT(*) AS titles
FROM tournaments 
GROUP BY winner ORDER BY titles DESC;
"""
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            (country, titles) = row
            print('  ', f'"{country}"',':', f'({titles})', 'Titles')
    except mysql.connector.Error as err:
        if DEBUG:
            sys.stderr(err)
            sys.exit(1)
        else:
            sys.stderr('An error occurred.')

# ----------------------------------------------------------------------
# Command-Line Functionality
# ----------------------------------------------------------------------
def show_options():
    """
    Displays options users can choose in the application, such as (g), (y),
    and (w) to view and (q) to quit.
    """
    print('What would you like to do? ')
    # print('  (l) login')
    print('  (g) view all time top World Cup goal scorers')
    print('  (y) view World Cup winners by year')
    print('  (w) view teams with most World Cup titles')
    print('  (q) - quit')
    print()
    while True:
        ans = input('Enter an option: ')[0].lower()
        if ans == 'q':
            quit_ui()
        # elif ans == 'l':
            # log_in()
        elif ans == 'g':
            player_goals_query()
        elif ans == 'y':
            year_wins_query()
        elif ans == 'w':
            team_wins_query()
        else:
            print('Unkown option.')

def quit_ui():
    """
    Quits the program, printing a good bye message to the user.
    """
    print('Good bye!')
    print('SIIIIIUUU')
    exit()


def main():
    """
    Main function for starting things up.
    """
    show_options()


if __name__ == '__main__':
    conn = get_conn()
    main()
