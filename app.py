from flask import Flask, request , jsonify , render_template , flash , session , redirect
import pickle
import numpy as np
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
app.secret_key = '1232'
model=pickle.load(open('model.pkl','rb'))


client = MongoClient('mongodb+srv://nirjaykumargupta:FzXyb8IMbUn0aDU2@cluster0.paxkl7q.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['user_db']
users = db['users']


@app.route('/')
def home():
    return render_template('login.html')
    

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        login_user = users.find_one({'username': request.form['username']})

        if login_user:
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), login_user['password']):
                session['username'] = request.form['username']
                return render_template('main.html')
        
        flash('Incorrect Username or Password')
        return render_template('login.html')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Only start this when there is POST call otherwise simply return signup.html
    # POST call will be made by signup form submission Form
    if request.method == 'POST':
        existing_user = users.find_one({'username': request.form['username']})
        if existing_user:
            flash('Username already exists')
        else:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'username': request.form['username'], 'password': hashed_password})
            flash('Account created successfully')
            return render_template('login.html')
    return render_template('signup.html')    


@app.route('/profile', methods=['GET', 'POST'])
def profile():
        username = session['username']  
        password = "*********"
        return render_template('profile.html', username=username , password=password)


@app.route('/logout' , methods=['POST'])
def logout():
    session.pop('username', None)
    flash('Logged Out successfully')
    return render_template('login.html')  


@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/about')
def about():
    return render_template('about.html') 


@app.route('/bmi')
def bmi():
    return render_template('bmi.html')               
 

@app.route('/predict',methods=['POST','GET'])
def predict():
    paramete = [str(x) for x in request.form.values()]

    symptoms=['itching', 'skin_rash', 'nodal_skin_eruptions',
       'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
       'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting',
       'vomiting', 'burning_micturition', 'spotting_ urination',
       'fatigue', 'weight_gain', 'anxiety', 'cold_hands_and_feets',
       'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
       'patches_in_throat', 'irregular_sugar_level', 'cough',
       'high_fever', 'sunken_eyes', 'breathlessness', 'sweating',
       'dehydration', 'indigestion', 'headache', 'yellowish_skin',
       'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes',
       'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea',
       'mild_fever', 'yellow_urine', 'yellowing_of_eyes',
       'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
       'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision',
       'phlegm', 'throat_irritation', 'redness_of_eyes', 'sinus_pressure',
       'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
       'fast_heart_rate', 'pain_during_bowel_movements',
       'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus',
       'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity',
       'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes',
       'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties',
       'excessive_hunger', 'extra_marital_contacts',
       'drying_and_tingling_lips', 'slurred_speech', 'knee_pain',
       'hip_joint_pain', 'muscle_weakness', 'stiff_neck',
       'swelling_joints', 'movement_stiffness', 'spinning_movements',
       'loss_of_balance', 'unsteadiness', 'weakness_of_one_body_side',
       'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
       'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching',
       'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain',
       'altered_sensorium', 'red_spots_over_body', 'belly_pain',
       'abnormal_menstruation', 'dischromic _patches',
       'watering_from_eyes', 'increased_appetite', 'polyuria',
       'family_history', 'mucoid_sputum', 'rusty_sputum',
       'lack_of_concentration', 'visual_disturbances',
       'receiving_blood_transfusion', 'receiving_unsterile_injections',
       'coma', 'stomach_bleeding', 'distention_of_abdomen',
       'history_of_alcohol_consumption', 'fluid_overload.1',
       'blood_in_sputum', 'prominent_veins_on_calf', 'palpitations',
       'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring',
       'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails',
       'inflammatory_nails', 'blister', 'red_sore_around_nose',
       'yellow_crust_ooze']
    
    disease=['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis',
       'Drug Reaction', 'Peptic ulcer diseae', 'AIDS', 'Diabetes ',
       'Gastroenteritis', 'Bronchial Asthma', 'Hypertension ', 'Migraine',
       'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice',
       'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'hepatitis A',
       'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E',
       'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia',
       'Dimorphic hemmorhoids(piles)', 'Heart attack', 'Varicose veins',
       'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia',
       'Osteoarthristis', 'Arthritis',
       '(vertigo) Paroymsal  Positional Vertigo', 'Acne',
       'Urinary tract infection', 'Psoriasis', 'Impetigo']
    

    input_data = np.zeros(len(symptoms))

    input_data = np.zeros(len(symptoms))

    for i, symptom in enumerate(symptoms):
        if symptom in paramete:
            input_data[i] = 1
        else:
            input_data[i] = 0

    input_data_reshaped = input_data.reshape(1, -1)

    prediction_index = int(model.predict(input_data_reshaped))
    if 0 <= prediction_index < len(disease):
        predicted_disease = disease[prediction_index]
        prediction_text = f'{predicted_disease}'
    else:
        prediction_text = "Unable to determine the predicted disease."
    return render_template('main.html',prediction_text=prediction_text)

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'username' in session:
        if 'old_password' in request.form and 'new_password' in request.form:
            old_password = request.form['old_password']
            new_password = request.form['new_password']

            user = users.find_one({'username': session['username']})
            if user and bcrypt.checkpw(old_password.encode('utf-8'), user['password']):
                new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
                users.update_one({'_id': user['_id']}, {'$set': {'password': new_hashed_password}})
                flash('Password changed successfully')
                return render_template('main.html')
            else:
                flash('Incorrect old password')
        else:
            flash(' ')
    else:
        flash('Session expired. Please log in again.')
        return  render_template('login.html')
    return  render_template('change_password.html')


if __name__ == "__main__":
    app.run()




    







     

