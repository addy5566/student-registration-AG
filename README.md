# Student Registration System (Django + MySQL)

A simple and secure student registration system built using Python Django and MySQL, developed as part of a technical assessment for an EdTech-focused use case.

The application allows students to register, securely stores sensitive information using encryption, sends confirmation emails, and provides an admin interface to view, filter, and export student data.

---

## Features

### Core Features (Assessment Requirements)
- Student registration with fields:
  - Name
  - Email (encrypted)
  - Mobile number (encrypted)
  - Class
- Secure encryption of email and mobile number before database storage
- Confirmation email sent after successful registration
- Auto-generated registration ID
- MySQL database integration
- Manual SQL script for table creation (no ORM used for schema generation)

### Additional Features (Value-Added)
- Admin page to view all registered students
- Search and filter students by name and class
- Export student list as CSV (ID, Name, Class)
- Clean and responsive UI using CSS
- Created and modified timestamps for auditing

---

## Tech Stack

- ##Backend:## Python, Django
- ##Database:## MySQL
- ##Frontend:## HTML, CSS
- ##Email Service:## SMTP (Gmail)
- ##Version Control:## Git & GitHub

---

## Project Structure

student_assessment/
│
├── edutech/
│ ├── manage.py
│ ├── edutech/
│ └── students/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── utils.py
│ ├── templates/
│ └── static/
│
├── student_table.sql
├── README.md
└── .gitignore


##  Database Schema

A manual SQL script is provided as required by the assignment.

## File: `student_table.sql`

  sql
CREATE TABLE students_student (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    mobile VARCHAR(255) NOT NULL,
    class_name VARCHAR(50) NOT NULL,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);


## Security & Encryption

Email and mobile number are encrypted using symmetric   encryption before being stored in the database

Decryption is performed only when required (e.g., sending confirmation email)

Encryption key is stored securely via environment configuration

##Email Configuration##

Confirmation email is sent after successful registration

Uses SMTP with TLS

Gmail App Password is used for authentication

## Running the Project Locally

1️⃣ Clone the Repository
git clone https://github.com/addy5566/student-registration-AG.git
cd student-registration-AG

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure MySQL Database

Create a database (e.g., edutech_db)

Update database credentials in settings.py

Execute student_table.sql manually in MySQL

5️⃣ Apply Migrations
python manage.py makemigrations
python manage.py migrate

6️⃣ Run Server
python manage.py runserver


Visit:

Registration page: http://127.0.0.1:8000/register/
Admin student list: http://127.0.0.1:8000/students/

## Testing

Manual test performed covering full flow:
Student registration
Encrypted storage verification
Email delivery
Admin list view
CSV export

## AI Usage Disclosure

As per the assignment guidelines:

AI tools were used only for guidance and clarification

No AI-generated code was blindly copied

All code was reviewed, understood, and manually implemented

AI Tool Used: ChatGPT Go
Purpose: Step-by-step understanding, debugging assistance, and documentation guidance
All implementation decisions were made manually


## Screenshots

Screenshots demonstrating the working application are available in the `screenshots/` directory, including:

- Student registration page
- Successful registration confirmation
- Email notification
- Encrypted database records
- Admin student list and filtering
- CSV export functionality


##  Documentation & References

### Application Flow
1 User opens the application and lands on the registration page.
2 User submits student details (name, email, mobile, class).
3 Sensitive data (email & mobile) is encrypted before storing in database.
4 A success page confirms registration.
5 Admin can view the registered students list.
6 Data is decrypted safely before display.

### References
- Django Official Documentation  
  https://docs.djangoproject.com/en/stable/

- Django Deployment (Gunicorn & WhiteNoise)  
  https://whitenoise.readthedocs.io/en/stable/

- Cryptography Fernet (Encryption)  
  https://cryptography.io/en/latest/fernet/

- Render Deployment Docs  
  https://render.com/docs/deploy-django




## Author

Aditya Raj
Computer Science Student / Backend Developer