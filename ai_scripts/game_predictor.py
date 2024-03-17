import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Embedding, Flatten

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder

# Load data from CSV
def load_data(csv_file):
    df = pd.read_csv(csv_file)
    return df

# Preprocess data
def preprocess_data(df):
    # Drop irrelevant columns
    df.drop(columns=['Year', 'Date', 'Final Score', 'Opponent Final Score', 'Outcome', 'Margin'], inplace=True)
    
    # Encode categorical variables
    label_encoders = {}
    for col in ['Venue', 'Team', 'Opponent']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    
    # Convert boolean Won column to numeric
    df['Won'] = df['Won'].astype(int)
    
    return df, label_encoders

# Define neural network model
def create_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(input_shape,)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Train the model
def train_model(model, X_train, y_train):
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Save model weights
def save_model_weights(model, filename):
    model.save_weights(filename)

# Load model weights
def load_model_weights(model, filename):
    model.load_weights(filename)

# Predict function
def predict_result(model, input_data):
    prediction = model.predict(input_data)
    return prediction

# Predict function with team names, round number, and venue
def predict_result_for_teams(model, team1_name, team2_name, round_number, venue, label_encoders):
    team1_encoded = label_encoders['Team'].transform([team1_name])[0]
    team2_encoded = label_encoders['Team'].transform([team2_name])[0]
    venue_encoded = label_encoders['Venue'].transform([venue])[0]
    
    input_data = np.array([[round_number, venue_encoded, team1_encoded, team2_encoded]])
    
    prediction = predict_result(model, input_data)
    return prediction

def evaluate_model(model, X_test, y_test):
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# Main function
def main():
    # Load and preprocess data
    df = load_data('football_data.csv')
    df, label_encoders = preprocess_data(df)
    
    # Split data into features and target
    X = df.drop(columns=['Won']).values
    y = df['Won'].values
    
    # Split data into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Create and train model
    print(X_train)
    return
    model = create_model(X_train.shape[1])
    train_model(model, X_train, y_train)
    evaluate_model(model, X_test, y_test)
    # Save model weights
    save_model_weights(model, 'model.weights.h5')
    
    # # Load model weights
    # model = create_model(X_train.shape[1])
    # load_model_weights(model, 'model.weights.h5')
    
    # Example input for prediction
    team1_name = "Richmond"
    team2_name = "Carlton"
    round_number = 1
    venue = "M.C.G."
    
    # Make prediction
    prediction = predict_result_for_teams(model, team1_name, team2_name, round_number, venue, label_encoders)
    print(f"Prediction: {prediction}")

if __name__ == "__main__":
    main()
