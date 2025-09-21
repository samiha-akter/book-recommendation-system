from http.server import BaseHTTPRequestHandler
import json
import pickle
import numpy as np
import os

# Load models - use absolute paths
def load_models():
    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        models_path = os.path.join(current_dir, '../models')
        
        popular_df = pickle.load(open(os.path.join(models_path, 'popular.pkl'), 'rb'))
        pt = pickle.load(open(os.path.join(models_path, 'pt.pkl'), 'rb'))
        similarity_scores = pickle.load(open(os.path.join(models_path, 'similarity_scores.pkl'), 'rb'))
        books = pickle.load(open(os.path.join(models_path, 'books.pkl'), 'rb'))
        
        return popular_df, pt, similarity_scores, books
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None, None, None

popular_df, pt, similarity_scores, books = load_models()

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Serve the recommendation form
        with open(os.path.join(os.path.dirname(__file__), '../templates/recommend.html'), 'r') as f:
            html_content = f.read()
        
        self.wfile.write(html_content.encode())
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        params = json.loads(post_data)
        user_input = params.get('user_input', '')
        
        response_data = {}
        
        if pt is None:
            # Demo mode
            response_data = {
                "data": [
                    ["The Silent Echo", "Elizabeth Morgan", "https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80"],
                    ["Beyond the Horizon", "Michael Reeves", "https://images.unsplash.com/photo-1536746803623-cef87080c7b2?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80"],
                    ["Whispers of the Past", "Sarah Johnson", "https://images.unsplash.com/photo-1512820790803-83ca734da794?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80"]
                ],
                "search_query": user_input
            }
        else:
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
                
                response_data = {
                    "data": data,
                    "search_query": user_input
                }
                
            except IndexError:
                response_data = {
                    "error": "Book not found in our database. Please try another title.",
                    "search_query": user_input
                }
            except Exception as e:
                response_data = {
                    "error": "An error occurred. Please try again.",
                    "search_query": user_input
                }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())
        return