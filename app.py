"""
Notes: for why we use the different parameter options
GET /v3/uk/train/station_timetables/{id}.json
`https://transportapi.com/v3/uk/train/station_timetables/${trainStation}.json?app_id=${appId}&app_key=${appKey}&train_status=passenger`
# example date
# datetime = 2022-02-03T20:30:00+01:00

# goes into the future
# to_offset=PT06:00:00
# am going to put this to 12 hours once working so we can see the next train if we are after 2am as there
# is a gap of more than 6 hours between trains over night in some instances.

# no need to add from_offset as we dont care about past arrivals
# from_offset = 0

# we want arrivals not departures and not stopping
# type = arrival

# we want passenger trains as we want to catch the train
# train_status = passenger

Notes for readme file.  
- currently the port is set at 8000:  please feel free to change that to suit your requirements.
- the index page is set to '/Welcome'
- the index displays information to the user about entering their 3letter code for their choosen station.  there are some examples, however due to 
 a. the time delay between Australia and the UK means there is a period of time where there may be no trains or buses expected for the next 12 hours.
 b. the API only allows 30 hits per day.
 c. each train station has different busy times for trains and buses.

- the return page automatically returns the route /show_nexttrain.html.  
On this page the the current time for the uk is always shown, then if there is data returned the following data is shown. station choosen, the next train arrival time, and what platform your train will arrive on. (If the next arrival is a bus the platform is shown as None)
The user has the option to press two buttons:
    1) show/hide more trains - which shows the trains due to arrive at the choosen station in the next 12 hours.
    2) show/hid buses - which shows the buses due to arrive at the choosen station in the next 12 hours. (this is a nice to have and additional to the original scope)

Return data is of json format.
 
Development and Testing
- for the purposes of testing I mainly used RMD and RED (Richmond and Redruth) stations as they seem to have a spread of bus and train arrivals 
- I ran out of API calls for the short time i had to design and test so there may be instances during future development that cases may arrise that have not been tested for.
- the user is given information to find codes as there many trainlines and a multiude of codes.  Some of which are duplicates. 
- i have commented out the print statements used in testing (but these are handy and can be uncommented out.(i do not know the python equivallent to kdebug for print statements))


Future updates:
- As this app is now functioning the next step would be for me to increase the to_offset to its max and check a large range of stations to ensure the majority of train 
    and bus arrivals are covered, especially for those stations that have less volume.   
-  I have not had time to investigate what happens for those train stations with duplicate codes.  
    I suppect for the future if i update this app i would have to add in either a check in return data that checks the station name for all data and allows the user to 
    choose which of the stations they want to look at or add a column so that each train and bus shows which station. 

"""
import os
import requests
import pytz
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

load_dotenv()
API_Key = os.getenv('API_Key')
print(API_Key)
API_ID = os.getenv('API_ID')
print(API_ID)

# Global variable to store train data
more_buses_data = []

def get_train_data(station_id):
    global more_trains_data, more_buses_data

    api_url = 'https://transportapi.com/v3/uk/train/station_timetables/{id}.json'

    url = api_url.format(id=station_id)
    base_url = 'https://transportapi.com/v3/uk/train/station_timetables/${trainStation}.json?app_id=${appId}&app_key=${appKey}&train_status=passenger'

    params = {'app_id' : API_ID,
          'app_key' : API_Key,
          'id' : station_id,
          'train_status' : 'passenger',
          'trainStation' : station_id,
          'type' : 'arrival',
#           'datetime': '2022-02-03T20:30:00+01:00',
          'to_offset' : 'PT12:00:00',
          'from_offset' : '-PT00:00:00'
        }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # train_data = data['arrivals']['all']
        print(data)
        return data 
    else:
        print("Failed to retrieve data:", response.text)
        # return {}
    
@app.route('/Welcome', methods=['GET', 'POST'])
def enter_Station_id_form():
    return render_template('nexttrain_form.html')

@app.route('/get_next_train', methods=['POST'])
def get_next_train():
    
# Get the user-entered station code
    station_id = request.form['station_id'].strip().upper()

# Check if the code is alphabetic and has a length of 3, Add "crs:" to the beginning of the station code
# for train in data['arrivals']['all']:
    if station_id.isalpha() and len(station_id) == 3:  
        station_id = f"crs:{station_id}"  
        data = get_train_data(station_id)
        print(data)

        # i did get the time conversion for the uk from chatgpt# 
        uk_timezone = pytz.timezone('Europe/London')
        current_datetime_uk = datetime.now(uk_timezone)
        current_time_uk = current_datetime_uk.time()

        print("Current time in the UK:", current_time_uk.strftime('%H:%M')) 
        current_time = current_datetime_uk
        current_time_format = current_time_uk.strftime('%H:%M')

        # print(data['station_name'])
        if data is None or 'arrivals' not in data:
            return render_template('show_nexttrain.html', no_data_message="No train data available at the moment.  Please check the official website for your station for future arrivals.")
            
#  so we can see that out train data is actually nested so:
        train_data = data['arrivals']['all']
        your_station = data['station_name']
        print(your_station)

# Clear previous data
        more_buses_data.clear() 

        if not more_buses_data:
            no_bus_message = f"No bus data available!  This page does not show system outages.  If no trains data please check the official timetable for the station you have selected."
        else:
            no_bus_message = None 

        if not train_data:
            no_train_message = f"No train data available! This page does not show system outages.  If no bus data please check the official timetable for the station you have selected."
        else:
            no_train_message = None 

        for train in train_data:
            mode = train['mode']
            arrival_time = train['aimed_arrival_time']
            print(f"Train mode: {mode}, Arrival time: {arrival_time}")
    
        arrival_time = datetime.strptime(train['aimed_arrival_time'], '%H:%M')
        your_station = None 
        train_platform = None   
        next_train = None

        for arrival in train_data:
            arrival_time = uk_timezone.localize(datetime.strptime(arrival['aimed_arrival_time'], "%H:%M")).strftime("%H:%M")
            print(f'arrival_time = {arrival_time}')
    
#     if train
        if arrival['mode'] == 'train':
            if next_train is None or (arrival_time > current_time and arrival_time < next_train):
                next_train = arrival_time
                train_platform = arrival['platform']
                your_station = data['station_name']

#     if bus
        elif arrival['mode'] == 'bus':
            if next_bus is None or (arrival_time > current_time and arrival_time < next_train):
                next_bus = arrival_time
                more_buses_data.append({
                    'mode': arrival['mode'],
                    'aimed_arrival_time': arrival['aimed_arrival_time'],
                    'origin_name': arrival['origin_name'],
                    'destination_name': arrival['destination_name']
                })
                print("bus added")

        return render_template('show_nexttrain.html', train_data=train_data, your_station=your_station, arrival_time=arrival_time, train_platform=train_platform, more_buses_data=more_buses_data, no_bus_message=no_bus_message, current_time_format = current_time_format)

    else:
        return "Invalid station code. Please enter a 3-letter alphabetic code."



if __name__ == '__main__':
    app.run(port=8000, debug=True)
