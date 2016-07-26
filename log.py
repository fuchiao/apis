import json
import datetime


class LogEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return super().default(self, obj)


class LogCategory:
    def __init__(self, cnx, cursor):
        self.cnx = cnx
        self.cursor = cursor

    def on_get(self, req, resp):
        """Handles GET requests"""
        query = 'SELECT * FROM logs'
        query_cond = ''
        params = {}
        data = []
        req.get_param_as_date('from', store=params)
        req.get_param_as_date('to', store=params)
        if 'from' in params and 'to' in params:
            query_cond += 'WHERE creat BETWEEN %s AND %s '
            data.append(params['from'])
            data.append(params['to'])
        elif 'from' in params:
            query_cond += 'WHERE creat >= %s '
            data.append(params['from'])
        elif 'to' in params:
            query_cond += 'WHERE creat <= %s '
            data.append(params['to'])
        else:
            pass
        req.get_param('path', store=params)
        if query_cond and 'path' in params:
            query_cond += 'AND path LIKE %s '
            data.append(params['path']+'%')
        elif 'path' in params:
            query_cond += 'WHERE path LIKE %s '
            data.append(params['path']+'%')
        else:
            pass
        params['tag'] = []
        req.get_param_as_list('tag', store=params)
        for i in params['tag']:
            if query_cond:
                query_cond += 'AND FIND_IN_SET(%s, tag) '
                data.append(i)
            else:
                query_cond += 'WHERE FIND_IN_SET(%s, tag) '
                data.append(i)
        params['key'] = []
        req.get_param_as_list('key', store=params)
        for i in params['key']:
            if query_cond:
                query_cond += 'AND context LIKE %s '
                data.append('%'+i+'%')
            else:
                query_cond += 'WHERE context LIKE %s '
                data.append('%'+i+'%')
        params['limit'] = 100
        req.get_param_as_int('limit', store=params)
        query_cond += 'ORDER BY id DESC LIMIT {}'.format(params['limit'])
        query = query+' '+query_cond
        print(query)
        print(data)
        self.cursor.execute(query, data)
        rows = self.cursor.fetchall()
        resp.body = json.dumps(rows, cls=LogEncoder, ensure_ascii=False)

    def on_post(self, req, resp):
        """Handles POST requests"""
        payload_raw = req.stream.read()
        payload = json.loads(payload_raw)
        query = ('INSERT INTO logs (path, context) VALUES (%s, %s)')
        data = (payload['path'], payload['context'])
        try:
            self.cursor.execute(query, data)
        except Exception as e:
            resp.body = str(e)
        else:
            self.cnx.commit()
            resp.body = str(self.cursor.lastrowid)


class LogIndex:
    def __init__(self, cnx, cursor):
        self.cnx = cnx
        self.cursor = cursor

    def on_get(self, req, resp, index):
        """Handles GET requests"""
        query = ('SELECT path, context FROM logs WHERE id=%s')
        data = (index,)
        self.cursor.execute(query, data)
        rows = self.cursor.fetchall()
        resp.body = json.dumps(rows, ensure_ascii=False)

