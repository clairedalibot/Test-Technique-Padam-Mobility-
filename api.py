import datetime
import sqlite3
from dateutil import parser


# function that gets data from one table in db.sqlite3
def get_data(table):
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute(f"SELECT * FROM {table}")
    donnees = c.fetchall()

    if table == 'busshift':
        busshift_list = []
        for i in donnees:
            di = dict(i)
            di['busstops'] = ", ".join(di['busstops'].split("///"))
            start_time = parser.parse(di['start'])
            di['start'] = start_time
            stop_time = parser.parse(di['stop'])
            di['stop'] = stop_time
            busshift_list.append(di)
        conn.close()
        return busshift_list

    else:
        data_list = []
        for i in donnees:
            di = dict(i)
            data_list.append(di)
        conn.close()
        return data_list


# creating the Busshift class
class Busshift:
    date_ref = datetime.date(1, 1, 1)

    def __init__(self, name, bus, driver, busstops, start, stop):
        self.name = name
        self.bus = bus
        self.driver = driver
        self.busstops = "///".join(busstops)
        self.start = datetime.datetime.combine(self.date_ref, start)
        self.stop = datetime.datetime.combine(self.date_ref, stop)

    def __str__(self):
        return f"BusShift {self.name} --> Bus : {self.bus}, Driver : {self.driver}, BusStops : {self.busstops}, Start : {self.start}, Stop : {self.stop}"

    # definition of the busshift's duration
    @property
    def duration(self):
        return self.stop - self.start

    # function that saves the busshift in a table "busshift" in db.sqlite3
    def save(self):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(f"""
        CREATE TABLE IF NOT EXISTS busshift (
            name text,
            bus text,
            driver text,
            busstops text,
            start text,
            stop text
        )
        """)

        if self.validation() == 1 :
            dic = vars(self)

            c.execute("INSERT INTO busshift VALUES (:name, :bus, :driver, :busstops, :start, :stop)", dic)

        conn.commit()
        conn.close()
        print("save")

    # function that deletes the busshift in the table "busshift" in db.sqlite3
    def delete(self):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        query = "DELETE FROM busshift WHERE name = ?"
        c.execute(query, (self.name,))
        conn.commit()
        conn.close()

    # check if the busshift's name is already used
    def busshift_name_validation(self):
        for busshift in get_data('busshift'):
            if self.name == busshift['name']:
                return False
        return True

    # check if the start time is before the stop time
    def busshift_time_validation(self):
        if self.start < self.stop :
            return True
        return False

    # check if the bus is already used on the time slot
    def busshift_bus_validation(self):
        ans = 1
        for busshift in get_data('busshift'):
            if self.bus == busshift['bus']:
                if not(self.stop < busshift['start'] or self.start > busshift['stop']):
                    ans = 0

        if ans == 0:
            return False
        return True

    # check if the driver is already occupied on the time slot
    def busshift_driver_validation(self):
        ans = 1
        for busshift in get_data('busshift'):
            if str(self.driver) == busshift['driver']:
                if not (self.stop < busshift['start'] or self.start > busshift['stop']):
                    ans = 0

        if ans == 0:
            return False
        return True

    # check that there is at least one bus stop
    def busshift_busstops_validation(self):
        return bool(self.busstops)

    # do all the checks
    def validation(self):
        return self.busshift_name_validation()*self.busshift_time_validation()*self.busshift_bus_validation()*self.busshift_driver_validation()*self.busshift_busstops_validation()


if __name__ == '__main__':
    data = get_data("busshift")
    #print(data)
    busshift1 = Busshift('200', 'HX--UC', 7, ['rue Blin', 'avenue de Hebert', 'rue de Bruneau'], datetime.time(9, 0, 0), datetime.time(18, 0, 0))
    print(busshift1.busshift_driver_validation())




