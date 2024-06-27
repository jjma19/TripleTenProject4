# Market of Used Cars Web App
This project is a web application built using Streamlit that allows users to explore and analyze a dataset of cars in the US. The application provides functionalities to filter the dataset based on manufacturer and model year, as well as to visualize various aspects of the data through histograms and scatter plots.

Features
Data Cleaning and Preparation: The app handles missing values and converts data types to ensure clean and accurate data.
Interactive Filtering: Users can filter the data by manufacturer and model year using dropdown menus and sliders.
Dynamic Data Display: The filtered data is displayed in an interactive table.
Price Analysis: Visualizations to explore how different factors influence car prices.

Getting Started
Prerequisites
Python 3.7 or higher
Streamlit
pandas
plotly

Installation
1. Clone the repository
git clone <repository-url>
2. Navigate to teh project directory
cd <project-directory>
3. Install the required packages
pip install -r requirements.txt

Usuage
1. Run the Streamlit app
streamlit run app.py
2. Open your web browser and go to http://localhost:8501.

Data Preparation
The dataset used in this app is vehicles_us.csv. Before any analysis, the data goes through several cleaning steps:

Fill Missing Values:
'odometer' is filled with the median value.
'model_year' is filled with the median value.
'cylinders' is filled with -1.
'paint_color' is filled with 'unknown'.
'is_4wd' is filled with -1.

Convert Data Types:
'odometer', 'model_year', 'cylinders', and 'is_4wd' are converted to integer type.

Split and Rename Columns:
The 'model' column is split into 'make' and 'model' columns.
The 'type' column is renamed to 'vehicle_type'.

Interactive Filters
Manufacturer and Model Year Filters
Users can select a car manufacturer from a dropdown menu and choose a range of model years using a slider. The filtered data is then displayed in an interactive table.

Price Analysis
Histogram
A histogram is used to show the distribution of car prices based on various factors such as transmission, vehicle type, condition, and cylinders.

Scatter Plot
A scatter plot is used to explore how factors such as odometer reading, days on market, and paint color affect car prices. Cars are categorized by age.

Acknowledgments
Streamlit for providing an easy way to create web applications.
Plotly for the powerful visualization library.
Data source: vehicles_us.csv.
This README.md provides an overview of the project, its features, and instructions for setting up and running the web app.

Public Web Link: https://vehicle-data-dashboard-1mma.onrender.com