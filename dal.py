import sqlite3
import logging


class UsersDatabase:
    
    def __init__(self):
        try:
            self.connection = sqlite3.connect("users.db")
        except:
            logging.error('Could not connect to database')
        
        self.connection.cursor().execute('CREATE TABLE IF NOT EXISTS "users" '
                                         '(`id`	INTEGER NOT NULL UNIQUE, '
                                         '`pt`	TEXT NOT NULL, PRIMARY KEY(`id`))')
        
        self.add_query = 'INSERT INTO users VALUES(?, 0)'
        self.get_query = 'SELECT * FROM users WHERE id=?'
        self.del_query = 'DELETE FROM users WHERE id=?'
        self.upd_query = 'UPDATE users SET pt=? WHERE id=?'
        
    def add_user(self, id):
        cursor = self.connection.cursor()
        cursor.execute(self.add_query, (id,))
        self.connection.commit()
        
    def del_user(self, id):
        cursor = self.connection.cursor()
        cursor.execute(self.del_query, (id,))
        self.connection.commit()
        
    def get_user(self, id):
        cursor = self.connection.cursor()
        cursor.execute(self.get_query, (id,))
        return cursor.fetchone()
    
    def upd_user(self, id, pt):
        cursor = self.connection.cursor()
        cursor.execute(self.upd_query, (pt, id))
        self.connection.commit()
        
    