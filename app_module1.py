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


matplotlib.use("agg")

_lock = RendererAgg.lock


sns.set_style("darkgrid")
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

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

st.markdown("""
    # Outputs
""")

col1, col2, col3 = st.columns(3)
col1.metric("Size", df[df['building_id'] == selected_building_id]['square_feet'], 'sqft')
col2.metric("Year built", df[df['building_id'] == selected_building_id]['year_built'].values[0])
col3.metric("Primary use", df[df['building_id'] == selected_building_id]['primary_use'].values[0])

col1, col2 = st.columns(2)
col1.metric("Energy consumption", "$437.8", "-$1.25")
col2.metric("Energy efficiency", "$121.10", "0.46%")

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
