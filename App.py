from flask import Flask, render_template, request
import pickle
import numpy as np

# Load data from pickle files
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Initialize Flask app
app = Flask(__name__)

@app.route('/')
def index():
    # Ensure all required columns are present
    if {'Book-Title', 'Book-Author', 'Image-URL-M', 'num_ratings', 'avg_rating'}.issubset(popular_df.columns):
        return render_template(
            'index.html',
            book_name=list(popular_df['Book-Title'].values),
            author=list(popular_df['Book-Author'].values),
            image=list(popular_df['Image-URL-M'].values),
            votes=list(popular_df['num_ratings'].values),
            rating=list(popular_df['avg_rating'].values),
        )
    else:
        return "Data columns are missing in the dataset. Please verify your pickle files.", 500


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    if user_input not in pt.index:
        return render_template('recommend.html', data=None, message="Book not found in the dataset!")

    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return render_template('recommend.html', data=data, message=None)


if __name__ == '__main__':
    app.run(debug=True)
