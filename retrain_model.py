import pandas as pd
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten
from sklearn.model_selection import train_test_split


projects = pd.read_csv('generate_random_data_project.csv')
preferences = pd.read_csv('new_merged_data.csv')

n_project = preferences.project_id.nunique()
n_freelancer = preferences.freelancer_id.nunique()

train, test = train_test_split(preferences, test_size=0.2)

EMBEDDING_DIM = 27

#input layer
project_input = Input(shape=1)
freelancer_input = Input(shape=1)

#embedding layer
project_embedding = Embedding(n_project+1, EMBEDDING_DIM)(project_input)
freelancer_embedding = Embedding(n_freelancer+1, EMBEDDING_DIM)(freelancer_input)

#flatten layer
project_flat = Flatten()(project_embedding)
freelancer_flat = Flatten()(freelancer_embedding)

#output layer
output = Dot(1)([project_flat, freelancer_flat])

model = Model([project_input, freelancer_input],[output])

model.compile(optimizer='adam', loss='mse')

model.fit(x=[train.project_id, train.freelancer_id], y=[train.preference_freelancer],
         epochs=30, batch_size=128)

# model.evaluate(x=[test.project_id, test.freelancer_id], y=[test.preference_freelancer])

model.save('recommender_model_tes.h5')