# Module 10 Challenge
**Advanced SQL, SQLAlchemy, ORM**

## Background
Finally! I am treating myself to a long holiday vacation in Honolulu, Hawaii.🏝️
To help with my trip planning, I decided to do a climate analysis about the area. 
The following sections outline the steps that I took to accomplish this task.

## Software
GitHub, Jupyter Notebook, Python, SQLAlchemy, Flask

## This challenge has the following sections:

### Part 1: Analyze and Explore the Climate Data
In this section, I used Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database. Specifically, I used SQLAlchemy ORM queries, Pandas, and Matplotlib.

#### ☔ Precipitation Analysis
#### ☔ Weather Station Analysis


### Part 2: Design Your Climate App
After I completed my initial analysis, I designed a Flask API based on the queries that I developed.
The Flask API has the following options:

1) **Welcome homepage** listing all the available routes.
2) **Precipitation** route to convert the results from the precipitation analysis into a dictionary
   and return the JSON representation of the dictionary.
3) **Weather Stations** route to return a JSON list of weather stations.
4) **Temperature Observations** route to:
     a) Query the dates and temperature observations of the most-active station for the previous year of data.
     b) Return a JSON list of temperature observations for the previous year.
5) **Starting Date** route and **Date Range** to:
     a) Return a JSON list of the minimum temperature, the average temperature, 
        and the maximum temperature for a specified start or start-end range.
     b) For a specified start date, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
     c) For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

## Summary
Most definitely, I will not be traveling to the location of station USC00519281. Too much rain!

