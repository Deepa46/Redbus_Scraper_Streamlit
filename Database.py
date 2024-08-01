import mysql.connector
import re
import pandas as pd
'''
#connect database
mydb = mysql.connector.connect(
    host="localhost",
    user = "root",
    password = "Deepa@280624"
)
cursor = mydb.cursor()
#CREAT DATABASE
cursor.execute("CREATE DATABASE redbus_project")
'''
# Read the CSV file
df = pd.read_csv(r'C:\Users\yuvar\PycharmProjects\RedBus_Project\All_state_data.csv')


# function to extract integer
def extract_seat_count(seat_string):
    match = re.search(r'\d+', seat_string)
    return int(match.group()) if match else None


# apply function to seat_available column
df['Seat_Available'] = df['Seats Available'].apply(extract_seat_count)


# connect to particural database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Deepa@280624",
    database="redbus_project"
)
cursor = mydb.cursor()
cursor.execute('''
      CREATE TABLE bus_routes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Route_Name TEXT,
        Route_Link TEXT,
        Bus_Name TEXT,
        Bus_Type TEXT,
        Departing_Time Time,
        Duration TEXT,
        Reaching_Time Time,
        Star_Rating Float,
        Bus_Fare DECIMAL(10, 2),
        Seats_Available int
      );
''')

# column name in csv
data = df[['Route Name', 'Route Link', 'Bus Name', 'Bus Type', 'Departure Time', 'Duration', 'Arrival Time', 'Rating',
           'Fare', 'Seat_Available']].values.tolist()
# insert data into table
cursor.executemany(''' 
         INSERT INTO bus_routes (Route_Name, Route_Link, Bus_Name, Bus_Type, Departing_Time, Duration, Reaching_Time, 
         Star_Rating, Bus_Fare, Seats_Available)
         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
         ''', data)
mydb.commit()
cursor.close()
mydb.close()
print("Data stored in SQL database successfully.")
