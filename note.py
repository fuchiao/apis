import json
import datetime


class NoteEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return super().default(self, obj)


class NoteCategory:
    def __init__(self, cnx, cursor):
        self.cnx = cnx
        self.cursor = cursor

    def on_get(self, req, resp):
        """Handles GET requests"""
        query = ('SELECT * FROM notes')
        cursor.execute(query)
        rows = cursor.fetchall()
        resp.body = json.dumps(rows, cls=NoteEncoder, ensure_ascii=False)

    def on_post(self, req, resp):
        """Handles POST requests"""
        payload_raw = req.stream.read()
        payload = json.loads(payload_raw)
        query = ('INSERT INTO notes (title, path, context) VALUES (%s, %s, %s)')
        data = (payload['title'], payload['path'], payload['context'])
        try:
            cursor.execute(query, data)
        except Exception as e:
            resp.body = str(e)
        else:
            cnx.commit()
            resp.body = str(cursor.lastrowid)


class NoteIndex:
    def __init__(self, cnx, cursor):
        self.cnx = cnx
        self.cursor = cursor

    def on_get(self, req, resp, index):
        """Handles GET requests"""
        payload_raw = req.stream.read()
        payload = json.loads(payload_raw)
        print(str(payload))
        query = ('SELECT title, path, context FROM notes WHERE id=%s')
        data = (index)
        cursor.execute(query, data)
        rows = cursor.fetchall()
        resp.body = json.dumps(rows, ensure_ascii=False)

    def on_patch(self, req, resp, index):
        """Handles PATCH requests"""
        payload_raw = req.stream.read()
        payload = json.loads(payload_raw)
        print(str(payload))
        query = ('UPDATE notes SET title=%s, path=%s, context=%s WHERE id=%s')
        data = (payload['title'], payload['path'], payload['context'], index)
        cursor.execute(query, data)
        cnx.commit()
        resp.body = "Good"
