import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Load the AFL data from CSV
data = pd.read_csv("football_data.csv")
useful_cols = ["Venue", "Team", "Won", "Round"]
for col in data.columns:
    if col not in useful_cols:
        data.drop([col], axis=1, inplace=True)
# Encode categorical variables
label_encoders = {}
for column in useful_cols:
    label_encoders[column] = LabelEncoder()
    data[column] = label_encoders[column].fit_transform(data[column])

# Split data into features and target
X = data.drop(["Won"], axis=1)
y = data["Won"]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize and train the logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


# Predict the winner of AFL games
def predict_winner(venue, team, round):
    venue_encoded = label_encoders["Venue"].transform([venue])[0]
    team_encoded = label_encoders["Team"].transform([team])[0]
    # opponent_encoded = label_encoders["Opponent"].transform([opponent])[0]
    round_encoded = label_encoders["Round"].transform([round])[0]
    prediction = model.predict(
        [[venue_encoded, team_encoded, round_encoded]]
    )
    return prediction
    if prediction[0] == 1:
        return team
    else:
        return opponent


# Test the model's accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model Accuracy:", accuracy)

# Example usage
venue = "Carrara"
team = "Richmond"
round = 1
predicted_winner = predict_winner(venue, team, round)
print("Predicted Winner:", predicted_winner[0])
