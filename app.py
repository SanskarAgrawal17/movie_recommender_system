

from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests

# Create a Flask web application
app = Flask(__name__)

def fetch(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a23a2f8cdf94b96195532ec2446f259a'.format(movie_id))
    data=response.json()
    return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"

# Load the movie data and similarity matrix from the pickle files
movie_vlu = pickle.load(open('movies1.pkl', 'rb'))
movie = pd.DataFrame(movie_vlu)
# movie = movie.sort_values( by='title',ascending=True)

similarity = pickle.load(open('similarity.pkl', 'rb'))


@app.route('/', methods=['POST', 'GET'])
def recommend():
    return render_template('index.html')

# Define a route for the root URL
@app.route('/MovieRecommendedModel', methods=['POST', 'GET'])
def recommend1():
    if request.method == 'POST':

        moviee = str(request.form['genre'])

        movie_index = movie[movie['title'] == moviee].index[0]
        distance = similarity[movie_index]

        movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
        recomended_poster=[]
        recommend_mv = []
        for i in movie_list:
            movie_id=movie.iloc[i[0]].id
            recommend_mv.append(movie.iloc[i[0]].title)
            #Fetch Poster Form Api
            recomended_poster.append(fetch(movie_id))

        return render_template('r_system.html', vlu=recommend_mv,hlo=recomended_poster,random=1)


    else:
        return render_template('r_system.html', result=movie['title'],random=0)


# Run the web application
if __name__ == '__main__':
    app.run(debug=True)

