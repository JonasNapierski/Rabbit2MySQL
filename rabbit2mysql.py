from distutils.log import  warn, error
import mysql.connector, json, sys, pika, os

# global variables
configFilePath = ""
config = None

# commandline argument parser
try:
    if not sys.argv.__contains__("-c"):
        sys.exit(1)     
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-c":
            configFilePath = sys.argv[i+1] #get configfilePath from commandline arguments

    file = open(configFilePath, "r")
    config = json.loads(file.read())
except:
    warn("You must use the Command Argument -c [path/to/config.json]")
    sys.exit(0)


def initMySQL():
    """
        init MySql via Config settings
    """
    mydb = mysql.connector.connect(
        port=config["mysql"]["port"],
        host=config["mysql"]["host"],
        user=config["mysql"]["user"],
        password=config["mysql"]["password"],
        database=config['query']['database']
    )
    return mydb


def rabbit2mysql_key(rabbit_key: str):
    """ 
        rabbit2mysql_key converts the key from the input 'rabbit_key' [str] into the in the config
        defined convertion of the mysql database

        return [str]
    """
    for obj in config["query"]["rabbit2mysql"]:
        if  obj["rabbit"] == rabbit_key:
            return obj["mysql"]
    return None

def main():

    # init and set cursor to the right database
    mydb = initMySQL()
    mycursor = mydb.cursor()
    
    # init rabbit connection wit pika 
    conn = pika.BlockingConnection(pika.ConnectionParameters(config["rabbit"]["host"]))
    chan = conn.channel()
    #chan.queue_declare(queue="hello") # create if not existing channel
    

    # callback function for rabbitmq messages
    def callback(ch, method, properties, body: bytes):
        try:
            body = body.decode() # decode body into json 
            queue_element = json.loads(body) 
            
            values = ""
            temp = ""
            for e in queue_element:
                key = rabbit2mysql_key(e)
                if key:
                    temp = temp +f",{key}"
                    if type(queue_element[e]) == str:
                        values = values + f",'{queue_element[e]}'"
                    else:
                        values = values + f",{queue_element[e]}"

            mysql_query = f"INSERT INTO {config['query']['table']} ({temp[1:]}) values ({values[1:]})"          
            mycursor.execute(mysql_query)
            print(" [x] executed: "+ mysql_query)
            mydb.commit()
        except:
            error("Your queue in Rabbit is not in valid JSON format.")


    chan.basic_consume(queue=config["query"]["queue"], auto_ack=True, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CRT+C")
    chan.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)


