import nltk
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import pickle

# Download required NLTK data
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Initialize the lemmatizer and define stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Load your pre-trained model and vectorizer from pickle files
with open('./pickle_names/tuned_rf_tf_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('./models/vectorizer.pkl', 'rb') as file:
    vectorizer = pickle.load(file)   

with open('./models/labels.pkl', 'rb') as file:
    label_categories = pickle.load(file)    

def preprocess_text(text):
    # Convert to lower case
    text = text.lower()
    
    # Tokenize the text
    tokens = nltk.word_tokenize(text)
    
    # Remove punctuation and stop words, and lemmatize the tokens
    cleaned_tokens = [
        lemmatizer.lemmatize(token) 
        for token in tokens 
        if token not in string.punctuation and token not in stop_words
    ]
    
    return ' '.join(cleaned_tokens)

def vectorize(clean_data):
    # Transform the cleaned text to TF-IDF representation using the loaded vectorizer
    text_tfidf = vectorizer.transform([clean_data])
    return text_tfidf

def predict(tf_data):
    # Make prediction using the loaded model
    prediction = model.predict(tf_data)
    return label_categories[prediction[0]]

def execute_flow(text):
    clean_texts = preprocess_text(text)
    vectorized_data = vectorize(clean_data=clean_texts)
    return predict(vectorized_data)   