import streamlit as st
import pandas as pd
import plotly_express as px

# Read data
df_vehicles = pd.read_csv('vehicles_us.csv')

# Filling all missing values
# Filling 'odometer' missing values with the median
median_odometer = df_vehicles['odometer'].median()
df_vehicles['odometer'] = df_vehicles['odometer'].fillna(median_odometer)

#Convert 'odometer' to integer
df_vehicles['odometer'] = df_vehicles['odometer'].astype(int)

# Filling missing 'model_year' values based on 'odometer'
median_model_year = df_vehicles['model_year'].median()
df_vehicles['model_year'] = df_vehicles['model_year'].fillna(median_model_year)

# Convert 'model_year' to int
df_vehicles['model_year'] = df_vehicles['model_year'].astype(int)

# Filling missing 'cylinders' with -1 and convert to integer type
df_vehicles['cylinders'] = df_vehicles['cylinders'].fillna(-1)
df_vehicles['cylinders'] = df_vehicles['cylinders'].astype(int)

# Filling all unknown 'paint_color' entries with 'unknown'
df_vehicles['paint_color'] = df_vehicles['paint_color'].fillna('unknown')

# Fill in null values with -1
df_vehicles['is_4wd'] = df_vehicles['is_4wd'].fillna(-1)

# Convert 'is_4wd' column to integer type
df_vehicles['is_4wd'] = df_vehicles['is_4wd'].astype(int)

# Separating 'model' column into proper 'make' and 'model' columns
# Rename the original 'model' column to ease in later removal
df_vehicles.rename(columns={'model': 'original_model'}, inplace=True)

# Define the function to remove everything after the second space
def remove_after_second_space(text):
    parts = text.split(' ')
    if len(parts) > 2:
        return ' '.join(parts[:2])  # Join first two parts if more than two parts exist
    else:
        return text  # Return as is if less than two parts

# Apply the function to the 'model' column and create 'model_trimmed'
df_vehicles['model_trimmed'] = df_vehicles['original_model'].apply(remove_after_second_space)

# Perform the split transformation on 'model_trimmed'
split_df = df_vehicles['model_trimmed'].str.split(' ', n=1, expand=True)

# Label the columns as 'make' and 'model'
split_df.columns = ['make', 'model']

# Concatenate the split_df back into df_vehicles
df_vehicles = pd.concat([df_vehicles, split_df], axis=1)

# Drop the original 'model' and intermediate 'model_trimmed' columns
df_vehicles.drop(columns=['original_model', 'model_trimmed'], inplace=True)

# Rename 'type' column for clarify
df_vehicles.rename(columns={'type': 'vehicle_type'}, inplace=True)

# Create dropdown menu to select the make of a car
# Include an 'all' selection for make
make = ['all'] + df_vehicles['make'].unique().tolist()
selected_make = st.selectbox('Select a manufacturer', make)

# Create slider bar to select a range of years
min_year, max_year = int(df_vehicles['model_year'].min()), int(df_vehicles['model_year'].max())
year_range = st.slider('Choose years', value=(min_year, max_year), min_value=min_year, max_value=max_year)
actual_range = list(range(year_range[0], year_range[1]+1))

# Filter the dataframe based on the selected make and year range
if selected_make == 'all':
    df_filtered = df_vehicles[df_vehicles.model_year.isin(actual_range)]
else:
    df_filtered = df_vehicles[(df_vehicles['make'] == selected_make) & (df_vehicles.model_year.isin(actual_range))]

# Create a new model_year column for display purposes
df_filtered['model_year_display'] = df_filtered['model_year'].apply(lambda x: f'{x}')

# Drop the original 'model_year' column and rename 'model_year_display' to 'model_year'
df_filtered = df_filtered.drop(columns=['model_year']).rename(columns={'model_year_display': 'model_year'})

# Define the desired column order
new_order = ['make', 'model', 'model_year', 'price', 'condition', 'odometer', 'fuel', 
             'transmission', 'cylinders', 'vehicle_type', 'paint_color', 'is_4wd', 'date_posted', 'days_listed']

# Reorder the columns in the DataFrame
df_filtered = df_filtered[new_order]

# Streamlit formating 
st.header('Market of Used Cars')
st.write("""
##### Filter the data below to see the ads by manufacturer
""")
# Display filtered dataframe with newly formatted 'model_year' and drop old
st.dataframe(df_filtered)


# Price analysis 
st.header('Price analysis')
st.write("""
##### What factor influences price the most? 
""")

list_for_hist = ['transmission','vehicle_type','condition','cylinders']

selected_type = st.selectbox('Price based on:', list_for_hist)

fig1 = px.histogram(df_vehicles, x='price', color= selected_type)
fig1.update_layout(title= "<b> Split of price by {}</b>".format(selected_type))

st.plotly_chart(fig1)

st.write("""
##### How does odometer reading, days on market, or color affect price? 
""")

# Create a separate age column to assist in our analysis
df_vehicles['age'] = 2024 - df_vehicles['model_year']

# Create interactive scatterplot
def age_category(x):
    if x<5: return '<5'
    elif x>=5 and x<10: return '10-20'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'

df_vehicles['age_category'] = df_vehicles['age'].apply(age_category)

list_for_scat = ['odometer', 'days_listed', 'paint_color']
choice_for_scat = st.selectbox('Price based on:', list_for_scat)

fig2 = px.scatter(df_vehicles, x='price', y=choice_for_scat, color= 'age_category', hover_data=['model_year'])
fig2.update_layout(title='<b> Price vs {}</b>'.format(choice_for_scat))

st.plotly_chart(fig2)
