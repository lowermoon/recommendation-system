import pandas as pd
import numpy as np
import tensorflow as tf
from flask import Flask, request, jsonify
from keras.models import load_model
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten
from sklearn.model_selection import train_test_split
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def connect_to_sql():
    try:
        conn = psycopg2.connect(
            host=os.environ.get("CLOUD_SQL_HOST"),
            database=os.environ.get("CLOUD_SQL_DATABASE"),
            user=os.environ.get("CLOUD_SQL_USERNAME"),
            password= '@Vi{2~:]f;Kvi`9a'
        )
        cur = conn.cursor()
        print("Connected to database")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn = None
    return conn

def get_projects_from_db(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(projects, columns=['project_id', 'project_name', 'project_desc', 'user_id', 'deadline', 'project_category', 'imgUrl'])

app = Flask(__name__)

model = load_model('recommender_model.h5')
# projects = pd.read_csv('generate_random_data_project.csv')
conn = connect_to_sql()
projects = get_projects_from_db(conn)



# def get_recommendations(id_freelancer, projects, model):
#     try:
#         projects = projects.copy()
#         id_freelancers = np.array([id_freelancer] * len(projects))
#         results = model([projects.id_project.values, id_freelancers]).numpy().reshape(-1)

#         projects['predicted_rating'] = pd.Series(results)
#         projects = projects.sort_values('predicted_rating', ascending=False)

#         print(f'Recommendations for user {id_freelancer}')
#         return projects
#     except tf.errors.InvalidArgumentError:
#         print(f'User {id_freelancer} not found. Returning random recommendations.')
#         # Menggunakan np.random.randint untuk mendapatkan nilai random_state yang berbeda setiap kali dijalankan
#         random_state = np.random.randint(1, 100)
#         projects = projects.sample(n=10, random_state=random_state)
#         return projects


@app.route('/', methods=['GET'])
def connect():
    return jsonify('Connected to server!')

# @app.route('/get_recommendations', methods=['GET'])
# def recommendations():
#     rekomendasi = get_recommendations(19, projects, model)
#     rekomendasi_dict = rekomendasi.to_dict(orient='index')
#     return jsonify(rekomendasi_dict)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))