import streamlit as st
import pandas as pd
import mysql.connector


# Function to get data from Mysql
def get_data_from_db(query, params=None):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Deepa@280624',
        database='redbus_project'
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# st.title("Bus Booking System")


# Query
route_query = "SELECT DISTINCT Route_Name FROM bus_routes"
seat_type_query = "SELECT DISTINCT Bus_Type FROM bus_routes"
departure_time_query = "SELECT DISTINCT Departing_Time FROM bus_routes"
rating_query = "SELECT DISTINCT Star_Rating FROM bus_routes"

route_data = pd.DataFrame(get_data_from_db(route_query))
seat_type_data = pd.DataFrame(get_data_from_db(seat_type_query))
departure_time_data = pd.DataFrame(get_data_from_db(departure_time_query))
rating_data = pd.DataFrame(get_data_from_db(rating_query))

# Add "Others" option to the dropdown
route_data = pd.concat([pd.DataFrame(['Others'], columns=['Route_Name']), route_data])
seat_type_data = pd.concat([pd.DataFrame(['Others'], columns=['Bus_Type']), seat_type_data])
rating_data = pd.concat([pd.DataFrame(['Others'], columns=['Star_Rating']), rating_data])

# Sidebar menu
st.sidebar.title("Menu")
menu_option = st.sidebar.selectbox("Select an option", ["Home", "Filter"])

if menu_option == "Filter":
    st.sidebar.title("Filters")

    route = st.sidebar.selectbox("Select the Route", route_data['Route_Name'])
    seat_type = st.sidebar.selectbox("Select the Seat Type", ["Seater", "Sleeper", "Others"])
    ac_type = st.sidebar.selectbox("Select the AC Type", ["A/C", "Non-A/C", "Others"])
    departure_time = st.sidebar.selectbox("Select the Departing Time", [
        "00:00 - 06:00",
        "06:00 - 12:00",
        "12:00 - 18:00",
        "18:00 - 00:00",
        "Others"
    ])
    rating = st.sidebar.selectbox("Select the Ratings", ["2 to 3", "3 to 4", "4 to 5", "Others"])

    # Map departure time filter to actual times
    departure_time_map = {
        "00:00 - 06:00": ("00:00", "06:00"),
        "06:00 - 12:00": ("06:00", "12:00"),
        "12:00 - 18:00": ("12:00", "18:00"),
        "18:00 - 00:00": ("18:00", "23:59")
    }

    # filter conditions
    route_condition = "" if route == "Others" else "Route_Name = %s"
    seat_type_condition = "" if seat_type == "Others" else "bus_Type LIKE %s"
    ac_condition = "" if ac_type == "Others" else "Bus_Type LIKE %s"
    departure_time_condition = "" if departure_time == "Others" else "Departing_Time BETWEEN %s AND %s"
    rating_condition = "" if rating == "Others" else "Star_Rating BETWEEN %s AND %s"

    # build WHERE clause dynamically
    conditions = " AND ".join(filter(None, [
        route_condition,
        seat_type_condition,
        ac_condition,
        departure_time_condition,
        rating_condition
    ]))

    #  final query
    filter_query = f"""
    SELECT Route_Name, Bus_Name, Bus_Type, Star_Rating, Bus_Fare, 
    CONCAT(Seat_Available,' Seat Available') AS Seat_Available
    FROM bus_routes
    """

    if conditions:
        filter_query += " WHERE " + conditions

    #  parameters based on the filters
    params = []
    if route != "Others":
        params.append(route)
    if seat_type != "Others":
        params.append(f"%{seat_type}%")
    if ac_type != "Others":
        params.append("A/C%" if ac_type == "A/C" else "%Non A/C%")
    if departure_time != "Others":
        params.extend(departure_time_map[departure_time])
    if rating != "Others":
        rating_start, rating_end = {
            "2 to 3": (2, 3),
            "3 to 4": (3, 4),
            "4 to 5": (4, 5)
        }[rating]
        params.extend([rating_start, rating_end])

    # Get filtered data
    filtered_data = pd.DataFrame(get_data_from_db(filter_query, params))

    # Display DataFrame
    st.header("Filtered Bus Data")
    st.dataframe(filtered_data)

else:
    st.header("Welcome to the Home Page")
    st.write("Please select 'Filter' from the sidebar to filter bus data.")
