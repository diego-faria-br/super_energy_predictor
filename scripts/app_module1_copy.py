###########################################################################################################
###########################################################################################################
###########################################################################################################
######## Le Wagon batch #1011
######## authors = Alexandre Chartier, Ana Gama, Diego Faria
######## version = 1.0
######## status = WIP
######## deployed at = https://share.streamlit.io/tdenzl/bulian/main/BuLiAn.py
######## layout inspired by https://share.streamlit.io/tylerjrichards/streamlit_goodreads_app/books.py
###########################################################################################################
###########################################################################################################
###########################################################################################################

import urllib.request

import matplotlib
import numpy as np
import pandas as pd
import requests
import seaborn as sns
import streamlit as st
#import xmltodict
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.figure import Figure
from pandas import json_normalize
from PIL import Image
from streamlit_lottie import st_lottie

st.set_page_config(page_title="Super Energy Predictor", layout="wide")


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_book = load_lottieurl("https://assets4.lottiefiles.com/temp/lf20_aKAfIn.json")
st_lottie(lottie_book, speed=1, height=200, key="initial")

### Data Import ###

matplotlib.use("agg")

_lock = RendererAgg.lock

### Helper Methods ###

########################
### ANALYSIS METHODS ###
########################

sns.set_style("darkgrid")
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

####################
### INTRODUCTION ###
####################

row0_1.title("Super Energy Predictor")

with row0_2:
    st.write("")

row0_2.subheader(
    "A Streamlit web app by [Alexandre Chartier](https://github.com/opxal89), [Ana Gama](https://github.com/anaflaviagama) and [Diego Faria](https://github.com/diego-faria-br/)"
)


row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

with row1_1:
    st.markdown(
        "Climate has been changing in plain sight. And unfortunately, extreme weather events from heat waves, floods, forest fires have become an everyday reality of our lives."
    )
    st.markdown(
        "**Then, what can you do to effectively switch this path?**"
    )
    st.markdown(
        "**We created Super Energy Predictor to help companies to develop strategies considering energy consumption and efficiency when choosing their new buildings.**"
    )


#################
### MODULE 1 ###
#################

### Inputs ###

columns = st.columns(3)

site_name = 'University of Central Florida, Orlando, FL'

df = pd.read_csv('super_energy_predictor/data/building_selection.csv')
site_name = columns[0].selectbox(
        "Select a site", df['site_name'].unique())

site_id = df[df['site_name'] == site_name]['site_id'].values[0]

def building_selection(df):
    keys = df['site_name'].unique()
    response = {}
    for key in keys:
        building_list = df[df['site_name'] == key]['building_id'].to_list()
        response[key] = building_list
    return response

dict_building = building_selection(df)

selected_building_id = columns[1].selectbox("Select a building", dict_building[site_name])

meter = columns[2].selectbox(
        "Select a a meter",
        ('Electricity',
         'Chilled water',
         'Steam',
         'Hot water'
         ))

if meter == 'Electricity':
    meter_num = 0
if meter == 'Chilled water':
    meter_num = 1
if meter == 'Steam':
    meter_num = 2
if meter == 'Hot water':
    meter_num = 3


import datetime

columns = st.columns(2)

start_date = columns[0].date_input(
    "Select a start date",
    datetime.date(2019, 7, 1))

end_date = columns[1].date_input(
    "Select an end date",
    datetime.date(2019, 7, 1))

### Outputs ###

st.markdown("""
    # Outputs
""")

if site_name == 'University of Central Florida, Orlando, FL':
    columns = st.columns(2)
    st.image("""data:image/jpeg;base64,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""")
    st.markdown('**University of Central Florida, Orlando, FL**')

# st.image('super_energy_predictor/images/image_0.png')

col1, col2, col3 = st.columns(3)
col1.metric("Size", str(df[df['building_id'] == selected_building_id]['square_feet'].values[0]) + ' sqft')
col2.metric("Year built", int(df[df['building_id'] == selected_building_id]['year_built'].values[0]))
col3.metric("Primary use", df[df['building_id'] == selected_building_id]['primary_use'].values[0])

col1, col2 = st.columns(2)
col1.metric("Energy consumption", "$437.8", "-$1.25")
col2.metric("Energy efficiency", "$121.10", "0.46%")



#################
### MODULE 2 ###
#################

### Inputs ###

st.markdown("""
    # Energy alternatives
""")


url = 'http://127.0.0.1:8000/refit'


building_id = st.number_input('Building ID',step=1,format=f'%i',min_value=0,max_value=9999)
meter = st.number_input('Meter',step=1,format=f'%i',min_value=0,max_value=4)


# Limit dates to the available horizon

min_date = datetime.datetime(2017, 1, 1)
max_date = datetime.datetime(2018, 12, 31)
value_date = datetime.datetime(2017, 1, 1)


initial_date = st.date_input("Initial Date",value=value_date, min_value=min_date,max_value=max_date)
initial_date = str(initial_date)
final_date = st.date_input("Final date",value=value_date, min_value=min_date,max_value=max_date)
final_date = str(final_date)

primary_use = st.number_input('New Primary Use',format=f'%i',min_value=0,max_value=16)
size_change = st.number_input('Proportion size change',step =.1, format=f'%.1f')

freq =  st.selectbox("Frequency", ['Hourly','Daily',"Monthly"])

accu = st.checkbox("Accumulates over the period")

ty = freq=='Daily'

ty

params = {'building_id':building_id,
          'meter':meter,
          'initial_date':initial_date,
          'final_date':final_date,
          'primary_use':primary_use,
          'size_change':size_change
          }

### Outputs ###

response = requests.get(url=url,params=params)

y_json = response.json()
y_recovered = pd.read_json(y_json)


if freq == 'Daily':
    y_recovered = y_recovered.resample('D').mean()

if freq == 'Monthly':
    y_recovered = y_recovered.resample('M').mean()

if accu:
    graph = ps.line(y_recovered.cumsum())
else:
    graph = ps.line(y_recovered)

st.plotly_chart(graph)





@st.cache
def get_user_data(
    user_id, key="ZRnySx6awjQuExO9tKEJXw", v="2", shelf="read", per_page="200"
):
    api_url_base = "https://www.goodreads.com/review/list/"
    final_url = (
        api_url_base
        + user_id
        + ".xml?key="
        + key
        + "&v="
        + v
        + "&shelf="
        + shelf
        + "&per_page="
        + per_page
    )
    contents = urllib.request.urlopen(final_url).read()
    return contents


user_input = str(user_input)
contents = get_user_data(user_id=user_id, v="2", shelf="read", per_page="200")
contents = xmltodict.parse(contents)

line1_spacer1, line1_1, line1_spacer2 = st.columns((0.1, 3.2, 0.1))

with line1_1:
    if int(contents["GoodreadsResponse"]["reviews"]["@total"]) == 0:
        st.write(
            "Looks like you did not read any books on Goodreads. Add some books to your profile or try a different profile"
        )
        st.stop()

    st.header("Analyzing the Reading History of: **{}**".format(user_name))

df = json_normalize(contents["GoodreadsResponse"]["reviews"]["review"])
u_books = len(df["book.id.#text"].unique())
u_authors = len(df["book.authors.author.id"].unique())
df["read_at_year"] = [i[-4:] if i != None else i for i in df["read_at"]]
has_records = any(df["read_at_year"])

st.write("")
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)


with row3_1, _lock:
    st.subheader("Books Read")
    if has_records:
        year_df = pd.DataFrame(df["read_at_year"].dropna().value_counts()).reset_index()
        year_df = year_df.sort_values(by="index")
        fig = Figure()
        ax = fig.subplots()
        sns.barplot(
            x=year_df["index"], y=year_df["read_at_year"], color="goldenrod", ax=ax
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Books Read")
        st.pyplot(fig)
    else:
        st.markdown("We do not have information to find out _when_ you read your books")

    st.markdown(
        "It looks like you've read a grand total of **{} books with {} authors,** with {} being your most read author! That's awesome. Here's what your reading habits look like since you've started using Goodreads.".format(
            u_books, u_authors, df["book.authors.author.name"].mode()[0]
        )
    )


with row3_2, _lock:
    st.subheader("Book Age")
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(
        pd.to_numeric(df["book.publication_year"], errors="coerce")
        .dropna()
        .astype(np.int64),
        kde_kws={"clip": (0.0, 2020)},
        ax=ax,
        kde=True,
    )
    ax.set_xlabel("Book Publication Year")
    ax.set_ylabel("Density")
    st.pyplot(fig)

    avg_book_year = str(int(np.mean(pd.to_numeric(df["book.publication_year"]))))
    row_young = df.sort_values(by="book.publication_year", ascending=False).head(1)
    youngest_book = row_young["book.title_without_series"].iloc[0]
    row_old = df.sort_values(by="book.publication_year").head(1)
    oldest_book = row_old["book.title_without_series"].iloc[0]

    st.markdown(
        "Looks like the average publication date is around **{}**, with your oldest book being **{}** and your youngest being **{}**.".format(
            avg_book_year, oldest_book, youngest_book
        )
    )
    st.markdown(
        "Note that the publication date on Goodreads is the **last** publication date, so the data is altered for any book that has been republished by a publisher."
    )

st.write("")
row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row4_1, _lock:
    st.subheader("How Do You Rate Your Reads?")
    rating_df = pd.DataFrame(
        pd.to_numeric(
            df[df["rating"].isin(["1", "2", "3", "4", "5"])]["rating"]
        ).value_counts(normalize=True)
    ).reset_index()
    fig = Figure()
    ax = fig.subplots()
    sns.barplot(x=rating_df["index"], y=rating_df["rating"], color="goldenrod", ax=ax)
    ax.set_ylabel("Percentage")
    ax.set_xlabel("Your Book Ratings")
    st.pyplot(fig)

    df["rating_diff"] = pd.to_numeric(df["book.average_rating"]) - pd.to_numeric(
        df[df["rating"].isin(["1", "2", "3", "4", "5"])]["rating"]
    )

    difference = np.mean(df["rating_diff"].dropna())
    row_diff = df[abs(df["rating_diff"]) == abs(df["rating_diff"]).max()]
    title_diff = row_diff["book.title_without_series"].iloc[0]
    rating_diff = row_diff["rating"].iloc[0]
    pop_rating_diff = row_diff["book.average_rating"].iloc[0]

    if difference > 0:
        st.markdown(
            "It looks like on average you rate books **lower** than the average Goodreads user, **by about {} points**. You differed from the crowd most on the book {} where you rated the book {} stars while the general readership rated the book {}".format(
                abs(round(difference, 3)), title_diff, rating_diff, pop_rating_diff
            )
        )
    else:
        st.markdown(
            "It looks like on average you rate books **higher** than the average Goodreads user, **by about {} points**. You differed from the crowd most on the book {} where you rated the book {} stars while the general readership rated the book {}".format(
                abs(round(difference, 3)), title_diff, rating_diff, pop_rating_diff
            )
        )

with row4_2, _lock:
    st.subheader("How do Goodreads Users Rate Your Reads?")
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(
        pd.to_numeric(df["book.average_rating"], errors="coerce").dropna(),
        kde_kws={"clip": (0.0, 5.0)},
        ax=ax,
        kde=True,
    )
    ax.set_xlabel("Goodreads Book Ratings")
    ax.set_ylabel("Density")
    st.pyplot(fig)
    st.markdown(
        "Here is the distribution of average rating by other Goodreads users for the books that you've read. Note that this is a distribution of averages, which explains the lack of extreme values!"
    )

st.write("")
row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row5_1, _lock:
    # page breakdown
    st.subheader("Book Length Distribution")
    fig = Figure()
    ax = fig.subplots()
    sns.histplot(pd.to_numeric(df["book.num_pages"].dropna()), ax=ax, kde=True)
    ax.set_xlabel("Number of Pages")
    ax.set_ylabel("Density")
    st.pyplot(fig)

    book_len_avg = round(np.mean(pd.to_numeric(df["book.num_pages"].dropna())))
    book_len_max = pd.to_numeric(df["book.num_pages"]).max()
    row_long = df[pd.to_numeric(df["book.num_pages"]) == book_len_max]
    longest_book = row_long["book.title_without_series"].iloc[0]

    st.markdown(
        "Your average book length is **{} pages**, and your longest book read is **{} at {} pages!**.".format(
            book_len_avg, longest_book, int(book_len_max)
        )
    )


with row5_2, _lock:
    # length of time until completion
    st.subheader("How Quickly Do You Read?")
    if has_records:
        df["days_to_complete"] = (
            pd.to_datetime(df["read_at"]) - pd.to_datetime(df["started_at"])
        ).dt.days
        fig = Figure()
        ax = fig.subplots()
        sns.histplot(pd.to_numeric(df["days_to_complete"].dropna()), ax=ax, kde=True)
        ax.set_xlabel("Days")
        ax.set_ylabel("Density")
        st.pyplot(fig)
        days_to_complete = pd.to_numeric(df["days_to_complete"].dropna())
        time_len_avg = 0
        if len(days_to_complete):
            time_len_avg = round(np.mean(days_to_complete))
        st.markdown(
            "On average, it takes you **{} days** between you putting on Goodreads that you're reading a title, and you getting through it! Now let's move on to a gender breakdown of your authors.".format(
                time_len_avg
            )
        )
    else:
        st.markdown(
            "We do not have information to find out _when_ you finished reading your books"
        )


st.write("")
row6_space1, row6_1, row6_space2, row6_2, row6_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)


with row6_1, _lock:
    st.subheader("Gender Breakdown")
    # gender algo
    d = gender.Detector()
    new = df["book.authors.author.name"].str.split(" ", n=1, expand=True)

    df["first_name"] = new[0]
    df["author_gender"] = df["first_name"].apply(d.get_gender)
    df.loc[df["author_gender"] == "mostly_male", "author_gender"] = "male"
    df.loc[df["author_gender"] == "mostly_female", "author_gender"] = "female"

    author_gender_df = pd.DataFrame(
        df["author_gender"].value_counts(normalize=True)
    ).reset_index()
    fig = Figure()
    ax = fig.subplots()
    sns.barplot(
        x=author_gender_df["index"],
        y=author_gender_df["author_gender"],
        color="goldenrod",
        ax=ax,
    )
    ax.set_ylabel("Percentage")
    ax.set_xlabel("Gender")
    st.pyplot(fig)
    st.markdown(
        "To get the gender breakdown of the books you have read, this next bit takes the first name of the authors and uses that to predict their gender. These algorithms are far from perfect, and tend to miss non-Western/non-English genders often so take this graph with a grain of salt."
    )
    st.markdown(
        "Note: the package I'm using for this prediction outputs 'andy', which stands for androgenous, whenever multiple genders are nearly equally likely (at some threshold of confidence). It is not, sadly, a prediction of a new gender called andy."
    )

with row6_2, _lock:
    st.subheader("Gender Distribution Over Time")

    if has_records:
        year_author_df = pd.DataFrame(
            df.groupby(["read_at_year"])["author_gender"].value_counts(normalize=True)
        )
        year_author_df.columns = ["Percentage"]
        year_author_df.reset_index(inplace=True)
        year_author_df = year_author_df[year_author_df["read_at_year"] != ""]
        fig = Figure()
        ax = fig.subplots()
        sns.lineplot(
            x=year_author_df["read_at_year"],
            y=year_author_df["Percentage"],
            hue=year_author_df["author_gender"],
            ax=ax,
        )
        ax.set_xlabel("Year")
        ax.set_ylabel("Percentage")
        st.pyplot(fig)
        st.markdown(
            "Here you can see the gender distribution over time to see how your reading habits may have changed."
        )
    else:
        st.markdown("We do not have information to find out _when_ you read your books")
    st.markdown(
        "Want to read more books written by women? [Here](https://www.penguin.co.uk/articles/2019/mar/best-books-by-female-authors.html) is a great list from Penguin that should be a good start (I'm trying to do better at this myself!)."
    )

st.write("")
row7_spacer1, row7_1, row7_spacer2 = st.columns((0.1, 3.2, 0.1))

with row7_1:
    st.header("**Book List Recommendation for {}**".format(user_name))

    reco_df = pd.read_csv("recommendations_df.csv")
    unique_list_books = df["book.title"].unique()
    reco_df["did_user_read"] = reco_df["goodreads_title"].isin(unique_list_books)
    most_in_common = (
        pd.DataFrame(reco_df.groupby("recommender_name").sum())
        .reset_index()
        .sort_values(by="did_user_read", ascending=False)
        .iloc[0][0]
    )
    avg_in_common = (
        pd.DataFrame(reco_df.groupby("recommender_name").mean())
        .reset_index()
        .sort_values(by="did_user_read", ascending=False)
        .iloc[0][0]
    )
    most_recommended = reco_df[reco_df["recommender_name"] == most_in_common][
        "recommender"
    ].iloc[0]
    avg_recommended = reco_df[reco_df["recommender_name"] == avg_in_common][
        "recommender"
    ].iloc[0]

    def get_link(recommended):
        if "-" not in recommended:
            link = "https://bookschatter.com/books/" + recommended
        elif "-" in recommended:
            link = "https://www.mostrecommendedbooks.com/" + recommended + "-books"
        return link

    st.markdown(
        "For one last bit of analysis, we scraped a few hundred book lists from famous thinkers in technology, media, and government (everyone from Barack and Michelle Obama to Keith Rabois and Naval Ravikant). We took your list of books read and tried to recommend one of their lists to book through based on information we gleaned from your list"
    )
    st.markdown(
        "You read the most books in common with **{}**, and your book list is the most similar on average to **{}**. Find their book lists [here]({}) and [here]({}) respectively.".format(
            most_in_common,
            avg_in_common,
            get_link(most_recommended),
            get_link(avg_recommended),
        )
    )

    st.markdown("***")
    st.markdown(
        "Thanks for going through this mini-analysis with me! I'd love feedback on this, so if you want to reach out you can find me on [twitter] (https://twitter.com/tylerjrichards) or my [website](http://www.tylerjrichards.com/)."
    )
# API INFO #

#url =
params = {'site_id': site_id, 'building_id': selected_building_id, 'meter': meter_num, 'start_date': start_date, 'end_date': end_date}
response = requests.get(url,data=params)
