# CITS3403 AWD Group Project

## Contributors
| UWA ID   |  Name    | Github Username |
|----------|----------|----------|
| 23600251   | Linshan Xiao   | LinshanXiao  |
| 22975178   | Dirk Haasbroek | AfricanAlien |
| 24092758   | Yiming Ding    | Vincent0301 |
| 23865288   | Andrew Gibson  | wizarddog61728    | 

# GameNalyzer 

**GameNalyzer** is a web application that transforms user gameplay data into clear, visual statistics, helping users track and understand their performance. It also allows users to compare their stats with others for deeper insights.


## Features

- **User Authentication**  
  Users can  register for an account login and manage their profile.

- **Upload Game Data**  
  Users can upload their game data by either inputting their information manually or with the use of a CSV file.

- **Personalisation** 
  You can download a profile picture to personalise your account.

- **Multiple Game Support**  
  In the account settings the user is able to input their username for multiple games such as PUBG, Valorant, Apex Legends, as well as League of Legends. They can then access these individual game statistics.

- **Data Visualisation**  
  Once the website has been given the data it summarises the information into charts and graphs. These charts and graphs dynamically change when more data is provided.

- **Data Sharing**  
  Users are able to add and accept other users as friends, allowing them to compare and view each others statistics. 

- **User Profile**  
  Each user has a dedicated profile page summarizing their game activity, linked accounts, and performance metrics.

- **Update Information** 
  In the acccount settings users are able to change their username for each of the supported games. 


---
## Project Structure
```
├── app/
│ ├── auth/ # Authentication blueprint
│ ├── main/ # Main routes blueprint
│ ├── static/
│ │ ├── css/
│ │ ├── images/
│ │ ├── js/
│ │ └── template.csv # Sample CSV format
│ ├── templates/ # Jinja HTML templates
│ ├── upload # Upload routes blueprint
│ └── utils
│   ├── init.py
│   ├── config.py
│   ├── forms.py
│   └── models.py
├── migrations
├── tests
├── .gitignore
├── LICENSE
├── README.md
├── populate_users.py
├── requirement.txt
└── run.py

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
python -m unittest discover -s tests

```
- **UI Testing with Selenium**
- To run Selenium-based browser tests:
- Ensure you have selenium and the appropriate WebDriver installed (e.g., ChromeDriver).
- Run the tests:
```
python tests/system_test.py
```
## Target audience
This project is designed for gamers who play League of Legends, Apex Legends, PUBG, and Valorant, and want to track and analyze their in-game performance. It provides visual graphs and statistics to help users gain insights into how they’re performing over time.
- **Note**
- This app is intended for local use only and is not deployed online.
- All game data is private by default unless explicitly shared by the user.




