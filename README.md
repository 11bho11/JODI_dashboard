# JODI Exploratory Dashboard        
An interactive dashboard developed using Dash (Plotly) and python to visualise data from the JODI World Database. The project aims to facilitate exploratory analysis on global oil and gas product flows.

## About the Project
The JODI (Joint Organisations Data Initiative) World Database consists of oil & gas data from over 120 countries, with historical data dating back to Jan 2002. The goal of the database is to improve transparency within the global energy markets. Learn more about the history of JODI [here](https://www.ief.org/jodi/history). 

Data frequency is monthly. The data feed is updated monthly, with a 2-3 month lag period. Find more about JODI release dates [here](https://www.jodidata.org/). 


## Why did I build this?
There are frustratingly only a few public energy databases such as EIA, IEA, and CFTC that can be used to explore. The JODI database was freely available, but was difficult to access or analyse effectively. 

While JODI data is accessible on Nasdaq Data Link, there was no interface for data visualisation, unlike other public databases like the EIA. Therefore, I built this project which does the following:
- Automatically fetches live data via the Nasdaq Data Table API
- Allows for interactive filtering by product,flow, and country
- Visualise clean data without having to download data manually

## Getting Started
The dashboard connects to the Nasdaq JODI Database via the Nasdaq Data Link Tables API. Learn more about Nasdaq tables [here](https://data.nasdaq.com/databases/JODI#:~:text=This%20database%20provides%20comprehensive%20and,from%20production%20to%20end%20use.) 

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
   
3. Save your API key in an `.env` file in the root directory to store private credentials securely. Save as the following:
   ```
   nasdaq_api_key = "YOUR_API_KEY"
   ```

### Usage
Run the main.py script to start the Dash app. Open your browser to view the dashboard.

## App Details
![image](https://github.com/user-attachments/assets/bb7a1ab2-9025-46c9-8fa8-867d74266fd7)
- Sidebar controls located at the top-left which lets you filter by country, energy, unit, and dates.
- Below the controls you can find a summary box with the most up-to-date or relevant information.
- Charts on the right enables you to filter by both product and flow to show product breakdown by flow, or flow breakdown by product.

