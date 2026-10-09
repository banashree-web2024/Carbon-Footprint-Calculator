# Carbon Footprint Calculator 🌱

## About the Project

Carbon Footprint Calculator is a web application that helps users estimate and track their carbon emissions from everyday activities.

It considers transportation, electricity consumption, food habits, and waste generation. Based on the information entered, the application calculates the estimated carbon footprint, displays a category-wise breakdown, and provides suggestions to help users reduce their emissions.

## Features

* User registration and login
* Carbon emission calculation based on daily activities
* Emission breakdown for transportation, electricity, food, and waste
* Recommendations for reducing carbon emissions
* Dashboard to view the latest calculation results
* History to track previous calculations
* MySQL database integration for storing user details and results

## Technologies Used

* **Frontend:** HTML, CSS, JavaScript
* **Backend:** Python, Flask
* **Database:** MySQL
* **Deployment:** GitHub, Render, Railway

## How It Works

1. Users register or log in to the application.
2. They enter details about their daily activities.
3. The Flask backend calculates the estimated carbon emissions.
4. The results are stored in the MySQL database.
5. Users can view their results, recommendations, and previous calculations.

## Database

The application uses MySQL to store user information and carbon footprint results.

* **`users`** – Stores registered user details.
* **`carbon_results`** – Stores carbon calculation results and supports history tracking.

The application associates calculation records with the respective user.

## Security

* Session-based user authentication
* Password hashing
* Environment variables for database configuration

## Deployment

The application is deployed using Render, with Railway providing the cloud-hosted MySQL database.

* **Live Application:** https://carbon-footprint-calculator-wjl5.onrender.com
* **GitHub Repository:** https://github.com/banashree-web2024/Carbon-Footprint-Calculator

## Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/banashree-web2024/Carbon-Footprint-Calculator.git
```

### 2. Open the project folder

```bash
cd Carbon-Footprint-Calculator
```

### 3. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure the database

Set the following environment variables according to your MySQL configuration:

```text
MYSQLHOST
MYSQLUSER
MYSQLPASSWORD
MYSQLDATABASE
MYSQLPORT
```

### 6. Run the application

```bash
python app.py
```

Open the local address displayed by Flask in your browser.

## Future Improvements

* Add monthly and yearly analytics with downloadable reports.
* Expand activity categories and personalize recommendations.
* Improve mobile responsiveness and sustainability goal tracking.

## Conclusion

This project provides a practical way to estimate and monitor carbon emissions from everyday activities. It also gave us hands-on experience with backend development, database management, user authentication, and deploying a full-stack web application.
