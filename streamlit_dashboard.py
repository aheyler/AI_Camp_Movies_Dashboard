import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import statsmodels
#[theme]
#base="dark"

st.title("Analyzing Movies")
st.image("https://s3-us-west-2.amazonaws.com/prd-rteditorial/wp-content/uploads/2018/03/13153742/RT_300EssentialMovies_700X250.jpg","Source:Rotten Tomatoes")
st.caption("In this dashboard, we investigate movies––their ratings, revenues, genres, streaming platforms, and directors. We were curious to see how these attributes changed over time as well as how they relate to one another. The following graphs illustrate our key findings. ")

#mcol1, mcol2, mcol3, mcol4 = st.columns(4)
mcol1, mcol2 = st.columns(2)
mcol1.metric("Movies Collected","1000")
mcol2.metric("Directors Analyzed","401")
mcol3, mcol4 = st.columns(2)
mcol3.metric("Genres Categorized","6")
mcol4.metric("Streaming Platforms Sorted","4")

st.caption("Data Sources:")
link = '[IMDB Data](https://www.kaggle.com/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows)'
st.markdown(link, unsafe_allow_html=True)
link = '[Best-Selling Movies](https://www.kaggle.com/mathurinache/bestsellingmoviesofalltime)'
st.markdown(link, unsafe_allow_html=True)
link = '[Movies on Netflix, Prime Video, Hulu and Disney+](https://www.kaggle.com/ruchi798/movies-on-netflix-prime-video-hulu-and-disney)'
st.markdown(link, unsafe_allow_html=True)

st.header("Movie Directors")
movie_df = pd.read_csv("imdb_top_1000.csv")
movie_df.dropna(inplace=True)
movie_df ["Runtime"] = movie_df["Runtime"].apply(lambda x: pd.to_numeric(x.replace("min",""),errors='coerce'))
movie_df["Gross_Rev"] = movie_df["Gross"].apply(lambda x: pd.to_numeric(str(x).replace(",", ""), errors='coerce')) # create new Gross column with integer revenues

#First Graph of Movie Directors
# function for creating a new dataset with director information of their movies, average revenue, and ratings
def director_stats_df(movie_df):
    directors = movie_df.Director.unique()
    director_stats = pd.DataFrame(index=directors,columns=['rating','Avg Domestic Revenue','Number of Movies Made'])
    for director in directors:
        director_stats.loc[director,'rating']=movie_df[movie_df.Director==director]['IMDB_Rating'].mean()
        director_stats.loc[director,'Number of Movies Made']=len(movie_df[movie_df.Director==director])
        director_stats.loc[director,'Avg Domestic Revenue']=movie_df[movie_df.Director==director]['Gross_Rev'].mean()
        director_stats.sort_index(inplace = True) 
    return director_stats
director_stats=director_stats_df(movie_df)  
director_stats = director_stats.reset_index(level=0)
director_stats.rename({'index': 'director'}, axis=1, inplace=True)
director_stats['rating']=director_stats["rating"].apply(lambda x: int(x))
figd = px.scatter(director_stats, x='Number of Movies Made', y='Avg Domestic Revenue',
                 hover_data=['director'],size='rating',
                 title= 'Which directors are most successful?')
figd.update_layout(autosize=False,width=800,height=600,)
figd.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
st.plotly_chart(figd,use_container_width=False)
st.caption("From the data above, it is evident that Steven Spielberg has directed the most movies that are on the top 1000 IMDB List (exlcuding movies with no recorded revenue). The director who has the highest average revenue from movies in the top 1000 is Anthony Russo with a 551.3 million dollar average. The majority of movie directors have made 3 or less films and have an average revenue lower than 500 million. There is no trend of a higher average revenue with more movies. In fact, directors with fewer movies in the top 1000 have a higher average revenue. ")


# Year-based graphs
st.header("Movies Through the Ages")
option = st.selectbox("Select a Movie Variable to See Over the Years", ["Runtime (movie duration)", "Ratings"])

if option=="Runtime (movie duration)": 
    #Second Graph of Runtime vs year
    def runtime_stats_df(movie_df):
        years=movie_df.Released_Year.unique()
        runtime_stats=pd.DataFrame(index=years,columns=['runtime','rating'])
        for year in years:
            runtime_stats.loc[year,'rating']=movie_df[movie_df.Released_Year==year]['IMDB_Rating'].mean()
            runtime_stats.loc[year,'runtime']=movie_df[movie_df.Released_Year==year]['Runtime'].mean()

            runtime_stats.sort_index(inplace = True)
        return runtime_stats
    runtime_stats=runtime_stats_df(movie_df)
    runtime_stats = runtime_stats.reset_index(level=0)
    runtime_stats.rename({'index': 'year'}, axis=1, inplace=True)
    runtime_stats['year']=runtime_stats["year"].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    figr = px.scatter(runtime_stats, x='year', y='runtime',
                     trendline="ols", trendline_scope = 'overall',
                     title= 'Runtime by the Years')
    st.plotly_chart(figr)
    st.caption("Overall, there is a trend in the increasing runtime of movies over the years. With an exception to films made in the 1960s, movies have been getting longer from 1920 to 2020. Movies used to last around 1 hour, but now they provide around 2 hours of content for the world to consume. The varying runtime of movies has gotton narrower as the years progressed. Starting from a wide range of runtimes in the 1940s to a standard runtime of around 2 hours in 2020. ")
elif option=="Ratings":
    #Ratings over the years
    movie_years = movie_df
    movie_years.drop(movie_years.index[movie_years['Released_Year'] == 'PG'], inplace = True)
    movie_years['Year']=movie_df['Released_Year'].apply(lambda x: int(x))
    movie_years.sort_values('Year',inplace=True)
    figrm = px.scatter(movie_years, x="Year", y="IMDB_Rating", hover_data = ["Series_Title"], title="Ratings Over Time")
    st.plotly_chart(figrm)
    st.caption("There is no definitive trend between movie ratings over the years. As the world progresses, more movies are made each year, allowing there to be a variety of ratings. Since more movies are being made, there is a greater number of movies past 1970 with a rating of 8.8 or higher. However, from 2010-2020 there were no movies with a rating of an 8.8 or higher")


#movie Rating graphs
st.header("Movie Ratings")
rating_options=st.selectbox("Select a movie Variable to compare its correlation to movie ratings: ",["Runtime","Votes","Revenue"])
if rating_options=="Runtime":
    # Movie Ratings vs. Movie Length Scatter Plot
    figRL = px.scatter(movie_df, x="IMDB_Rating", y="Runtime", hover_data = ["Series_Title"], title ="Movie Ratings In Respect To Movie Length")
    st.plotly_chart(figRL)
    st.caption("The data shows that movies longer than 2 hours have ratings above 8.6, except for '12 Angry Men'. The bulk of the data shows no distinct correlation between movie length and rating, but it can be interpretted that longer movies outliers are rated higher. ")
elif rating_options=="Votes":
    # Movie ratings vs Votes
    figRV = px.scatter(movie_df, x="IMDB_Rating", y="No_of_Votes",hover_data=["Series_Title"], title="IMDB Ratings and Votes")
    st.plotly_chart(figRV)
    st.caption("The number of votes that a movie received increased as the rating went up. ")
elif rating_options=="Revenue":
    #movie ratings vs revenue
    figRR = px.scatter(movie_df, x="IMDB_Rating", y="Gross_Rev", hover_data = ["Series_Title"], size ='IMDB_Rating', title= "Rating and Revenue Comparison")
    st.plotly_chart(figRR)
    st.caption("Most movies that are rated above an 8.5 earn less than 400 million dollars. The correlation between ratings and revenue shows that a movie does not have to be highly rated to earn a high revenue. ")


# Nathan & Emilio
st.header("Movie Genres")
def create_rating_df(): 
    rating_df = pd.read_csv("imdb_top_1000.csv")
    rating_df = rating_df.dropna()
    rating_df.drop(columns = ['Poster_Link', 'Released_Year', 'Certificate', 'Overview', 'Star1', 'Star2', 'Star3', 'Star4', 'No_of_Votes'], inplace = True)
    rating_df["Gross"] = rating_df["Gross"].apply(lambda gross: gross.replace(",", ""))
    rating_df["Runtime"] = rating_df["Runtime"].apply(lambda runtime : runtime.replace("min", ""))
    rating_df["Runtime"] = rating_df["Runtime"].apply(lambda runtime : int(runtime))
    rating_df["Gross"] = rating_df["Gross"].apply(lambda gross : int(gross))
    rating_list = rating_df.Genre.unique()
    rating_df["Genre"] = rating_df["Genre"].apply(lambda genre : genre.replace(",", ""))
    rating_df["Drama"] = rating_df["Genre"].apply(lambda x: 1 if "Drama" in x else None)
    rating_df["Romance"] = rating_df["Genre"].apply(lambda x: 1 if "Romance" in x else None)
    rating_df["Comedy"] = rating_df["Genre"].apply(lambda x: 1 if "Comedy" in x else None)
    rating_df["Action"] = rating_df["Genre"].apply(lambda x: 1 if "Action" in x else None)
    rating_df["Sci-Fi"] = rating_df["Genre"].apply(lambda x: 1 if "Sci-Fi" in x else None)
    rating_df["Thriller"] = rating_df["Genre"].apply(lambda x: 1 if "Thriller" in x else None)
    return rating_df

rating_df = create_rating_df()

def create_maingenre_df(): 
    maingenre_df = pd.read_csv("imdb_top_1000.csv")
    maingenre_df = maingenre_df.dropna()
    maingenre_df.drop(columns = ['Poster_Link', 'Released_Year', 'Certificate', 'Runtime', 'Overview', 'Director', 'Star1', 'Star2', 'Star3', 'Star4', 'No_of_Votes'], inplace = True)

    maingenre_df["Drama"] = maingenre_df["Genre"].apply(lambda x: 1 if "Drama" in x else None)
    maingenre_df["Romance"] = maingenre_df["Genre"].apply(lambda x: 1 if "Romance" in x else None)
    maingenre_df["Comedy"] = maingenre_df["Genre"].apply(lambda x: 1 if "Comedy" in x else None)
    maingenre_df["Action"] = maingenre_df["Genre"].apply(lambda x: 1 if "Action" in x else None)
    maingenre_df["Sci-Fi"] = maingenre_df["Genre"].apply(lambda x: 1 if "Sci-Fi" in x else None)
    maingenre_df["Thriller"] = maingenre_df["Genre"].apply(lambda x: 1 if "Thriller" in x else None)
    maingenre_df["Gross"] = rating_df["Gross"].apply(lambda gross: str(gross).replace(",", ""))
    maingenre_df["Gross"] = rating_df["Gross"].apply(lambda gross : int(gross))
    maingenre_df = maingenre_df.dropna(thresh= 6)
    maingenre_df = maingenre_df.fillna(0)
    return maingenre_df
maingenre_df = create_maingenre_df()

#lists for box/whiskers
def create_genre_df():
    counts_per_genre = {"Drama": sum(maingenre_df["Drama"]), "Comedy": sum(maingenre_df["Comedy"]),"Romance": sum(maingenre_df["Romance"]), "Action": sum(maingenre_df["Action"]), "Sci-Fi": sum(maingenre_df["Sci-Fi"]), "Thriller": sum(maingenre_df["Thriller"])}
    genre_df = maingenre_df.from_dict(counts_per_genre, orient = 'index', columns=['number_of_movies'])
    avg_per_genre = [77.54,77.53, 80.22, 73.21, 78.24, 75.83 ]
    min_per_genre = [28, 41, 45, 30, 30, 30 ]
    max_per_genre = [100, 99, 100, 98, 98, 97]
    twentyfive_per_genre = [70, 70, 72, 64, 73, 69.5]
    fifty_per_genre = [79, 80.5, 83, 75, 80, 77]
    seventyfive_per_genre = [87, 87, 89, 83, 89, 85]
    realmin_per_genre = [44.5, 44.5, 46.5, 43.5, 55.5, 46.25]
    genre_df["Meta_score_avg"] = avg_per_genre
    genre_df["Meta_score_min"] = min_per_genre
    genre_df["Meta_score_max"] = max_per_genre
    genre_df["Meta_score_twentyfive"] = twentyfive_per_genre
    genre_df["Meta_score_fifty"] = fifty_per_genre
    genre_df["Meta_score_seventyfive"] = seventyfive_per_genre 
    genre_df["Meta_score_realmin"] = realmin_per_genre
    return genre_df

genre_df = create_genre_df()
rows = genre_df.index

fig = px.bar(genre_df, x=rows, y="number_of_movies", color = rows, title="Distribution of Genres Across the Top 700 Movies")
st.plotly_chart(fig)

fig = px.pie(genre_df, values="number_of_movies", names=rows, title="Distribution of Genres Across the Top 700 Movies")
st.plotly_chart(fig)

st.caption("This pie chart shows the number of movies across different genres among the top 700 movies. The drama genre seems to be the most popular among the top 1000 IMDB movies.")

fig = px.scatter(rating_df, x="IMDB_Rating", y="Gross", color="Drama", hover_data = ["Series_Title"])
st.plotly_chart(fig)
st.caption("This scatter plot shows the relationship between a movie's IMDB rating and Gross income. The colors of the plots show if the movie was in the drama genre. It seems that the drama movies are more likely to have higher IMDB rating.")

rows = genre_df.index
fig = px.box(genre_df, x=rows, y=['Meta_score_min',"Meta_score_max", "Meta_score_twentyfive", "Meta_score_fifty", "Meta_score_seventyfive", "Meta_score_realmin"], title="Distribution of Meta Score", color = rows)
st.plotly_chart(fig)

st.caption("Box and Whisker plot describing the range of ratings across multiple movie genres. The figure shows that the Romance genre is most consistently highest rated on the Meta Score platform.")


# Alina & Saul
st.header("Streaming Platforms")
df = pd.read_csv("MoviesOnStreamingPlatforms.csv")
df["Rotten Tomatoes"] = df["Rotten Tomatoes"].apply(lambda x: pd.to_numeric(str(x).replace("/100", ""), errors="coerce"))

sum_of_platforms = {"Netflix": sum(df["Netflix"]), "Disney+": sum(df["Disney+"]), "Hulu": sum(df["Hulu"]), "Prime Video": sum(df["Prime Video"])}
platforms_df = df.from_dict(sum_of_platforms, orient = "index", columns=["movie amount"])
streams = platforms_df.index

fig = px.bar(platforms_df, x=streams, y="movie amount", color=streams, color_discrete_map = {"Netflix": 'red', "Disney+" : 'mediumblue', "Hulu" : 'lawngreen', "Prime Video": 'lightskyblue'}, title = "Movie Availability in Streaming Platforms") 
st.plotly_chart(fig)
st.caption("The bar graph displays information collected from Netflix, Disney+, Hulu, and Prime Video, which was then organized into a bar graph comparing the amounts of movies on the different streaming services showing that the service with the most movies is Prime Video with 4,113 movies, followed closely by Netflix with 3,695 , which was then followed by Hulu with 1047 movies, while leaving Disney+ as the streaming service with the least movies in total at 922 movies.")

fig = px.pie(platforms_df, values = "movie amount", names=streams, color=streams, color_discrete_map = {"Netflix": 'orangered', "Disney+" : 'mediumblue', "Hulu" : 'lawngreen', "Prime Video": 'lightskyblue'}, title="Number of Movies in Streaming Platforms")
st.plotly_chart(fig)
st.caption("The pie chart shows an overview of the amount of movies held by each streaming platform. Prime Video contains the most movies, with Disney+ having the least, as it's a relatively new streaming platform.") 

# figure out how to move radio button below graph without having 'define error'
platform_selected = st.radio("Select a streaming platform:", ["Prime Video", "Disney+", "Hulu", "Netflix"])

fig = px.scatter(df, x="Age", y="Rotten Tomatoes", 
                 color = platform_selected,
                 title = "Which Age Group Has The BEST Movies",
                 category_orders={"Age": ["7+", "13+", "16+", "18+", "all"]}) 
st.plotly_chart(fig)
st.caption("The graph displays the target age group demographic versus the rotten tomatoes rating. From the graph, it seems that target age group isn't correlated to higher or lower rotten tomato ratings.") 


if platform_selected=="Prime Video":
     st.caption("Prime Video contains 4,113 movies, the highest out of the selected streaming platforms. Most of their target audience are located in the '18+' category.")
elif platform_selected=="Netflix": 
     st.caption("Netflix holds the second largest amount of movies, where they have 3,695 movies. From the graph, their movies have consistently high rotten tomato ratings.") 
elif platform_selected=="Hulu":
     st.caption("Hulu does not appear substantially enough on the scatterplot graph for conclusions to be drawn about their age ratings with rotten tomatoes. They have 1,047 movies, placing them at third for total movies contained.") 
elif platform_selected=="Disney+": 
     st.caption("Disney+ holds the least amount of movies, only adding up to 922, with the majority of their movies being aimed at children. They fill up the '7+' and 'all' age categories.")

        
# CONCLUSION- don't forget to add to this :)
st.header("Key Takeaways")
st.caption("**Directors:** Looking at directors of top 1000 movies, Steven Spielberg has directed the most movies, while Anthony Russo has the highest average IMDB ratings for his movies. ")
st.caption("**Trends over time:** Over time, movie durations have grown more similar, and ratings haven't changed significantly.")
st.caption("**Genres:** From our IMDB data, we were able to see that movies from the drama genre are most popular in the list of the top 700 movies. However, romance has a higher median Meta Score out of the movies in this list, while drama has the highest deviation of scores.")
st.caption("**Renues & ratings:** For the correlation of revenue to IMDB rating, we found that there is no correlation rating and gross income.")
st.caption("**Streaming platforms:** In conclusion our data shows that Prime Video hosts the most top movies, followed by Netflix. We also found that movie streaming services can cater to specific audiences based on their age group. For example, Disney+ has most of the movies in the all and 7+ category, while Prime Video has most of the movies in the 18+ section. Another note-worthy takeaway is that Rotten Tomatoe ratings do not have any clear correlations to audience age group.")
