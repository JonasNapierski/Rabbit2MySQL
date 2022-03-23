# Rabbit2MYSQL

Rabbit2MYSQl is a small to automaticly insert your Rabbit-Queue data into a MySQL Database. This Script uses only a few Packages and will convert your JSON input in Rabbit into valid MySQL queries. 

## Features

- Convert key names from rabbit to new key names in MySQL
- Automaticly commits to your MySQL-Database new Messages from RabbitMQ
- flexibly design with a simple JSON-Config 


## How-To use it
Firstly `install` all nessesary packages using this command
```
python -m pip install mysql-connector-python pika
```
To `run` the script simply use:

```
python rabbit2mysql.py -c [path/to/config.json]
```


## JSON-Config example
Here is an example of the json config I used:
```json
{
    "mysql": {
        "host": "localhost",
        "port": 49161,
        "password": "rabbit",
        "user": "root"
    },
    "rabbit": {
        "host": "localhost" 
    },
    "query": {
        "queue": "test",
        "database": "test",
        "table": "temp",
        "rabbit2mysql": [
            {
                "rabbit": "name",
                "mysql": "sensorname"
            },
            {
                "rabbit": "temp",
                "mysql": "value"
            }
        ]
    }
}
```


## Todos
* [ ] create crash reports
* [ ] multable queries at once
* [ ] multithreadding for high frequencies of messages