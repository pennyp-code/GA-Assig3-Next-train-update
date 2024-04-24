# import os
# import requests
# import pytz
# from dotenv import load_dotenv
# from datetime import datetime


# load_dotenv()

# API_Key = os.getenv('API_Key')
# print(API_Key)
# API_ID = os.getenv('API_ID')
# print(API_ID)

# """
# Notes: for why we use the different parameter options
# GET /v3/uk/train/station_timetables/{id}.json
# `https://transportapi.com/v3/uk/train/station_timetables/${trainStation}.json?app_id=${appId}&app_key=${appKey}&train_status=passenger`
# # example date
# # datetime = 2022-02-03T20:30:00+01:00

# # goes into the future
# # to_offset=PT06:00:00

# # no need to add from_offset as we dont care about past arrivals
# # from_offset = 0

# # we want arrivals not departures and not stopping
# # type = arrival

# # we want passenger trains as we want to catch the train
# # train_status = passenger
# """

# my_id = API_ID
# my_key = API_Key
# # id for richmond station
# api_url = 'https://transportapi.com/v3/uk/train/station_timetables/{id}.json'
# station_id = 'crs:RMD'
# url = api_url.format(id=station_id)

# base_url = 'https://transportapi.com/v3/uk/train/station_timetables/${trainStation}.json?app_id=${appId}&app_key=${appKey}&train_status=passenger'

# params = {'app_id' : my_id,
#           'app_key' : my_key,
#           'id' : station_id,
#           'train_status' : 'passenger',
#           'trainStation' : station_id,
#           'type' : 'arrival',
# #           'datetime': '2022-02-03T20:30:00+01:00',
#           'to_offset' : 'PT01:30:00',
#           'from_offset' : '-PT00:00:00'
#         }
# response = requests.get(url, params=params)
# if response.status_code == 200:
#     data = response.json()
#     print(data)
# else:
#     print("Failed to retrieve data:", response.text)

# #  so we can see that out train data is actually nested so:
# train_data = data['arrivals']['all']
# print(train_data)

# #  so we can see that out train data is actually nested so:
# train_data = data['arrivals']['all']

# # i did get the time conversion for the uk from chatgpt# 

# # Create a timezone object for UK (London)
# uk_timezone = pytz.timezone('Europe/London')

# # Get the current datetime in the UK with the timezone
# current_datetime_uk = datetime.now(uk_timezone)

# # Extract only the time from the datetime object
# current_time_uk = current_datetime_uk.time()

# # Print the current time in the UK
# print("Current time in the UK:", current_time_uk.strftime('%H:%M'))
       
# # so the current time is 
# current_time = current_datetime_uk

# # just to check print all the arrival times and trains in the next x hours.
# for train in train_data:
#     mode = train['mode']
#     arrival_time = train['aimed_arrival_time']
#     print(f"Train mode: {mode}, Arrival time: {arrival_time}")
    
#     arrival_time = datetime.strptime(train['aimed_arrival_time'], '%H:%M')
# #     make sure todays date 
# #     train_arrival_datetime = datetime.combine(current_datetime_uk.date(), time(hours, minutes), tzinfo=uk_timezone)
    
# #     print (arrival_time)
# #     print(datetime)
    
    
# next_train = None
# next_bus = None
# train_origin = None
# train_destination = None
# bus_origin = None
# bus_destination = None 

# for arrival in train_data:
# #     arrival_time = datetime.strptime(train['aimed_arrival_time'], '%H:%M')
#     arrival_time = uk_timezone.localize(datetime.strptime(f"{datetime.now().date()} {arrival['aimed_arrival_time']}", "%Y-%m-%d %H:%M"))
#     print(f'arrival_time = {arrival_time}')
    
# #     if train or bus
#     if arrival['mode'] == 'train':
#         if next_train is None or (arrival_time > current_time and arrival_time < next_train):
#             next_train = arrival_time
#             train_origin = arrival['origin_name']
#             train_destination = arrival['destination_name']
            
#     if arrival['mode'] == 'bus':
#         if next_bus is None or (arrival_time > current_time and arrival_time < next_train):
#             next_bus = arrival_time
#             bus_origin = arrival['origin_name']
#             bus_destination = arrival['destination_name']
        
# if next_train:
#     print(f'the next train is arriving at {next_train}, from: {train_origin}, destination: {train_destination}')

# if next_bus:
#     print(f'the next train is arriving at {next_bus}, from: {bus_origin}, destination: {bus_destination}')
        #    return next_train, next_bus, train_origin, train_destination, bus_origin, bus_destination

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('index.html')

# @app.route('/next_5trains_results', methods=['POST'])
# def next_5trains_results():
#     if request.method == 'POST':
#         station_code = request.form['station_code'].strip().upper()  # Convert to uppercase and remove leading/trailing spaces
#         if len(station_code) != 3 or not station_code.isalpha():
#             return "Invalid station code. Please enter a 3-letter code."
#         station_id = "crm:" + station_code
#         train_data = train_data(station_id)
#         if train_data:
#             next_train, next_bus, train_origin, train_destination, bus_origin, bus_destination = get_next_train(train_data)
#             return render_template('next_5trains')
#         else:
#             return "Failed to fetch train data."
#     # data = get_data(station_id)
#     return render_template('next_train_result.html', data=data)

# if __name__ == '__main__':
#     app.run()
