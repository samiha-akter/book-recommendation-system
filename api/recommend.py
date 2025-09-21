from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load your data (this would need to be adapted for serverless)
try:
    popular_df = pickle.load(open('popular.pkl','rb'))
    pt = pickle.load(open('pt.pkl','rb'))
    similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
    books = pickle.load(open('books.pkl','rb'))
except:
    popular_df = None
    pt = None
    similarity_scores = None
    books = None

def recommend_books(user_input):
    if pt is None:
        return ["Demo Book 1", "Demo Book 2", "Demo Book 3"]
    
    try:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
        
        data = []
        for i in similar_items:
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            data.append({
                'title': list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)[0],
                'author': list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)[0],
                'image': list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)[0]
            })
        
        return data
    
    except:
        return []

@app.route('/api/recommend', methods=['POST'])
def recommend():
    user_input = request.json.get('book')
    recommendations = recommend_books(user_input)
    return jsonify(recommendations)

# Vercel requires this
if __name__ == '__main__':
    app.run(debug=True)