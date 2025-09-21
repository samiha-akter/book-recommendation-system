from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os

# Load your data
try:
    popular_df = pickle.load(open('popular.pkl','rb'))
    pt = pickle.load(open('pt.pkl','rb'))
    similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
    books = pickle.load(open('books.pkl','rb'))
except:
    # Create dummy data for demonstration if files not found
    popular_df = None
    pt = None
    similarity_scores = None
    books = None

app = Flask(__name__)

@app.route('/')
def index():
    if popular_df is None:
        return render_template('index.html',
                           book_name=["Demo Book 1", "Demo Book 2", "Demo Book 3"],
                           author=["Author 1", "Author 2", "Author 3"],
                           image=["https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80", 
                                  "https://images.unsplash.com/photo-1536746803623-cef87080c7b2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80",
                                  "https://images.unsplash.com/photo-1512820790803-83ca734da794?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80"],
                           votes=[100, 200, 300],
                           rating=[4.5, 4.2, 4.7]
                           )
    
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    
    if pt is None:
        # Demo mode - return sample recommendations
        data = [
            ["The Silent Echo", "Elizabeth Morgan", "https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80"],
            ["Beyond the Horizon", "Michael Reeves", "https://images.unsplash.com/photo-1536746803623-cef87080c7b2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80"],
            ["Whispers of the Past", "Sarah Johnson", "https://images.unsplash.com/photo-1512820790803-83ca734da794?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80"]
        ]
        return render_template('recommend.html', data=data, search_query=user_input)
    
    try:
        # Find the index of the book
        index = np.where(pt.index == user_input)[0][0]
        
        # Get similar items
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
        
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            
            data.append(item)
        
        return render_template('recommend.html', data=data, search_query=user_input)
    
    except IndexError:
        # Book not found in the dataset
        return render_template('recommend.html', error="Book not found in our database. Please try another title.", search_query=user_input)
    except Exception as e:
        # Other errors
        return render_template('recommend.html', error="An error occurred. Please try again.", search_query=user_input)

# This is required for Vercel to recognize the app
if __name__ == '__main__':
    app.run(debug=True)