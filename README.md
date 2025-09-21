# Book Recommendation System

A machine learning-powered book recommendation system built with Flask and Tailwind CSS that suggests books based on user preferences and collaborative filtering.

## Features

- **Top Books Recommendations**: Get book suggestions based on your reading preferences
- **Responsive Design**: Beautiful UI that works on desktop and mobile devices
- **Search Functionality**: Find books by title and get similar recommendations
- **Rating System**: View community ratings for each book

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Data Storage**: Pickle files for model persistence

## Dataset

This project uses the [Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset) from Kaggle. The dataset contains:

- 10,000+ books with metadata
- 1,000,000+ user ratings
- User information and book details

## Machine Learning Model

The recommendation system uses collaborative filtering to suggest books based on user preferences and similarity between books. The model training process includes:

1. Data preprocessing and cleaning
2. User-item matrix creation
3. Similarity calculation using cosine similarity
4. Model evaluation and validation

You can find the complete training code in the Jupyter notebook: [book_recommendation_model.ipynb](./book_recommendation.ipynb)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/samiha-akter/book-recommendation-system.git
cd book-recommendation-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the dataset from Kaggle and place it in the `data/` directory

5. Run the training notebook to generate the model files:
```bash
jupyter notebook notebooks/book_recommendation_model.ipynb
```

6. Start the Flask application:
```bash
python app.py
```

7. Open your browser and navigate to `http://localhost:5000`

## API Endpoints

- `GET /` - Homepage with popular books
- `GET /recommend` - Book recommendation form
- `POST /recommend_books` - Get book recommendations based on user input

## Model Details

The recommendation system uses a collaborative filtering approach:

1. **Data Preprocessing**: Cleaning and transforming the book rating data
2. **Matrix Creation**: Building a user-item matrix of book ratings
3. **Similarity Calculation**: Using cosine similarity to find similar books
4. **Recommendation Generation**: Generating top-N recommendations based on similarity scores

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Dataset provided by [Kaggle Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)
- Icons by [Font Awesome](https://fontawesome.com/)
- Styling with [Tailwind CSS](https://tailwindcss.com/)
- Book images from [Unsplash](https://unsplash.com/)

## Contact

Samiha Akter

Project Link: [Live Link](https://book-recommender-gray-eta.vercel.app/)