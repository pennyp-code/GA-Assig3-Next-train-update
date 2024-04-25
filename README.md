# Train time table data from the UK.  
## Website
free API Key and ID can be requested from
https://transportapi.com

Note:
This is My first use of git, with github and vscode.
https://github.com/pennyp-code/GA-Assig3-Next-train-update

## Languages
This python app, uses Flask and jinja, and some html and CSS.

## Project idea
data from london train timetables is fetched once the user enters the train station they want
the idea is..... 
then they are told when the next 5 trains arrive.  
then they are told what train line this train is on.  they can then look up all the stations for this trainline.

## EndPoints
### api_key and api_id are required from sign up.
GET /v3/uk/train/station_timetables/{id}.json
`https://transportapi.com/v3/uk/train/station_timetables/${trainStation}.json?app_id=${appId}&app_key=${appKey}&train_status=passenger`

## parameter options
- example date
    datetime = 2022-02-03T20:30:00+01:00
- Can make calls for times into the future using to_offset
    to_offset=PT06:00:00
- I intially used PT06:00 to not get too much data back, however changed this to PT12:00 once this was working as I found that over night there were gaps of more than 12 hours until the next train due.   (usually after 2.30 am local uk time).
- There is a from_offset
     to see what trains were due (and you can check if the train actually arrived), but as we dont care about past arrivals for this app i left that as is from_offset = 0
- we want arrivals not departures and not stopping
    therefore used type = arrival
- we want passenger trains as we want to catch the train, so i used train_status = passenger

## Running the app.
- currently the port is set at 8000:  
    please feel free to change that to suit your requirements.
- currently debug=True
    please feel free to change that to suit your requirements
- the index page is set to '/Welcome'
- run the app, then open the link to the route and add '/Welcome'
- the index route or /Welcome page: - displays information to the user about entering their 3letter code for their choosen station.  There are some examples, however due to 
 a. the time delay between Australia and the UK means there is a period of time where there may be no trains or buses expected for the next 12 hours.
 b. the API only allows 30 hits per day.
 c. each train station has different busy times for trains and buses.

- Once the Station Code is entered into the index page (using a form) the route /show_nexttrain.html. is automatically shown to the user. 
On the /show_nexttrain.html page the the current time for the uk is always shown, then if there is data returned the following data is shown. station choosen, the next train arrival time, and what platform your train will arrive on. (If the next arrival is a bus the platform is shown as None)
The user has the option to press two buttons:
    1. show/hide more trains - which shows the trains due to arrive at the choosen station in the next 12 hours.
    2. show/hid buses - which shows the buses due to arrive at the choosen station in the next 12 hours. (this is a nice to have and additional to the original scope)

## Return data type is json data.
 
## Development and Testing
- for the purposes of testing I mainly used RMD and RED (Richmond and Redruth) stations as they seem to have a spread of bus and train arrivals 
- I ran out of API calls for the short time i had to design and test so there may be instances during future development that cases may arrise that have not been tested for.
- the user is given information to find codes as there many trainlines and a multiude of codes.  Some of which are duplicates. 
- i have commented out the print statements used in testing (but these are handy and can be uncommented out.(i do not know the python equivallent to kdebug for print statements))


## Future updates:
- As this app is now functioning the next step would be for me to increase the to_offset to its max and check a large range of stations to ensure the majority of train 
    and bus arrivals are covered, especially for those stations that have less volume.   
-  I have not had time to investigate what happens for those train stations with duplicate codes.  
    I suppect for the future if i update this app i would have to add in either a check in return data that checks the station name for all data and allows the user to 
    choose which of the stations they want to look at or add a column so that each train and bus shows which station. 

