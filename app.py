# load packages

import flask
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

app = flask.Flask(__name__, template_folder='templates')

data = pd.read_csv("music_df.csv")

# to generate the count matrix
count = CountVectorizer()
count_matrix = count.fit_transform(data['text'])

# to generate the cosine similarity matrix (size 250 x 250)
# rows represent all movies; columns represent all movies
# cosine similarity: similarity = cos(angle) = range from 0 (different) to 1 (similar)
# all the numbers on the diagonal are 1 because every movie is identical to itself (cosine value is 1 means exactly identical)
# matrix is also symmetrical because the similarity between A and B is the same as the similarity between B and A.
# for other values eg 0.1578947, movie x and movie y has similarity value of 0.1578947

cosine_sim = cosine_similarity(count_matrix, count_matrix)

# to create a Series for record titles which can be used as indices (each index is mapped to a movie title)
indices = pd.Series(data['side_a'])

# this function takes in a movie title as input and returns the top 10 recommended (similar) titles

def recommend(side_a, cosine_sim = cosine_sim):
    recommended_record = []
    genre_a = []
    genre_b = []
    label = []

    idx = indices[indices == side_a].index[0]   # to get the index of the song title matching the input song

    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)   # similarity scores in descending order

    top_10_indices = list(score_series.iloc[1:11].index)   # to get the indices of top 10 most similar movies
    # [1:11] to exclude 0 (index 0 is the input movie itself)

    for i in top_10_indices:   # to append the titles of top 10 similar movies to the recommended_movies list
        recommended_record.append(list(data['Title'])[i])

    for i in top_10_indices:   # to append the titles of top 10 similar movies to the recommended_movies list
        genre_a.append(list(data['Catalyst Music Genre Side A'])[i])

    for i in top_10_indices:   # to append the titles of top 10 similar movies to the recommended_movies list
        genre_b.append(list(data['Catalyst Music Genre Side B'])[i])

    for i in top_10_indices:   # to append the titles of top 10 similar movies to the recommended_movies list
        label.append(list(data['Label Name'])[i])

    return recommended_record, genre_a, genre_b, label


# Set up the main route
@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return(flask.render_template('home.html'))

    if flask.request.method == 'POST':
        s_name = flask.request.form['song_name']
#        check = difflib.get_close_matches(m_name,all_titles,cutout=0.50,n=1)
        if s_name not in list(indices):
            return(flask.render_template('error.html'))
        else:
            recommended_record, genre_a, genre_b, label = recommend(s_name)

            return flask.render_template('result.html',song_names=recommended_record,a=genre_a,b = genre_b, label = label, search_name=s_name)

if __name__ == '__main__':
    app.run()
