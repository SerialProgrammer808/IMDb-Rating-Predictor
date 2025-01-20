import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from minutizer import minutizer
from vote_converter import vote_converter

#clean data
media = pd.read_csv("/Users/noahasano/Desktop/IMDb.csv")
media = media[["Year", "Duration", "Rating", "Votes", "nominations"]]
media = media.dropna()

#convert duration
media["Duration"] = media["Duration"].apply(minutizer)

#convert votes
media["Votes"] = media["Votes"].apply(vote_converter)

#parse data into training data and testing data
train = media[media["Year"] < 2015].copy()
test = media[media["Year"] >= 2015].copy()

#initialize random forrest regression model and dependent/independent variables
reg = RandomForestRegressor(n_estimators=100, random_state=42)
predictors = ["Duration", "Votes", "nominations"]
target = "Rating"

#train random forrest regression model by fitting trend between predictors and target
reg.fit(train[predictors], train["Rating"])
#test random forrest regression by predicting the medals on test when only given "athletes" and "prev_medals"
predictions = reg.predict(test[predictors])

#set the "predictions" for data 2015 and on equal to our predictions
test["predictions"] = predictions
#set negative values equal to zero, round, cap predicitons at 10
test.loc[test["predictions"] < 0, "predictions"] = 0
test["predictions"] = test["predictions"].round()
test["predictions"] = np.clip(test["predictions"], 0, 10)

#calculate mean error
error = mean_absolute_error(test["Rating"], test["predictions"])
print(error)
print(test)

# Scatter plot: Actual vs Predicted Rating
plt.figure(figsize=(8, 6))
plt.scatter(test["Rating"], test["predictions"], color='blue', alpha=0.5)

# Add labels and title
plt.xlabel('Actual Ratings')
plt.ylabel('Predicted Ratings')
plt.title('Actual vs Predicted Ratings')

# Add a diagonal line for reference (y = x)
plt.plot([0, 10], [0, 10], color='red', linestyle='--')

# Show plot
plt.show()