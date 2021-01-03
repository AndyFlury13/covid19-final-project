# COVID-19 Exploratory Data Analysis
## Introduction
The total number of COVID-19 cases in the US has recently surpassed 1.4 million, with over 80,000 deaths due to the disease or related complications. Though the world’s foremost institutes are dedicated to researching the virus, we still thought it worth exploring the COVID-19 dataset. Upon some precursory data analysis, we decided to focus our the brunt of our EDA on how COVID-19 affects people of different social status/background. Which social factors are most closely correlated to COVID-19 incidence? If an initial hypothesis that the lower class is more affected by COVID-19 is correct, what are the specific class factors that influence COVID-19 incidence? More specifically, how does SVI (social vulnerability) affect COVID-19 incidence?
Note: In this project we will be mainly examining COVID-19 in the United States, with parts focusing on California.

## Description of Data/EDA
#### I - SVI and COVID
SVI (Social Vulnerability Index) is a measure of the “resilience of communities when confronted by external stresses on human health, stresses such as natural or human-caused disasters, or disease outbreaks.” 
A county’s SVI percentile, given in “abridged_couties.csv”, gives a rough estimate on how vulnerable a county is with respect to the rest of the nation. We merged this into  “county_info_cases.csv” to combine county demographic data with COVID-19 case and death data at a county level. We then selected all California counties, and created a pair of new dataframes with SVI percentile data along with case and death data.
#### Visualizations
The plot_svi_bins() function binned the counties using dataframe methods and then plotted their case and death rates over time, shown below:
![Case Rate over time](markdown_images/case_rate.png)
![Death Rate over time](markdown_images/death_rate.png)
The graphs confirm some basic suspicions: the most socially vulnerable counties suffer the largest impact from COVID-19, and the middle 50% of counties have roughly the same COVID-19 incidence. The one surprising feature of these graphs is how quickly the bottom quartile flatlined in both case and death rates, with there being practically no increase in deaths among these counties since mid-April.
We briefly examined which factors of SVI had the highest correlation with COVID-19 incidence. This examination can be seen in the SVI portion of our notebook.

### II - Correlation Exploration
In addition, we tried to find the specific variables that affect COVID-19 cases/deaths/infections rate. We correlated all appropriate demographic variables (logged and otherwise) with either deaths per capita, cases per capita, or new infections per current infections. Then, we plotted those with the highest correlation. This allowed us to see variables worth exploring more. Here are a subset of the plots with deaths per capita:
![Correlation graphs](markdown_images/correlation.png)
While performing EDA, we discovered some major issues to be aware of. Many values were zeroes, so performing log transformations were difficult. Cases and demographic county data like the number of hospitals was largely in absolute numbers, which required normalization with the population.
#### Methods
**PCA**: To further examine our high dimensional data, we decided to use PCA to identify strong associations in the data. Thus, we performed PCA on the cases by day for counties in California, and plotted each county according to PC1, PC2, and PC3.
![PCA visualization](markdown_images/pca.png)
To see what PC1 and PC2 were associated with, we then identified clusters in the resulting graph and plotted the cases over time for each cluster. We found that the low PC1 cluster tended to have a higher infection per capita, especially around mid April.
#### Results, Discussion, and Difficulties
We would categorize the above methods as a surface level data exploration, as it only looks at potential variables instead of a deep dive. It gives us promising areas of further study, such as a score for minority/language ranking, but also topics that seem to have no useful relation, like longitude. It also shows that the topic is incredibly difficult to study-- not just in the number of variables but also the nature of the disease.
The correlation plots have a couple problems: They assume a linear relationship and generally have rather low correlations. To combat the first issue, we also tried it with different log combinations, but we did not try square root or exponentiating. With so many variables tried, it’s very possible that some are highly correlated due to chance.

### III - Mortality Prediction
Many already-existing models already do an excellent job of predicting and visualizing the future of COVID-19, but we nevertheless explored the short-term future of COVID-19’s mortality rate.
#### Data Cleaning
Though we performed our previous analysis at the county-scale, we found that county data was far too messy to warrant usage of a regression model. The vast majority of counties reported few deaths, and at times the cumulative death statistics (which should be strictly increasing) dropped. To obtain more reliable data, we moved to the state level. There was far less demographic data for states available to us, so our goal was not to directly predict future behavior from demographics; instead, our model predicts future mortality rates based on past mortality and incident rates. We do expect demographic and response information to greatly effect the behavior of the time series, but we treat those features as latent variables embedded within the behavior of the time series. With this in mind, we decided to create a moving-window model that predicts COVID-19’s mortality rate based on a past number of days.

We chose mortality rate as our predictive statistic for a number of reasons. First, we make the assumption that the confounds associated with COVID mortality are less pronounced than those associated with its incidence rate. While mortality rates may vary based on  to be the cases rate per day had a heavy dosage of NaN values, so we ultimately took the path of least resistance and analyzed mortality rate over time. This involved scraping GitHub for the cases information each day (done with the function get_day_cases() in utils.py), filtering based on state, and then selecting features to create a training matrix.
#### Methods
**Linear Regression**: Because we were working at a state scale, we did not have the same access to demographic data as our previous analyses. We decided to take a moving-window approach; calculating the next X days’ mortality rates based off of case and mortality information from the past Y days, using a LinearRegression model from SciKit. The features we ultimately decided to use were the ‘Confirmed’, ‘Deaths’, ‘Active’, ‘Incident_Rate’, and ‘Mortality_Rate’ columns (where ‘Mortality_Rate’ was only used for the past Y days) out of get_day_cases(). We achieved a training RMSE of just over .02 using these features, with our cross-validation RMSE coming out to be just over .033 (both values are available in regression.ipynb).
#### Visualizations
![Mortality Graph Visualization](markdown_images/mortality.png)
For several West coast states, the mortality rate in the short term seems to be decreasing, which reflects where in the curve the west coast is (COVID-19 spread throughout the West Coast sooner than in the Southeast, for example):
![Florida and Alabama mortality rates](markdown_images/florida.png)
In the Southeast, states are still grappling with increasing cases, and our model predicts that mortality rates still increase in this area of the country. 
