import cx_Oracle
import sys

import getpass
class Database(object):
    def __init__(self, details):
        self.startConnection(details)
        self.cursor = self.connection.cursor()

    def startConnection(self, details):
        """
        Returns a the connection to the database.
        """
        try: 
            # Make the connection 
            connection = cx_Oracle.connect(details)
            self.connection = connection

        except cx_Oracle.DatabaseError as exc:
            error = exc.args
            print( sys.stderr, "Oracle code:", error.code)
            print( sys.stderr, "Oracle message:", error.message)


    def execute(self, query):
        """
        Executes the SQL query
        """
        curs = self.cursor
        curs.execute(query)

    def close(self):
        self.connection.close()


