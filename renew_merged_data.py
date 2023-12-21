import pandas as pd
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Dot, Flatten
from sklearn.model_selection import train_test_split

data_project = pd.read_csv('generate_random_data_project.csv',names=["project_id", "project_category"])
freelancer_preference = pd.read_csv('new_combined_preferences.csv')

result_data = []

# Loop melalui setiap baris di freelancer_preference
for _, row in freelancer_preference.iterrows():
    freelancer_id = row['freelancer_id']
    
    # Loop melalui setiap kolom kecuali 'freelancer_id'
    for col in freelancer_preference.columns[1:]:
        project_category = col
        preference_freelancer = row[col]
        
        # Filter data_project berdasarkan project_category
        filtered_data_project = data_project[data_project['project_category'] == project_category]
        
        # Loop melalui setiap baris di data_project yang sesuai
        for _, project_row in filtered_data_project.iterrows():
            id_project = project_row['project_id']
            
            # Tambahkan data ke list
            result_data.append({'project_id': project_id, 'freelancer_id': freelancer_id, 'project_category': project_category, 'preference_freelancer': preference_freelancer})

result = pd.DataFrame(result_data)
result.to_csv('new_merged_data.csv', index=False)