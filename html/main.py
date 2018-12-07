import tornado.ioloop
import tornado.web
# import tornado.database
import sqlite3
import os

def _execute(query):
        # dbPath = './trial.db'
        dbPath = "./1.sqlite"
        connection = sqlite3.connect(dbPath)
        cursorobj = connection.cursor()
        try:
                cursorobj.execute(query)
                result = cursorobj.fetchall()
                connection.commit()
        except Exception:
                raise
        connection.close()
        return result


class Main(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class AddStudent(tornado.web.RequestHandler):
    def get(self):
        self.render('sqliteform.html')

    def post(self):
        marks = int(self.get_argument("marks"))
        name = self.get_argument("name")
        query = ''' insert into stud (name, marks) values ('%s', %d) ''' %(name, marks);
        _execute(query)
        self.render('success.html')

class ShowRecords(tornado.web.RequestHandler):
    def get(self):
        query = ''' select * from t1 where id>100000'''
        rows = _execute(query)
        self._processresponse(rows)

    def _processresponse(self,rows):
        self.write("<b>Records</b> <br /><br />")
        for row in rows:
            print(row)
            self.write(str(row[0]) + "      " + str(row[1])+" <br />" )

# 
class ShowStudents(tornado.web.RequestHandler):
    def get(self):
        query = ''' select * from stud'''
        rows = _execute(query)
        self._processresponse(rows)

    def _processresponse(self,rows):
        self.write("<b>Records</b> <br /><br />")
        for row in rows:
            print(row)
            self.write(str(row[0]) + "      " + str(row[1])+" <br />" )


application = tornado.web.Application(
    handlers = [
        (r"/", Main),
        (r"/create" ,ShowRecords),
        (r"/show",ShowStudents),
        (r"/show_record",ShowRecords)],
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    # _path = os.path.join(os.path.dirname(__file__), "static"),
    debug=True,)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
