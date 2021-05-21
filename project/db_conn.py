import psycopg2
#from psycopg2.extras import Json


def saveMyData(json):
    connect = psycopg2.connect(dbname='mov_db', user='rhino', host='192.168.3.44', port='5432', password='stevieB')
    cur = connect.cursor()
    cur.execute("select measure.savemeasure(%s)",(json,))
    #config = cur.fetchall()
    connect.commit()
    connect.close()
    print("data saved")