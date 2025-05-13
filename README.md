# CITS3403 AWD Group Project

## Contributors
| UWA ID   |  Name    | Github Username |
|----------|----------|----------|
| 23600251   | Linshan Xiao   | LinshanXiao  |
| 22975178   | Dirk Haasbroek | AfricanAlien |
| 24092758   | Yiming Ding    | Vincent0301 |
| 23865288   | Andrew Gibson  | wizarddog61728    | 

# GameNalyzer 

**GameNalyzer** is a game statistics web application that allows users to upload their gameplay data, visualize performance trends, and selectively share records with friends. 

## Features

- **User Authentication**  
  Users can register, log in, and manage their profile.

- **Upload Game Data**  
  Upload gameplay data via CSV files or input manually with structured game information.

- **Data Visualisation**  
  Interactive charts and summaries of user-uploaded game data.

- **Data Sharing**  
  Share selected matches with users from your friend list.

- **User Profile**  
  View your upload history.

---
## Project Structure
```
├── app/
│ ├── auth/ # Authentication blueprint
│ ├── main/ # Main routes blueprint
│ ├── upload/ # Upload routes blueprint
│ ├── static/
│ │ ├── css/
│ │ ├── images/
│ │ ├── js/
│ │ └── template.csv # Sample CSV format
│ ├── templates/ # Jinja HTML templates
│ ├── init.py
│ ├── config.py
│ ├── models.py
│ └── app.db # SQLite database file
│
├── Deliverables/ 
├── tests/
├── migrations/ # Flask-Migrate migration files
├── run.py # Entry point for running the Flask app
├── requirements.txt # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

---
## Running the App Locally
### 1. Clone the repository
```
git clone https://github.com/LinshanXiao/AWD-Project.git
```
### 2. Create a virtual environment and activate it
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Initialize the database
```
flask db upgrade
```
### 5. Run the app 
```
flask run
```
Access the app at http://localhost:5000

---
## Testing
- **Unit Testing**  
Unit tests are written using the unittest framework. To run unit tests:
```
python -m unittest discover tests
```
- **UI Testing with Selenium**
- To run Selenium-based browser tests:
- Ensure you have selenium and the appropriate WebDriver installed (e.g., ChromeDriver).
- Run the tests:
```
python tests/test_ui.py
```
## Target audience
This project is intended for gamers who wish to track, analyze, and share their match statistics. It is also built as a practical web development assignment for CITS3403 Agile Web Development.
- **Note**
- This app is intended for local use only and is not deployed online.
- All game data is private by default unless explicitly shared by the user.




