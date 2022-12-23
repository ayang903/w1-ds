#importing general objects
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title('Video Game Sales Analysis')
st.write('Using a dataset from Kaggle, we made graphs and charts of Video game sales.')
st.write('this is a test')

df = pd.read_csv('vgsales.csv')
#cleaning nulls
df.isna().sum()
df.dropna(inplace=True)

# df = df.rename(columns={'NA_Sales': 'NA Sales (Millions)', 'EU_Sales': 'EU Sales (Millions)', 'JP_Sales': 'JP Sales (Millions)', 'Other_Sales': 'Other Sales (Millions)', 'Global_Sales': 'Global Sales (Millions)'}, inplace = True)
temp = df.head(25)


#sales histograms
region = st.selectbox('Choose the region', options=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales','Global_Sales'], key=1)
fig = px.histogram(df, x=region, nbins=250)
st.plotly_chart(fig)

##figNA = px.histogram(df, x="NA_Sales", nbins=250)
#t.plotly_chart(figNA)

#igEU = px.histogram(df, x="EU_Sales", nbins=250)
#t.plotly_chart(figEU)

#igJP = px.histogram(df, x="JP_Sales", nbins=250)
#t.plotly_chart(figJP)

#igG = px.histogram(df, x="Global_Sales", nbins=250)
#t.plotly_chart(figG)


#Top 25 most sold games per region

#use st.selectionbox to have the user select a sales region
# generalize the following code, to work with the selected region
# graphing the selected region

region = st.selectbox('Choose your region', options=['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales','Global_Sales'])

# UStemp = temp.sort_values('NA_Sales', ascending=False)
# EUtemp = temp.sort_values('EU_Sales', ascending=False)
# JPtemp = temp.sort_values('JP_Sales', ascending=False)
# Otemp = temp.sort_values('Other_Sales', ascending=False)
# Wtemp = temp.sort_values('Global_Sales', ascending=False)
region_sales = temp.sort_values(region, ascending=False)
#Sorting top 25 games

# #putting them in order
# newtemp2 = UStemp.groupby('Name').mean().sort_values('NA_Sales', ascending=False).head(25)
# EUtemp = EUtemp.copy().groupby('Name').mean().sort_values('EU_Sales', ascending=False)
# JPtemp = JPtemp.groupby('Name').mean().sort_values('JP_Sales', ascending=False)
# Otemp = Otemp.groupby('Name').mean().sort_values('Other_Sales', ascending=False)
# Wtemp = Wtemp.groupby('Name').mean().sort_values('Global_Sales', ascending=False)

regiondf = region_sales.groupby('Name').mean().sort_values(region, ascending=False)

# #Bar charts

fig = px.bar(regiondf, x=regiondf.index, y=region, color=region, height=1000, title=region)
st.plotly_chart(fig)

# NASales = px.bar(newtemp2, x=newtemp2.index, y='NA_Sales', color='NA_Sales', height=1000, title="North American Sales")
# NAstreamlit = st.plotly_chart(NASales)

# EUSales = px.bar(EUtemp, x=EUtemp.index, y='EU_Sales', color='EU_Sales', height=1000, title="European Sales")
# EUstreamlit = st.plotly_chart(EUSales)

# JPSales = px.bar(JPtemp, x=JPtemp.index, y='JP_Sales', color='JP_Sales', height=1000, title="Japan Sales")
# JPstreamlit = st.plotly_chart(JPSales)

# OSales = px.bar(Otemp, x=Otemp.index, y='Other_Sales', color='Other_Sales', height=1000, title="Other Sales")
# Ostreamlit = st.plotly_chart(OSales)

# WSales = px.bar(Wtemp, x=Wtemp.index, y='Global_Sales', color='Global_Sales', height=1000, title="Global Sales")
# Wstreamlit = st.plotly_chart(WSales)

consoles = df.groupby('Platform').count()
fig = px.pie(consoles, values='Global_Sales', names=consoles.index)
st.plotly_chart(fig)


# Popular Platform by global sales
average = df.groupby("Platform").mean()

drop_List = ["Rank", "Year"]
average_sales = average.drop(drop_List, axis = 1, inplace = False)

def total_Sale(average_sales_sorted):
    index = average_sales_sorted.index
    gobal_Sales = average_sales_sorted['Global_Sales']
    NA_Sales = average_sales_sorted['NA_Sales']
    EU_Sales = average_sales_sorted['EU_Sales']
    JP_Sales = average_sales_sorted['JP_Sales']
    Other_Sales = average_sales_sorted['Other_Sales']


    # fig with highest number of 'Global_Sales'
    fig = px.scatter(average_sales_sorted, x = index, y = gobal_Sales, title = 'Platform Sales')

    # adding data in
    fig.add_scatter(x=index, y=gobal_Sales, mode='lines+markers', name = "Gobal Sales")
    fig.add_scatter(x=index, y=NA_Sales, mode='lines+markers', name = "NA Sales")
    fig.add_scatter(x=index, y=EU_Sales, mode='lines+markers', name = "EU Sales")
    fig.add_scatter(x=index, y=JP_Sales, mode='lines+markers', name = "JP Sales")
    fig.add_scatter(x=index, y=Other_Sales, mode='lines+markers', name = "Other Sales")

    #change fig label
    fig.update_layout(xaxis_title = 'Platform', yaxis_title = "Sales (million)")
    return fig

# columns = list[average_sales.columns.tolist()]
# option = st.selectbox('Choose region :', ('Total_Sales', 'NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales'))

fig = total_Sale(average_sales.sort_values('Global_Sales'))
st.plotly_chart(fig)
# fig.show()

# Video game yearly sales (line chart)

yrs_global_sales = df[['Year', 'Global_Sales']]
yrs_grouped = yrs_global_sales.groupby('Year').mean()

yearly_sales = px.line(yrs_grouped, title='Annual Video Game Sales (Global)', labels={'value':'Average Global Sales (Millions)'})

#yearly_sales.show()
st.plotly_chart(yearly_sales)




# Popular genres (bar graph)

# Choosing which columns to use
df[['Genre', 'Rank', 'Global_Sales']].head()

# Grouping & sorting
grouped = df.groupby('Genre').mean()
new_grouped = grouped['Global_Sales']
new_grouped = new_grouped.sort_values(ascending=False)

popular_genres = px.bar(new_grouped, title = 'Popular Video Game Genres Based off Global Sales', labels={'value':'Average Global Sales (Billions)'}, color='value')

# popular_genres.show() 
st.plotly_chart(popular_genres)

listofgenres = ['Platform', 'Shooter', 'Role-Playing', 'Racing']
# listofgenres = st.selectbox("Select Genre:", options=['Platform', 'Shooter', 'Role-Playing', 'Racing'])

# Sales of different genres
fig = make_subplots(rows=2, cols=2, vertical_spacing=0.16)
row=1
col=1


for genre in listofgenres:
    temporary = df[df['Genre'] == genre]

    temporary = temporary.sort_values('Global_Sales', ascending=False).head(11)

    fig.add_trace(
    go.Bar(name=genre, x=temporary.Name, y=temporary['Global_Sales']),
    row=row, col=col)

#     fig = px.bar(temporary.head(11), x='Name', y='Global Sales (Millions)', color="Genre")
    col += 1
    if (col == 3):
        col = 1
        row += 1

fig.update_layout(height=1000, width=1000, title_text="Most Popular Games in the Most Popular Genres")
st.plotly_chart(fig)
# fig.show()



# consoles = df.groupby('Platform').count()
# px.pie(consoles, values='Global_Sales', names=consoles.index)

# px.scatter_matrix(df,
#                   dimensions=['NA_Sales','EU_Sales','JP_Sales','Global_Sales'],
#                   width = 1000,
#                   height = 1000)

st.write('Estefanny - I created different types of charts(Pie, scatter, and histogram) based on diferent Video game sales from paticular places, which are North America, Japan, United Kingdom, globally.  ')

st.write('Hayden - I created a bar chart showcasing the Top 25 most sold games in North America, Europe, Japan, Other Regions and Global sales. I started by sorting games into one of the five regions and the top 25 games for each and creating bar charts for each using Plotly. After creating the charts, I discovered something unique about each region. North America had the only Microsoft game in the top 10, Kinect Adventures for the Xbox 360. In Europe, they are big Wii fans, with 7 of their top 25 all being Wii games. In Japan, 21 of their top 25 were all Nintendo. They also had the most Pokemon games by far, with 3 in the top 10. The "Other Regions" chart was the only one to not have a Nintendo game be first, with GTA San Andreas taking the lead. Globally, Wii Sports (as of 2016) had 84 MILLION sales! That is double the sales of the second place game, Super Mario Bros.')

st.write('Haokang - By Pandas, we create a data frame that allows us to clean the data (removing N/A and dropping unnecessary columns), but we ended up with only sales in the data. Next, using groupby() function gives us data frame sales based on the Platform, using mean() to find the average global sales of each platform, then using the sort_values() function, allows one to sort a particular column from the highest Global sale to the lowest Global sale. To create a scatter plot regularly based on the information, we will need to use Plotly Express and use fig = px.scatter(df, x = x, y = y). In this situation, df is equal to the data frame being sorted, x is equal to the platform, and y is equal to the columns including Global sales. This will give us a visual scatter graph of which platform has the highest Global sale by looking at the platform at the top-right (since we have sorted the data from maximum to minimum). As a result, Game Boy and NES have the highest Global sales.')

st.write('Amanda - Based off my graphs, I can conclude that the top three most popular videogame genres from the past few years are "Platform", "Shooter", and "Role-Playing"- with platform games having the highest average of global sales while adventure, strategy, and puzzle games had significantly lower global sales. Looking at the line chart, you can also see how the popularity of video games in general spiked in the late 1980s, with video games generating about $4 million in sales globally. However, video game sales seem to have dropped significantly after the year 1990- which is quite surprising.')

st.write('Catherine - The top 4 genres from the dataset are Platform, Shooter, Role-Playing, and Racing. The top 3 games in Platform are: Super Mario Bros, New Super Mario Bros, and Super Mario Bros Wii. For Shooter, the games are: Duck Hunt, Call of Duty: Modern Warfare 3, Call of Duty: Black Ops 2. The 3rd game in the top 3 is not Call of Duty: Black Ops because that game made less than Call of Duty: Blacks Ops 2 bbecause COD: Black Ops 2 made more money on the multiple consoles it was released on. In the Role-Play genre, the top 3 are: Pokemon Red/Blue, Pokemon Gold/Silver, Pokemon Diamond/Pearl. Lastly, in Racing, the top 3 are: Mario Kart Wii, Mario Kart DS, and Gran Turismo 3: A-Spec. The top game in the Platform genre made more money than the top games in the other 3 genres. The top 2 games in each genre have a wide gap, however, the top 2 games in the Shooter genre have similar sales. The top genre overall makes more money than the other genres.')





