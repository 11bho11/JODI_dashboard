# JODI Exploratory Dashboard        

This repository contains the code for setting up a Dash (Plotly) interactive dashboard to view data from the JODI World Database, developed with Python. The project aims to facilitate exploratory analysis on oil and gas product flows.

The JODI (Joint Organisations Data Initiative) World database consists of oil & gas data for over 120 countries, with historical data dating back to Jan 2002. The goal of the database is to provide a transparent and reliable platform for oil & gas data. Learn more about the history of JODI [here](https://www.ief.org/jodi/history). 

Data frequency is monthly. The data feed is updated monthly, with a 2-3 month lag period. Find more about JODI release dates [here](https://www.jodidata.org/). 


## Why did I build this?

The world of commodities can be a very mysterious place, and data is king to making important decisions in the industry. There are only so many publicly available databases such as EIA, IEA, CFTC. I could not view JODI data unless I bulk-downloaded an Excel file with 10M+ rows. 

Luckily, I found out that the JODI was accessible for free via Nasdaq. However, both JODI and Nasdaq had no way to visualise data nicely, unlike the EIA which does a great job. Therefore, I built this exploratary dashboard which automatically pulls data via the Nasdaq Data Table API, making the platform smooth and light.


## Getting Started
The JODI World database is available via the Nasdaq Data Link Tables API for free. Check out more on Nasdaq's website [here](https://data.nasdaq.com/databases/JODI#:~:text=This%20database%20provides%20comprehensive%20and,from%20production%20to%20end%20use.) 

You will need to register an account to get an API key which is needed to run the app. 

### Setup
1. Clone the repository
   ```
   git clone https://github.com/11bho11/JODI_dashboard.git
   ```
   
2. Install required Python packages
   ```
   pip install -r requirements.txt
   ```
   
3. Save your API key in an `.env` file to store private credentials securely. Save as the following:
   ```
   nasdaq_api_key = "YOUR_API_KEY"
   ```

### Usage
Run the main.py script and the app will be executed on your local machine.

## App Details
There is a filter box located at the top-left which lets you filter by country, energy, unit, and dates.

Below the filter box you can find a summary box with the energy products' most relevant or important information

Both charts on the right enables you to filter by both product and flow

