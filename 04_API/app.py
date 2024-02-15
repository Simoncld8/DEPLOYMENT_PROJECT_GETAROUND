import mlflow 
import uvicorn
import json
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse


description = """
Getaround Price Prediction API helps you determine the optimal rental price for your car on the Getaround platform. 
With this API, you can accurately estimate the rental value of your vehicle based on various factors such as 
mileage, engine power, fuel type, paint color, car type, availability of private parking, GPS, air conditioning,
automatic transmission, and other features. 
By leveraging machine learning algorithms, the API provides a reliable prediction of the rental price, 
helping you maximize your earnings while ensuring competitive rates for potential renters.

## Machine-Learning 

Where you can:
* `/predict` the price per day of your car 

"""


tags_metadata = [{
        "name": "Predictions",
        "description": "Endpoints that uses our Machine Learning model for detecting attrition"
    }
]

app = FastAPI(
    title="👨‍💼 Getaround Price Prediction API",
    description=description,
    version="0.1",
    contact={
        "name": "Simon Claude - Project Getaround",
        "url": "https://github.com/Simoncld8/DEPLOYMENT_PROJECT_GETAROUND",
    },
    openapi_tags=tags_metadata
)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")
    

@app.post("/predict", tags=["Machine-Learning"])
async def predict(data: dict):
    
    inputs = data["inputs"]
    input_dicts = []
    for input in inputs:
        input_dict = {
            "model_key": input[0],
            "mileage": input[1],
            "engine_power": input[2],
            "fuel": input[3],
            "paint_color": input[4],
            "car_type": input[5],
            "private_parking_available": input[6],
            "has_gps": input[7],
            "has_air_conditioning": input[8],
            "automatic_car": input[9],
            "has_getaround_connect": input[10],
            "has_speed_regulator": input[11],
            "winter_tires": input[12],
        }

        input_dicts.append(input_dict)


    df = pd.DataFrame(input_dicts)
    df.head()

    numeric_features = []
    categorical_features = []
    for i,t in df.dtypes.items():
        if ('float' in str(t)) or ('int' in str(t)) :
            numeric_features.append(i)
        else :
            categorical_features.append(i)

    # Log model from mlflow 
    logged_model = 's3://project-getaround-bucket/mlflowtracking/1/38dec835e4384daa975da2b7ed4d27ec/artifacts/model_linear_regression'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    prediction = loaded_model.predict(df)

    # Format response
    response = {"prediction": prediction.tolist()}
    return response


if __name__=="__main__":
    uvicorn.run(app, debug=True, reload=True)