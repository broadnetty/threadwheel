import sqlite3


class Settings:

    dbpath = 'resources/settings.db'

    def __init__(self):
        if not self.exec_query("SELECT name FROM sqlite_schema WHERE type='table'"):
            self.exec_query('''CREATE TABLE settings
                   (name text, type text, value text)''')


    def exec_query(self, command):
        con = sqlite3.connect(self.dbpath)
        cur = con.cursor()
        cur.execute(command)

        result = cur.fetchall()
        con.commit()
        con.close()
        return result

    def Get(self):
        result = self.exec_query("SELECT * FROM settings WHERE name='filters'")
        if result:
            return result
        else:
            return [('filters', 'owner', 'All'), ('filters', 'status', 'All')]

    def Save(self, data=None):
        if data is None:
            data = {'filters': {'owner': 'All', 'status': 'All'}}
        if not self.exec_query("SELECT * FROM settings WHERE name='filters'"):
            self.exec_query("INSERT INTO settings values('filters','owner','" + str(data['filters']['owner']) + "')")
            self.exec_query("INSERT INTO settings values('filters','status','" + str(data['filters']['status']) + "')")
        else:
            self.exec_query("UPDATE settings SET value='" + str(data['filters']['owner']) + "' WHERE name='filters' and type='owner'")
            self.exec_query("UPDATE settings SET value='" + str(data['filters']['status']) + "' WHERE name='filters' and type='status'")
        pass
