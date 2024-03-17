import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import json

with open("2023_data.json", "r") as fn:
    data = json.load(fn)
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load your data
# Assuming your data is stored in a variable named 'data'
# Adjust this code according to how your data is loaded

# Initialize lists to store processed data
team1_list = []
team2_list = []
venue_list = []
winner_list = []

# Iterate through the data
for year_data in data:
    for game_data in year_data['data']:
        for round_num, round_data in game_data.items():
            for game in round_data:
                team1_name = game['teams'][0]['name']
                team2_name = game['teams'][1]['name']
                venue = game['venue']
                winner = team1_name if game['teams'][0]['won'] else team2_name
                
                # Append data to lists
                team1_list.append(team1_name)
                team2_list.append(team2_name)
                venue_list.append(venue)
                winner_list.append(winner)

# Create DataFrame from lists
df = pd.DataFrame({
    'Team1': team1_list,
    'Team2': team2_list,
    'Venue': venue_list,
    'Winner': winner_list
})

# Label encode categorical variables
label_encoders = {}
for column in ['Team1', 'Team2', 'Venue']:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

# Display the preprocessed DataFrame
print(df.head())


# Prepare features and target variable
X = df[['Team1', 'Team2', 'Venue']]
# Assuming 'Winner' column indicates the winning team
y = (df['Winner'] == df['Team1']).astype(int)

# Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from keras.layers import Dense, Embedding, Flatten


# Build the neural network
model = Sequential([
    Embedding(input_dim=3, output_dim=10),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')

# Label encode categorical variables
label_encoders = {}
for column in ['Team1', 'Team2', 'Venue']:
    label_encoders[column] = LabelEncoder()
    df[column] = label_encoders[column].fit_transform(df[column])

# Save label encodings for later use during prediction
label_encodings = {}
for column in ['Team1', 'Team2', 'Venue']:
    label_encodings[column] = dict(zip(label_encoders[column].classes_, label_encoders[column].transform(label_encoders[column].classes_)))

# Display the preprocessed DataFrame
print(df.head())


# Function to prepare input data and make predictions
def predict_winner(team1_name, team2_name, venue_name, model, label_encodings):
    # Ensure venue name is in label encodings
    venue_encoding = label_encodings['Venue'].get(venue_name)
    if venue_encoding is None:
        print(f"Venue '{venue_name}' not found in label encodings.")
        return None
    
    # Encode team names and venue name
    team1_encoded = label_encodings['Team1'].get(team1_name)
    team2_encoded = label_encodings['Team2'].get(team2_name)
    if team1_encoded is None or team2_encoded is None:
        print("One or both of the team names not found in label encodings.")
        return None
    
    # Prepare input features
    input_features = np.array([[team1_encoded, team2_encoded, venue_encoding]])
    
    # Make prediction
    prediction = model.predict(input_features)
    
    # Decode prediction to get the winning team
    predicted_winner_encoded = np.round(prediction).astype(int)
    predicted_winner = label_encoders['Team1'].inverse_transform(predicted_winner_encoded)[0]
    
    return predicted_winner

# Example usage
team1_name = 'Sydney'
team2_name = 'Melbourne'
venue_name = 'S.C.G.'

# Assuming 'model' is your trained neural network model
# Assuming 'label_encodings' is a dictionary containing label encodings for each categorical variable
predicted_winner = predict_winner(team1_name, team2_name, venue_name, model, label_encodings)
print("Predicted winner:", predicted_winner)
