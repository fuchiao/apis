apis
========
## env
        virtualenv venv
        source venv/bin/activate
        pip install -r requirements.txt

## mysql service
        docker run --name mysqldb -v /tmp/mysql_data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=pass -it -p 3306:3306 -d mysql
        docker start mysqldb
        mysql -h 127.0.0.1 -u root -p < apis.sql

## start api server

### only local access
        gunicorn main:api

### public access
        gunicorn main:api -b 0.0.0.0:8000

## git archive
        git archive -o latest.zip HEAD

## test

### test tool
        sudo apt-get install httpie

### test command
        http POST zacknuc.csie.io:8000/user/ user=test1 pass=test123 mail=test@mail.com
        

## logs, search
  /logs/?path=aaa/bbb/ccc&tag=info,warn&from=20010102&to=20160505&key=abc&limit=100


## how to deploy
        http://docs.gunicorn.org/en/latest/deploy.html
