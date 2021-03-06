import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


df = pd.read_csv('df3_fac.csv')
df=df.round(3)

content_string="<p><b>Attributes</b></p><br><p><b>GDP growth (annual %):</b> Annual percentage growth rate of GDP based on local currency </p><p><b>GDP per capita (current US$):</b> Gross domestic product by midyear population. </p><p><b>Imports of goods & services (% GDP):</b> Value of all merchandise received from the world</p><p><b>Manufacturing, value added(% GDP):</b> Value of output minus input for ITIS division 15-37</p><p><b>Trade(% of GDP):</b> Sum of exports and imports of goods and services </p><p><b>Forest area(% of land area):</b> total land area divided by forest area</p><p><b>Forest area(sp.km):</b> it is land under natural or planted stands of trees height of at least 5 meters and a canopy height of 10 percent.</p> <p><b>Life Expectancy At Birth, Total (Years):</b>Expected number of years that a newborn child will live if the mortality rates are the same as the time the child was born.</p><p><b>Population growth (annual %):</b> the exponential rate of growth of midyear population from year t-1 to t, expressed as a percentage.</p><p><b>CO2 emissions (kg per 2010 US$ of GDP):</b>Carbon dioxide emissions are those stemming from the burning of fossil fuels and the manufacture of cement.</p><p><b>Agriculture, forestry, and fishing, value added (% of GDP):</b>value added to the net output of the ISIC( International standard industrial classification ) divisions 1-5 and includes forestry, hunting, and fishing, as well as cultivation of crops and livestock production.</p>"

pd.set_option('display.float_format', lambda x: '%.3f' % x)
html_string = "<br><br>"
st.title(':earth_americas:   GDP PREDICTOR')
st.markdown(html_string, unsafe_allow_html=True)


countries=['Germany',
    'France',
    'United States',
    'United Kingdom',
    'Malaysia',
    'India',
    'China',
    'Japan',
    'Spain',
    'East Asia & Pacific',
    'Europe & Central Asia',
    'Latin America & Caribbean',
    'Sub-Saharan Africa']

seriesName=['GDP per capita (current US$)',
             'GDP growth (annual %)',
             'Imports of goods and services (current US$)',
             'Manufacturing, value added (% of GDP)',
             'Trade (% of GDP)',
             'Forest area (% of land area)',
             'Forest area (sq. km)',
             'Life expectancy at birth, total (years)',
             'Population growth (annual %)',
             'CO2 emissions (kg per 2010 US$ of GDP)',
             'Agriculture, forestry, and fishing, value added (% of GDP)'   ]
        

    

navigate_button = st.sidebar.radio("Select The Page to View", ('GDP Overview','Compare Countries', 'Sun Burst View','Statistical Analysis','Comparisons')) 

if navigate_button=='GDP Overview':
    with st.beta_expander("Select Type"):
        compare_GDP = st.radio("Select type to compare", ('GDP growth (annual %)','GDP per capita (current US$)')) 
    selected_series='GDP growth (annual %)'
    if compare_GDP=='GDP growth (annual %)':
        selected_series='GDP growth (annual %)'
    else:
        selected_series='GDP per capita (current US$)'
    df_gdp = pd.read_csv('df3_fac.csv')
    df_gdp=df_gdp.loc[df_gdp['Indicator Name'] == selected_series]




    year_select = st.select_slider('Select a Year',
    options=['YR2006','YR2007','YR2008','YR2009','YR2010','YR2011','YR2012','YR2013','YR2014','YR2015','YR2016','YR2017','YR2018','YR2019'])
    st.write('Selected Year : ', year_select.replace("YR",""))

    fig = go.Figure(data=go.Choropleth(
        locations = df_gdp['Country Code'],
        z = df_gdp.loc[year_select],
        text = df_gdp['Country Name'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_tickprefix = '$',
        colorbar_title = selected_series,
    ))
    fig.update_layout(
   title=selected_series,
    autosize=True,
    width=1000,
    height=800,
    
    geo=dict(
        showframe=True,
        showcoastlines=True,
        projection_type='equirectangular'
    ))

    st.write(fig)


elif navigate_button=='Compare Countries':

   
    st.header('Comparison between  Countries')
    with st.expander("Select Attributes and countries"):
        option = st.multiselect('What countries do you want to compare?', countries)
        select_event = st.selectbox('Select series to compare?',
                                        seriesName)
    dfa=df.loc[(df['Indicator Name'] == select_event),[1961,1962,1963,1964,1965,1966,1967,1968,1969,1970,1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1995,1996,1997,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]]
    dfa=dfa.T
    dfa.columns=countries
    dfa = dfa.reset_index()

   


    multi_lc = alt.Chart(dfa).transform_fold(
        option,
        ).mark_line().encode(
        x='index:Q',
        y=alt.Y('value:Q', title=''),
        color='key:N'
        
        
    ).properties(
        title=select_event,
        width=600,
        height=400
    ).interactive()
    if(len(option)==0):
            st.line_chart(dfa)
    else:
        st.write( multi_lc )


elif navigate_button=='Statistical Analysis':
    st.header('Data Frame')

    select_event = st.selectbox('Select series to show the dataframe?',
                                        seriesName)

    dfa=df.loc[(df['Indicator Name'] == select_event),[2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]]
    dfa=dfa.T
    dfa.columns=countries
    dfa = dfa.reset_index()
    dfa=dfa.rename(columns={"index": "year"})
    dfa.set_index('year',inplace=True)
    st.write(dfa)
    with st.expander("Expand for Attributes definition"):
        st.markdown(content_string, unsafe_allow_html=True)



    st.header("Statistical Analysis")
    


    select_event = st.selectbox('Select series to show stats?',
                                        seriesName)

    dfa=df.loc[(df.SeriesName == select_event),[2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]]
    dfa=dfa.T
    dfa.columns=countries
    dfa = dfa.reset_index()
    countryName = st.selectbox('Choose country  to show stats?',
                                        countries)
    st.write( dfa.agg({countryName: ['min', 'max', 'mean', 'median']}) )


elif navigate_button=='Sun Burst View':
    st.header("Sun Burst")
    df = pd.read_csv('df3_fac.csv')
    df=df.round(3)
    pd.set_option('display.float_format', lambda x: '%.3f' % x)
    edf = pd.melt(df,id_vars=['IndicatorName','CountryName'], value_vars=[])
    countries = edf['CountryName'].unique()
    series = edf['IndicatorName'].unique()
    year = edf['variable'].unique()
    with st.expander("Select Attributes and countries"):
        select_event = st.selectbox('Select series',series)
        select_year = st.selectbox('Select year',year)
    edf2 = pd.melt(df,id_vars=['IndicatorName','CountryName'], value_vars=[])
    edf2=edf2.loc[edf2['IndicatorName'] == select_event]
    edf2=edf2.loc[edf2.variable == select_year]
    edf2.dropna()
    edf2["value"]=pd.to_numeric(edf2["value"])
    edf2["variable"]=pd.to_numeric(edf2["variable"])
    fig=px.sunburst(edf2, path=['variable','CountryName','IndicatorName'], values='value', width=1000,height=800,hover_name="CountryName", hover_data={'value':True})
    st.plotly_chart(fig)

elif navigate_button=='Comparisons':
   
    compare_button = st.radio("Select type to compare", ('Tree Chart','Bar Charts','Scatter Plots')) 


    if compare_button=='Tree Chart':

        df = pd.read_csv('df3_fac.csv')
        df=df.round(3)
        pd.set_option('display.float_format', lambda x: '%.3f' % x)
        edf = pd.melt(df,id_vars=['IndicatorName','CountryName'], value_vars=[1961,1962])
        countries = edf['CountryName'].unique()
        series = edf['IndicatorName'].unique()
        year = edf['variable'].unique()

        with st.expander("Select Attributes and countries"):
            selectState = st.multiselect('Select Countries', countries)
            series_data = st.multiselect("Attributes: ", series)
            selectyear = st.selectbox("Select a year",  year)
        country_d = edf['CountryName'].isin(selectState) & edf['IndicatorName'].isin(series_data) & edf.variable.isin([selectyear])
        tree_df = edf[country_d]


        if(len(series_data)>0):
            tree_graph = px.treemap(tree_df, path = ['IndicatorName','CountryName','value'],values='value', color='CountryName')
            st.markdown("**Comparison for** " + str(selectyear))
            st.plotly_chart(tree_graph)
       
    elif compare_button=='Bar Charts':

        edf = pd.melt(df,id_vars=['SeriesName','CountryName'], value_vars=[2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018])
        countries = edf['CountryName'].unique()
        series = edf['SeriesName'].unique()
        year = edf['variable'].unique()
        with st.expander("Select Attributes and countries"):
            selBarCountry = st.multiselect('Select Countries: ', countries)
            selBarSeries = st.selectbox('Select Attributes: ', series)
        barComp = edf['CountryName'].isin(selBarCountry) & edf['SeriesName'].isin([selBarSeries])
        bar_df = edf[barComp]
        lineChart=alt.Chart(bar_df).mark_bar(opacity=0.7, width = 25.5).encode(
        x='variable',
            y=alt.Y('value', stack = None),
            color='CountryName',
        ).properties(
            width=800,
            height=300)
        if(len(selBarCountry)>0):

            st.markdown('      _ compare countries and attributes from 2005 to 2018_')
            st.write(lineChart)

      

    elif compare_button=='Scatter Plots':
   
        edf = pd.melt(df,id_vars=['SeriesName','CountryName'], value_vars=[2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018])
        countries = edf['CountryName'].unique()
        series = edf['SeriesName'].unique()
        year = edf['variable'].unique()
        with st.expander("Select Attributes and countries"):
            scatterCountry = st.multiselect(' Select Countries: ', countries)
            scatterAttribute = st.selectbox('What do you want to see? ', series)

        if(len(scatterCountry)>0):
            scatterData = edf['CountryName'].isin(scatterCountry) & edf['SeriesName'].isin([scatterAttribute]) 
            scatterChart = edf[scatterData]

            fig = px.scatter(scatterChart, x="variable", y="value", color="CountryName",
                            hover_data=['value'])
            st.write(fig)
        
    


    




 
    

    
