# IMDB RATING PREDICTOR
## BACKGROUND
As a person studying computer science and someone with a big sense of curiosity, machine learning has always interested me. In an effort to learn more of the basics of `machine learning`, learn the libraries and technologies involved, and showcase my profficency with `Python`, I created this program which uses a random forrest regressor and an IMDb meta dataset to predict the rating of a show or movie based on its duration, number of votes, and nominations

## OVERVIEW
This project utilizes the following:
- `PANDAS` for reading and processing the dataset
- `NumPy` for handling data
- `Sci-kit Learn` for predicting rating scores and measuring error
- A minutizer function of my own design to convert media duration to a standard integer unit
- A vote converter function of my own design to convert votes from shortened string notation to a full length integer
- `Matplotlib` to plot the results

## RATINGS
The main function first uses `pandas` to read a CSV file containing the meta data from IMDb. The data is then cleaned to handle null values and to only include the relevent variables. 
###
```python
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
```
First, the minutizer function is used to convert the durations from "_h _m" format to an integer containing the length of the media in minutes. Then the vote converter function is used to convert the votes from shortened string notation to a full length integer.
###
```python
#convert duration
media["Duration"] = media["Duration"].apply(minutizer)

#convert votes
media["Votes"] = media["Votes"].apply(vote_converter)
```
The data is then parsed into 80% training data and 20% testing data. This split was chosen due to it being standard practice
###
```python
#parse data into training data and testing data
train = media[media["Year"] < 2015].copy()
test = media[media["Year"] >= 2015].copy()
```
We then initalize the random forrest model from Sci-kit Learn, train it, and test it.
```python
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
```
Finally we calculate the mean error, print it, print the testing data, and plot the results using `matplotlib`
```python
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
```

## MINUTIZER
In order for the ratings program to use the duration data, we must convert the duration from "_h _m" format to minutes as an integer. We can do so as follows:
###
```python
import re

def minutizer(time_str):
    # Use regex to extract hours and minutes (both optional)
    match = re.match(r"(?:(\d+)\s*h)?\s*(?:(\d+)\s*m)?", str(time_str))
    
    # Extract hours and minutes, default to 0 if not present
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    
    # Convert to total minutes
    total_minutes = hours * 60 + minutes
    return total_minutes

```
the regular expression used makes the hours and the minutes optional in order to correctly operate on arguments that only contain one or the other.

## VOTE CONVERTER
In order for the ratings program to use the voting data, we must convert the votes from a shortened string "__K, __M votes" to a full length integer. We can do so as follows:
###
```python
def vote_converter(vote):
    if "K" in vote:
        vote = vote.replace("K", "")
        return float(vote) * 1000
    
    elif "M" in vote:
        vote = vote.replace("M", "")
        return float(vote) * 1000000
    
    else:
        return float(vote)
```

## CONCLUSION
After running this program on the dataset I retrieved, I was returned a test data set with an average error of +-0.85 rating points, and a graph showing actual vs predicted ratings
![Figure_1](https://github.com/user-attachments/assets/605f3568-1660-4b9d-acef-72267940f7d2)

Though this program and was not of the highest performance, it a great way to learn and solidify my knowledge of python, machine learning, Sci-kit Learn, and the technologies/libraries involved in the process.
