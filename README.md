# DEPLOYMENT_PROJET_GETAROUND

## Description

When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.

In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.

## Goals

This project aims to build a online Dashboard with data analysis to understand how long the minimum delay should be and what is the scope of the features (only connect cars, connect and mobile,...). 

A second part of this project will be a machine learning model that will predict the price for car owners. It will be stored and accessible via an API.

## Dataset

To complete this project, we have two datasets:

1. "get_around_delay_analysis.xlsx": This file presents a number of rentals and the delay at check-out.

2. "get_around_pricing_project.csv": This file presents prices based on car characteristics and host reception.

## Content

This project is contains 

1. Streamlit Dashboard that shows some analysis about the right trade-off to adopt.

2. Notebook "PROJET_GETAROUND.ipynb" that contains some analysis of the pricing dataset and displays some machine learning model testing.

3. Mlflow directory that contains a tool to build a Heroku app and the script to train the model.

4. API files that provide files to build and test the API.

## Usage

To utilize and explore this project, follow these steps:

* Streamlit Dashboard
    
    follow this link 'https://projet-getaround-streamlit-607fb7f2782d.herokuapp.com/'


* Machine learning models : 

    1. **Clone the Repository:**

    git clone https://github.com/Simoncld8/DEPLOYMENT_PROJECT_GETAROUND.git

    2. Select directory 02_Machine_leraning_models

    3. **Install Dependencies:**

    pip install -r requirements.txt  

    4. **Run the Analysis:**

    You will find the analysis in the Jupyter Notebook provided (`PROJET_GETAROUND.ipynb`).


* API 
    follow this link 'https://project-getaround-api-5156ee192f6a.herokuapp.com/'

    For exemple of request, you can :

    1. **Clone the Repository:**

    git clone https://github.com/Simoncld8/DEPLOYMENT_PROJECT_GETAROUND.git

    2. **Run test_api.py**

    This files is in the API directory. 


Contributors

Simon Claude

This project was undertaken as part of the "Data Science and Engineering Fullstack" program offered by Jedha. Its aim was to fulfill a component of the "Machine Learning Engineer" certification.