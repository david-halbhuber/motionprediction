# Used to evaluated the trained model on unknown dataset 


import pandas as pd
import time
from tensorflow.python.keras.models import load_model

# Define your dataset here
df = pd.read_csv(r"UNKNOWN_EVAL_DATASET", header=None)


# Load model here, check if model is loaded correctly by summarizing
model = load_model(r"MODEL_PATH_TO_EVAL")
model.summary()

# Make prediciton and print actual target value
for i in range(1,100):
    start_time = time.time_ns()
    print("Model predicition: ", model.predict(test_input))
    end_time = time.time_ns()
    print(end_time - start_time)
    #print("Actual value: ",df_target.iloc[i-1:i])
    print("______________________________________________________--")
    #print("Model5 predicition: ", model.predict(df.iloc[0:1]))
