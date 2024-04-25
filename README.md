# Train time table data from <enter the web location>
## api key and api id are required from sign up.

This is My first use of git, with github and vscode.

This python app, uses Flask and jinja, and some html and CSS.

GET /v3/uk/train/station_timetables/{id}.json
`https://transportapi.com/v3/uk/train/station_timetables/${trainStation}.json?app_id=${appId}&app_key=${appKey}&train_status=passenger`


data from london train timetables is fetched once the user enters the train station they want
the idea is..... 
then they are told when the next 5 trains arrive.  
then they are told what train line this train is on.  they can then look up all the stations for this trainline.

# parameter options
- example date
- datetime = 2022-02-03T20:30:00+01:00

- goes into the future
- to_offset=PT06:00:00
- am going to put this to 12 hours once working so we can see the next train if we are after 2am as there
- is a gap of more than 6 hours between trains over night in some instances.

- no need to add from_offset as we dont care about past arrivals
- from_offset = 0

- we want arrivals not departures and not stopping
- type = arrival

- we want passenger trains as we want to catch the train
- train_status = passenger
