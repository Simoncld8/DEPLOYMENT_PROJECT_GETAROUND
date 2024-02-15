import argparse
import pandas as pd
import time
import mlflow
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import  StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import os


if __name__ == "__main__":

    mlflow.set_tracking_uri("your_uri")

    ### MLFLOW Experiment setup
    experiment_name="Price_recommandation"

    mlflow.set_experiment(experiment_name)

    experiment = mlflow.get_experiment_by_name(experiment_name)

    client = mlflow.tracking.MlflowClient()

    run = client.create_run(experiment.experiment_id)

    print("training model...")
    
    # Time execution
    start_time = time.time()

    # Call mlflow autolog
    mlflow.sklearn.autolog(log_models=False)

    # Parse arguments given in shell script

    # Import dataset
    df = pd.read_csv("get_around_pricing_project.csv", index_col=0)

    # Separate target variable Y from features X
    target_variable = "rental_price_per_day"
    X = df.drop(target_variable, axis = 1)
    Y = df.loc[:,target_variable]

    # Train / test split 
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Preprocessing 
    numeric_features = []
    categorical_features = []
    for i,t in X.dtypes.items():
        if ('float' in str(t)) or ('int' in str(t)) :
            numeric_features.append(i)
        else :
            categorical_features.append(i)

    # Standardize numeric features by removing the mean and scaling to unit variance.
    numeric_transformer = StandardScaler()

    # We use OneHotEncoder to create a binary column for each category.
    categorical_transformer = Pipeline(
        steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')), 
        ('encoder', OneHotEncoder(drop='first')) 
        ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])


    model = Pipeline(steps=[
        ("Preprocessing", preprocessor),
        ("Regressor",LinearRegression())
    ], verbose=True)


    # Log experiment to MLFlow
    with mlflow.start_run(run_id = run.info.run_id) as run:
        model.fit(X_train, Y_train)
        predictions = model.predict(X_train)

        # Log model seperately to have more flexibility on setup 
        mlflow.sklearn.log_model(model,"model_linear_regression")
        
    print("...Done!")
    print(f"---Total training time: {time.time()-start_time}")