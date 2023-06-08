# Streamlit is a Python library used for building web applications with simple Python scripts.
import streamlit as st

# Pandas is a Python library used for data manipulation and analysis.
import pandas as pd

# Plotly Express is a Python library used for creating interactive visualizations.
import plotly.express as px

# SQLAlchemy is a Python library used for working with SQL databases.
# 'create_engine' is used to establish 
# a connection to a database, while 'text' is used to create SQL queries as strings.
from sqlalchemy import create_engine, text

#---------------------------------------------------------------------------------------------------

# Connect to the MySQL database
# create engine with database credentials
engine = create_engine('mysql+pymysql://root:GItamsai123$@localhost:3306/phonepe_database')
# establish a connection to the database
connection = engine.connect()

# Note: Replace 'root' with your username and 'GItamsai123$' with your password
# Note: Replace 'localhost:3306' with the host and port number of your MySQL database
# Note: Replace 'phonepe_database' with the name of your database

#----------------------------------------------------------------------------------------------------

#The code is reading data from a database using SQL queries and the pandas.read_sql function.

#The first query selects all data from the agg_transaction_table and 
#assigns it to a pandas DataFrame called df.

#The second query selects all data from the longitude_latitude_state_table and 
#assigns it to a pandas DataFrame called state.

#The third query selects all data from the districts_longitude_latitude_table and 
#assigns it to a pandas DataFrame called districts.

#The fourth query selects all data from the district_map_transaction_table and 
#assigns it to a pandas DataFrame called districts_tran.

#The fifth query selects all data from the district_map_registering_table and 
#assigns it to a pandas DataFrame called app_opening.

#The sixth query selects all data from the agg_userbydevice_table and assigns it 
#to a pandas DataFrame called user_device.

#Finally, the code closes the database connection.

#It's important to note that the variable connection must have been 
#previously defined and established a connection to the database before the queries are executed.


# Read data from the database tables
query1 = text('SELECT * FROM agg_transaction_table')
df = pd.read_sql(query1, con=connection)

query2 = text('SELECT * FROM longitude_latitude_state_table')
state = pd.read_sql(query2, con=connection)

query3 = text('SELECT * FROM districts_longitude_latitude_table')
districts = pd.read_sql(query3, con=connection)

query4 = text('SELECT * FROM district_map_transaction_table')
districts_tran = pd.read_sql(query4, con=connection)

query5 = text('SELECT * FROM district_map_registering_table')
app_opening = pd.read_sql(query5, con=connection)


query6 = text('SELECT * FROM agg_userbydevice_table')
user_device = pd.read_sql(query6, con=connection)

# Close the database connection
connection.close()


#--------------------------------------------------------------------------------------------------
#sorts the rows of the state dataframe by the 'state' column in ascending order.
state = state.sort_values(by='state')
#resets the index of the state dataframe after sorting it.
state = state.reset_index(drop=True)

#groups the df dataframe by 'State' column and sums the 'Transaction Count' and 
# 'Transaction Amount' columns for each group, and stores the result in df2 dataframe.
df2 = df.groupby(['State']).sum()[['Transaction Count', 'Transaction Amount']]
#resets the index of the df2 dataframe after grouping and summing.
df2 = df2.reset_index()

#creates a copy of the state dataframe, which is used as the basis for creating a choropleth map.
choropleth_data = state.copy()

#----------------------------------------------------------------------------------------------------
# iterate through each column in df2
for column in df2.columns:
      # Add the data from the current column in df2 to choropleth_data with the same column name
    choropleth_data[column] = df2[column]
# Drop the 'State' column from choropleth_data
choropleth_data = choropleth_data.drop(labels='State', axis=1)

# Rename the 'State' column in df to 'state'
df.rename(columns={'State': 'state'}, inplace=True)
# Create a list of state names, formatted with hyphens instead of spaces
sta_list = ['andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
            'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
            'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
            'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
            'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
            'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
            'uttarakhand', 'west-bengal']
# Create a new DataFrame called 'state' with a single column 'state' containing the state names
state['state'] = pd.Series(data=sta_list)
# Merge the 'df' DataFrame with the 'state' DataFrame using an outer join on the 'state' column
state_final = pd.merge(df, state, how='outer', on='state')
# Merge the 'districts_tran' DataFrame with the 'districts' 
# DataFrame using an outer join on the 'State' and 'District' columns
districts_final = pd.merge(districts_tran, districts,
                           how='outer', on=['State', 'District'])

#--------------------------------------------------------------------------------------------------
# Display balloons for fun
st.balloons()
# Create a container to hold the page content
with st.container():
    # Display a title and subheader for the page
    st.title(':violet[PhonePe Pulse Data Visualization(2018-2022)]')
    st.write(' ')
    st.subheader(
        ':violet[Registered user & App installed -> State and Districtwise:]')
    st.write(' ')
    # Create a selectbox to choose the year for data visualization
    scatter_year = st.selectbox('Please select the Year',
                                ('2018', '2019', '2020', '2021', '2022'))
    st.write(' ')
    # Create a selectbox to choose the state for data visualization
    scatter_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                         'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                         'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                         'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                         'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'), index=10)
    # Convert selected year to integer
    scatter_year = int(scatter_year)
    # Filter data based on selected year and state
    scatter_reg_df = app_opening[(app_opening['Year'] == scatter_year) & (
        app_opening['State'] == scatter_state)]
    # Create scatter plot using Plotly Express
    #The scatter plot shows the relationship between the "District" variable on 
    #the x-axis and the "Registered User" variable on the y-axis. The color 
    #parameter assigns a unique color to each district, while the hover_name 
    #parameter specifies that the name of each district should appear when hovering over its
    #corresponding data point.
    #The hover_data parameter specifies additional information to be displayed
    #when hovering over a data point. In this case, the "Year", "Quarter", and "App Opening"
    #columns are added to the hover tooltip.
    #The size_max parameter sets the maximum size of the data points in the plot.
    scatter_register = px.scatter(scatter_reg_df, x="District", y="Registered User",  color="District",
                                  hover_name="District", hover_data=['Year', 'Quarter', 'App Opening'], size_max=60)
    # Display scatter plot on the page using Streamlit
    st.plotly_chart(scatter_register)
# Add some extra space to the page for readability
st.write(' ')
#---------------------------------------------------------------------------------------------------
#creates a set of tabs in the Streamlit app interface, where each tab can
#display a different type of information or analysis.
geo_analysis, Device_analysis, payment_analysis, transac_yearwise = st.tabs(
    ["Geographical analysis", "User device analysis", "Payment Types analysis", "Transacion analysis of States"])

#--------------------------------------------------------------------------------------------------
with geo_analysis:
    st.subheader(':violet[Transaction analysis->State and Districtwise:]')
    st.write(' ')
    
    # Select the Year using a radio button
    Year = st.radio('Please select the Year',
                    ('2018', '2019', '2020', '2021', '2022'), horizontal=True)
    st.write(' ')
    
    # Select the Quarter using a radio button
    Quarter = st.radio('Please select the Quarter',
                       ('1', '2', '3', '4'), horizontal=True)
    st.write(' ')
    
    # Convert selected Year and Quarter to integers
    Year = int(Year)
    Quarter = int(Quarter)
    
    # Filter the district data based on the selected Year and Quarter
    plot_district = districts_final[(districts_final['Year'] == Year) & (
        districts_final['Quarter'] == Quarter)]
    
    # Filter the state data based on the selected Year and Quarter
    plot_state = state_final[(state_final['Year'] == Year)
                             & (state_final['Quarter'] == Quarter)]
    
    # Group the state data by state, Year, Quarter, Latitude, and Longitude and calculate the sum of transaction values
    plot_state_total = plot_state.groupby(
        ['state', 'Year', 'Quarter', 'Latitude', 'Longitude']).sum()
    plot_state_total = plot_state_total.reset_index()
    
    # Define state codes for mapping
    state_code = ['AN', 'AD', 'AR', 'AS', 'BR', 'CH', 'CG', 'DNHDD', 'DL', 'GA',
                  'GJ', 'HR', 'HP', 'JK', 'JH', 'KA', 'KL', 'LA', 'LD', 'MP', 'MH',
                  'MN', 'ML', 'MZ', 'NL', 'OD', 'PY', 'PB', 'RJ', 'SK', 'TN', 'TS',
                  'TR', 'UP', 'UK', 'WB']
    
    # Assign state codes to the state data for mapping
    plot_state_total['code'] = pd.Series(data=state_code)
    
# Create a scatter plot for district data on a geographical map
fig1 = px.scatter_geo(plot_district,
                      lon=plot_district['Longitude'],
                      lat=plot_district['Latitude'],
                      color=plot_district['Transaction_amount'],
                      size=plot_district['Transaction_count'],
                      hover_name="District",
                      hover_data=["State", 'Transaction_amount', 'Transaction_count', 'Year', 'Quarter'],
                      title='District',
                      size_max=22,)

fig1.update_traces(marker={'color': "#CC0044",
                           'line_width': 1})

#---------------------------------------------------------------------------------------------------
# Create a scatter_geo plot
fig2 = px.scatter_geo(plot_state_total,
                      lon=plot_state_total['Longitude'],
                      lat=plot_state_total['Latitude'],
                      hover_name='state',
                      text=plot_state_total['code'],
                      hover_data=['Transaction Count', 'Transaction Amount', 'Year', 'Quarter']
                      )

# Customize the scatter_geo plot's traces
fig2.update_traces(marker=dict(color="#D5FFCC", size=0.3))

# Create a choropleth plot
fig = px.choropleth(choropleth_data,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    color='Transaction Amount',
                    color_continuous_scale='twilight',
                    hover_data=['Transaction Count', 'Transaction Amount'])

# Update the choropleth plot's geos settings
fig.update_geos(fitbounds="locations", visible=False)

# Add the scatter_geo and choropleth plots to a single figure
fig.add_trace(fig1.data[0])  # Assuming fig1 is defined earlier
fig.add_trace(fig2.data[0])

# Set the layout of the figure
fig.update_layout(height=1000, width=1000)

# Add spacing between the components
st.write(' ')
st.write(' ')

# Add a button to display the map in a new browser window
if st.button('Click here to see map clearly'):
    fig.show(renderer="browser")

# Display the figure in Streamlit
st.plotly_chart(fig)
#----------------------------------------------------------------------------------------------------

# Analysis of User Device
with Device_analysis:
    st.subheader(':violet[User Device analysis->Statewise:]')
    
    # Select State
    tree_map_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                          'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                          'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                          'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                          'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                          'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                          'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                          'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                          'uttarakhand', 'west-bengal'), index=10, key='tree_map_state')
    
    # Select Year
    tree_map_state_year = int(st.radio('Please select the Year',
                                       ('2018', '2019', '2020', '2021', '2022'), horizontal=True, key='tree_map_state_year'))
    
    # Select Quarter
    tree_map_state_quater = int(st.radio('Please select the Quarter',
                                         ('1', '2', '3', '4'), horizontal=True, key='tree_map_state_quater'))
    
    # Filter the data based on user selection
    user_device_treemap = user_device[(user_device['State'] == tree_map_state) & (user_device['Year'] == tree_map_state_year) &
                                      (user_device['Quarter'] == tree_map_state_quater)]
    
    # Convert Brand_count to string type
    user_device_treemap['Brand_count'] = user_device_treemap['Brand_count'].astype(str)
    
# Create Treemap
user_device_treemap_fig = px.treemap(user_device_treemap, path=['State', 'Brand'], values='Brand_percentage', hover_data=['Year', 'Quarter'],
                                         color='Brand_count',
                                         title='User device distribution in ' + tree_map_state +
                                         ' in ' + str(tree_map_state_year)+' at '+str(tree_map_state_quater)+' quarter',)
                                         
# Display Treemap
st.plotly_chart(user_device_treemap_fig)

# Create Bar Chart
bar_user = px.bar(user_device_treemap, x='Brand', y='Brand_count', color='Brand',
                    title='Bar chart analysis', color_continuous_scale='sunset',)
                    
# Display Bar Chart
st.plotly_chart(bar_user)


#---------------------------------------------------------------------------------------------------
# Payment Type Analysis
with payment_analysis:
    st.subheader(':violet[Payment type Analysis -> 2018 - 2022:]')
    
    # Read payment mode data from CSV file
    payment_mode = pd.read_csv('transaction_df.csv', index_col=0)
    
    # Select State
    pie_pay_mode_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                              'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                              'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                              'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                              'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                              'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                              'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                              'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                              'uttarakhand', 'west-bengal'), index=10, key='pie_pay_mode_state')
    
    # Select Year
    pie_pay_mode_year = int(st.radio('Please select the Year',
                                     ('2018', '2019', '2020', '2021', '2022'), horizontal=True, key='pie_pay_year'))
    
    # Select Quarter
    pie_pay_mode_quarter = int(st.radio('Please select the Quarter',
                                        ('1', '2', '3', '4'), horizontal=True, key='pie_pay_quarter'))
    
    # Select values to visualize
    pie_pay_mode_values = st.selectbox(
        'Please select the values to visualize', ('Transaction_count', 'Transaction_amount'))
    
    # Filter the payment mode data based on user selection
    pie_payment_mode = payment_mode[(payment_mode['Year'] == pie_pay_mode_year) & (
        payment_mode['Quarter'] == pie_pay_mode_quarter) & (payment_mode['State'] == pie_pay_mode_state)]
    
# Create Pie Chart
pie_pay_mode = px.pie(pie_payment_mode, values='Transaction Count',
                      names='Transaction Type', hole=.5, hover_data=['Year'])

# Create Bar Chart
pay_bar = px.bar(pie_payment_mode, x='Transaction Type',
                 y='Transaction Count', color='Transaction Type', title="Transaction Count")

# Display Bar Chart
st.plotly_chart(pay_bar)

# Display Pie Chart
st.plotly_chart(pie_pay_mode)

#--------------------------------------------------------------------------------------------------
# Transaction Analysis by Year
with transac_yearwise:
    st.subheader(':violet[Transaction analysis->Statewise:]')
    
    # Select State
    transac_state = st.selectbox('Please select State', ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                                                         'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                                                         'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                                                         'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                                                         'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                                                         'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                                                         'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                         'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                                                         'uttarakhand', 'west-bengal'), index=10, key='transac')
    
    # Select Quarter
    transac_quarter = int(st.radio('Please select the Quarter',
                                   ('1', '2', '3', '4'), horizontal=True, key='trans_quarter'))
    
    # Select Transaction Type
    transac_type = st.selectbox('Please select the Mode',
                                ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services', 'Others'), key='transac_type')
    
    # Select values to visualize
    transac_values = st.selectbox(
        'Please select the values to visualize', ('Transaction_count', 'Transaction_amount'), key='transac_values')
    
    # Read payment mode yearwise data from CSV file
    payment_mode_yearwise = pd.read_csv('Transaction_df.csv', index_col=0)
    
    # Group and aggregate data by State, Year, Quarter, and Transaction Type
    new_df = payment_mode_yearwise.groupby(
        ['State', 'Year', 'Quarter', 'Transaction Type']).sum()
    new_df = new_df.reset_index()
    
    # Filter the data based on user selections
    chart = new_df[(new_df['State'] == transac_state) &
                   (new_df['Transaction Type'] == transac_type) & (new_df['Quarter'] == transac_quarter)]
    
# Create Bar Chart by Year
year_fig = px.bar(chart, x='Year', y='Transaction Count', color='Transaction Type', color_continuous_scale='armyrose',
                      title='Transaction analysis '+transac_state + ' regarding to '+transac_type)

# Display the Bar Chart
st.plotly_chart(year_fig)


#---------------------------------------------------------------------------------------------------
# Overall India Analysis Sidebar
with st.sidebar:
    st.subheader(':violet[Overall India Analysis:]')
    
    # Select Values to Visualize
    overall_values = st.selectbox(
        'Please select the values to visualize', ('Transaction Count', 'Transaction Amount'), key='values')
    
    # Overall Transaction Analysis
    overall = new_df.groupby(['Year']).sum()
    overall.reset_index(inplace=True)
    
    # Create Bar Chart for Overall Transaction Analysis
    overall = px.bar(overall, x='Year', y=overall_values, color=overall_values,
                     title='Overall pattern of Transaction all over India', color_continuous_scale='sunset',)
    overall.update_layout(height=350, width=350)
    
    # Display the Bar Chart in the Sidebar
    st.plotly_chart(overall)
    

# Overall User Device Analysis
user_device_overall = pd.read_csv('user_by_device.csv', index_col=0)
overall_device = user_device_overall.groupby(['Brand', 'Year']).sum()
overall_device.reset_index(inplace=True)

# Create Bar Chart for Overall User Device Analysis
overall_dev_fig = px.bar(overall_device, x='Year', y='Brand_count',
                            color='Brand', title='Customer Device pattern from 2018 - 2022')
overall_dev_fig.update_layout(height=350, width=350)

# Display the Bar Chart for User Device Analysis
st.plotly_chart(overall_dev_fig)


# Overall User Registration Analysis
overall_reg = pd.read_csv('district_registering_map.csv')
overall_reg = overall_reg.groupby('Year').sum().reset_index()

# Create Bar Chart for Overall User Registration Analysis
overall_reg_fig = px.bar(
    overall_reg, 
    x='Year', 
    y='Registered User', 
    color_discrete_sequence=['#636EFA'], 
    title='Phonepe Registered Users from 2018 - 2022'
)
overall_reg_fig.update_layout(height=350, width=350)

# Display the Bar Chart for User Registration Analysis
st.plotly_chart(overall_reg_fig)


# Overall App Openings Analysis
overall_app_fig = px.bar(
    overall_reg, 
    x='Year', 
    y='App Opening', 
    color_discrete_sequence=['#EF553B'], 
    title='Phonepe App Openings from 2018 - 2022'
)
overall_app_fig.update_layout(height=350, width=350)

# Display the Bar Chart for App Openings Analysis
st.plotly_chart(overall_app_fig)




