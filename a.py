from flask import Flask, render_template, request, session, redirect, jsonify, url_for
import csv
import os
import subprocess
import requests
import mail
import sys

app = Flask(__name__, template_folder='templates')
app.secret_key = "your-secret-key" 

# Fix Unicode encoding issue
sys.stdout.reconfigure(encoding='utf-8')

CSV_FILE = 'use.csv'

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'email', 'password'])


def add_user_to_csv(name, email, password):
    """Adds a new user to the CSV file."""
    with open(CSV_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([name, email, password])


def verify_user(email, password):
    """Verifies if a user exists in the CSV file."""
    with open(CSV_FILE, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            if row and row[1] == email and row[2] == password:
                return True
    return False


# Fetch AQI data using latitude and longitude
def get_aqi(lat, lon):
    IQAIR_API_KEY = "8dadfa53-8d0d-454a-b491-16990aceb29c"
    url = f"http://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={IQAIR_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and "current" in data["data"] and "pollution" in data["data"]["current"]:
            return {
                "aqi": data["data"]["current"]["pollution"]["aqius"],
                "city": data["data"]["city"],
                "state": data["data"]["state"],
                "country": data["data"]["country"],
                "latitude": lat,
                "longitude": lon
            }
    return {"error": "Failed to fetch AQI data"}


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'signupEmail' in request.form:
            name = request.form['signupName']
            email = request.form['signupEmail']
            password = request.form['signupPassword']
            confirm_password = request.form['confirmPassword']

            if password != confirm_password:
                return render_template('a.html', error="Passwords do not match!")

            with open(CSV_FILE, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)
                for row in reader:
                    if row and row[1] == email:
                        return render_template('a.html', error="Email already exists.")

            add_user_to_csv(name, email, password)
            return render_template('a.html', message="Account created successfully. Please log in.")

        elif 'loginEmail' in request.form:
            email = request.form['loginEmail']
            password = request.form['loginPassword']

            if verify_user(email, password):
                # Redirect to blog page after login
                session["email"] = email  # Store email in session
                return render_template('Blogpage.html')

            return render_template('a.html', error="Invalid email or password.")

    return render_template('a.html')


# **NEW: API to Receive Location from Blog Page (WITHOUT Displaying on Webpage)**
@app.route('/location', methods=['POST'])
def get_location():
    data = request.json
    lat = data.get("latitude")
    lon = data.get("longitude")

    if lat and lon:
        email = session.get("email")  # Get logged-in user's email
        aqi_data = get_aqi(lat, lon)

        if "error" in aqi_data:
            return jsonify({"error": "Failed to fetch AQI data"}), 400

        city, state, country, aqi = aqi_data["city"], aqi_data["state"], aqi_data["country"], aqi_data["aqi"]

        # Log data (for debugging)
        print(f"📍 Location Received: {city}, {state}, {country}")
        print(f"🌫️ AQI Value: {aqi}")

        # Send email if AQI is greater than 150
        if aqi > 50 and email:
            user_name = session.get("user_name", "User")  # Get user's name
            print(f"🚨 Sending email to {email} because AQI in {city} is {aqi}")  # Debugging message
            mail.sendmail(email, user_name, city, aqi)


        # Return a success response without showing data on the webpage
        return jsonify({"message": "Location received successfully!"})

    return jsonify({"error": "Invalid location data"}), 400


# **Route Pages**
@app.route('/page1')
def page1():
    return render_template('Blogpage.html')


@app.route('/page2')
def page2():
    return render_template('mainweather.html')


@app.route('/page3')
def page3():
    return render_template('Mainairquality.html')


@app.route('/page4')
def page4():
    return render_template('ranked.html')


@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({"message": "Logged out successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Start locate.py automatically
    subprocess.Popen(["python", "locate.py"])

    app.run(debug=True)
