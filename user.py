import json
import datetime
import uuid
import hashlib
import arrow

class User:
    def __init__(self, cnx, cursor):
        self.cnx = cnx
        self.cursor = cursor

    def on_get(self, req, resp):
        """Handles GET requests"""
        payload_raw = req.stream.read()
        payload = json.loads(payload_raw)
        query = ('SELECT token, CURRENT_TIMESTAMP>expire FROM account WHERE user=%s AND pass=unhex(%s)')
        data = (payload['user'], hashlib.md5(payload['pass']+'holy_shit_there_is_a_lot_of_salt').hexdigest())
        self.cursor.execute(query, data)
        for row in self.cursor:
            if row[1]:  # expire
                query = ('UPDATE account SET token=unhex(%s) WHERE user=%s AND pass=unhex(%s)')
                new_uuid_hex = uuid.uuid4().hex
                data = (new_uuid_hex, payload['user'], payload['pass'])
                self.cursor.execute(query, data)
                self.cnx.commit()
                resp.body = new_uuid_hex
            else:   # not expire
                resp.body = row[0]
            return

    def on_post(self, req, resp):
        """Handles POST requests"""
        payload_raw = req.stream.read()
        payload = json.loads(payload_raw)
        query = ('INSERT INTO account (user, pass, mail, token) VALUES (%s, unhex(%s), %s, unhex(%s)')
        uuid_hex = uuid.uuid4().hex
        data = (payload['user'], hashlib.md5(payload['pass']+'holy_shit_there_is_a_lot_of_salt_!').hexdigest(), payload['mail'], uuid_hex)
        try:
            self.cursor.execute(query, data)
        except Exception as e:
            resp.body = str(e)
        else:
            self.cnx.commit()
            resp.body = uuid_hex


