#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Name : Alia Amr | Track : Data Management | Mail : aliaamr2110@gmail.com


# ### Problem Description

# The data science team in your company was working on a machine learning model that can help doctors in diagnosing diabetes. Then, the deployment team decided that the model itself (given in `model.h5` file) will be on server side so you have to provide the following:

# - A scoring script that uses the h5 file to predict the outcome of each patient.
# - The given file `pima-indians-diabetes.data.csv` should be injected to the database under the name of **diabetes_unscored**
# - Your script must listen to the database and take the newly added records in **diabetes_unscored**, run the model on them, and put them back in a new table **diabetes_scored**.
# - Your script should be a scheduled task that will run every hour.

# So, the deployment team will be able to inject data in a table and retrieve the prediction output from the other table.

# In[7]:


import h5py as h5
import numpy as np
import pandas as pd
import sqlalchemy as db
connection = db.create_engine('postgresql://aliaamr:123@localhost:5432/aa_task_3')
print('process started.')
print('process is running .....')


# In[8]:


diabetes_batch = """
SELECT *
FROM public."DIABETES_UNSCORED"
EXCEPT  
SELECT 
Pregnancies,
Glucose,
BloodPressure,
SkinThickness,
Insulin,
BMI,
DiabetesPedigreeFunction,
Age
FROM public."DIABETES_SCORED";
"""

batch = pd.read_sql(diabetes_batch, con=connection)


# In[9]:


import json
import pandas as pd
from keras.models import model_from_json

file = open('/home/aliaamr/Documents/Material/data/model.json', 'r')
json_model = file.read()
file.close()


# In[10]:


loaded_model = model_from_json(json_model)
loaded_model.load_weights('data/model.h5')


# In[11]:


unscored_data = pd.DataFrame(batch)
unscored_data = unscored_data .iloc[:,:].values
unscored_data_array = np.array(unscored_data)
predictions = loaded_model.predict(unscored_data_array)


# In[12]:


batch.head(10)


# In[9]:


print(batch)


# In[6]:


prediction_results = []
for n in predictions :
    if n > 0.5:
        r = 1
    else:
        r = 0
    prediction_results.append(r)


# In[7]:


batch['score'] = prediction_results


# In[8]:


batch.to_sql(name = 'DIABETES_SCORED', con = connection,
             schema = 'public', index = False, if_exists = 'append')


# In[9]:


print(len(batch['score']) , " row(s) of scored diabetes uploaded.")

