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


def get_train_data(station_id):

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
          'to_offset' : 'PT06:00:00',
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
    station_id = request.form['station_id'].strip().upper()  # Get the user-entered station code
    if station_id.isalpha() and len(station_id) == 3:  # Check if the code is alphabetic and has a length of 3
        station_id = f"crs:{station_id}"  # Add "crs:" to the beginning of the station code
        data = get_train_data(station_id)# for train in newdata['arrivals']['all']:
        print(data)
        # print(data['station_name'])
            
#  so we can see that out train data is actually nested so:
        train_data = data['arrivals']['all']
        your_station = data['station_name']
        print(your_station)

# i did get the time conversion for the uk from chatgpt# 
        uk_timezone = pytz.timezone('Europe/London')
        current_datetime_uk = datetime.now(uk_timezone)
        current_time_uk = current_datetime_uk.time()

        print("Current time in the UK:", current_time_uk.strftime('%H:%M')) 
        current_time = current_datetime_uk

        for train in train_data:
            mode = train['mode']
            arrival_time = train['aimed_arrival_time']
            print(f"Train mode: {mode}, Arrival time: {arrival_time}")
    
        arrival_time = datetime.strptime(train['aimed_arrival_time'], '%H:%M')
    
        your_station = None 
        
        train_platform = None   
        next_train = None
        train_origin = None
        train_destination = None
        
        next_bus = None
        bus_origin = None
        bus_destination = None 

        for arrival in train_data:
    #     arrival_time = datetime.strptime(train['aimed_arrival_time'], '%H:%M')
            # arrival_time = uk_timezone.localize(datetime.strptime(f"{datetime.now().date()} {arrival['aimed_arrival_time']}", "%Y-%m-%d %H:%M"))
            arrival_time = uk_timezone.localize(datetime.strptime(arrival['aimed_arrival_time'], "%H:%M")).strftime("%H:%M")
            print(f'arrival_time = {arrival_time}')
    
#     if train or bus
        if arrival['mode'] == 'train':
            if next_train is None or (arrival_time > current_time and arrival_time < next_train):
                next_train = arrival_time
                train_origin = arrival['origin_name']
                train_platform = arrival['platform']
                train_destination = arrival['destination_name']
                your_station = data['station_name']
            
        if arrival['mode'] == 'bus':
            if next_bus is None or (arrival_time > current_time and arrival_time < next_train):
                next_bus = arrival_time
                bus_origin = arrival['origin_name']
                bus_destination = arrival['destination_name']

        # if next_train:
        #     print(f'the next train for {your_station} is arriving at {next_train}, on Platform {train_platform}, from: {train_origin}, destination: {train_destination}')

        # if next_bus:
        #     print(f'the next train is arriving at {next_bus}, from: {bus_origin}, destination: {bus_destination}')

            
            # look at Geoffs example.
        # next_train_info = data
            # next_train_info = get_next_train(newdata['station_name'])

        return render_template('show_nexttrain.html', train_data=train_data, your_station=your_station, arrival_time=arrival_time, train_platform=train_platform)
    # else:
    #         # if 
    #     return "Failed to fetch train data2."
    else:
        return "Invalid station code. Please enter a 3-letter alphabetic code."


# Route to show more trains
@app.route('/show_more_trains')
def show_more_trains():
    # Logic to fetch and display more trains
    # Your logic to fetch more trains data goes here

    # Render template with more trains data
    return render_template('show_more_trains.html', trains=more_trains_data)

# Route to show buses
@app.route('/show_buses')
def show_buses():
    # Logic to fetch and display buses
    # Your logic to fetch buses data goes here

    # Render template with buses data
    return render_template('show_buses.html', buses=buses_data)

# @app.route('/reviews/<ID>')
# def show_reviews(ID):
#     for review in reviews:
#         if review['id'] ==ID:
#             review_text = review['review_text']
#             book_title = review['book_title']
#     return render_template('show.html', ID=ID,book_title =book_title, review_text=review_text )

if __name__ == '__main__':
    app.run(port=8000)
