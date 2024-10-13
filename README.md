Student Management System
This repository contains the source code for a simple Student Management System. The system allows students to sign up, log in, and submit their information. Administrators can view the student rank list, allocate branches, and manage user accounts.

Files
admin_panel.php: Displays the student rank list and allows administrators to allocate branches.
admin_signin.php: Handles the administrator login process.
admin_signup.php: Allows administrators to sign up for an account.
branch_allocation.php: Displays the allocated branch for the logged-in student.
fetch_allocated_branch.php: Fetches the allocated branch for a student based on their name.
index.php: The main page where students can submit their information.
login.php: Handles the student login process.
logout.php: Logs out the currently logged-in user.
process_form.php: Processes the submitted student information and saves it to the database.
profile.php: Google authentication example (not used in this project).
signup.php: Allows students to sign up for an account.
student_dashboard.php: The student dashboard displaying the student information and branch allocation.
success.php: A success page displayed after submitting the student information.
Database
The system uses a MySQL database with the following tables:

student_marks: Stores the student information and allocated branch.
users: Stores the user accounts for administrators.
Setup
Set up the database by creating a new database and importing the database.sql file provided in this repository.
Update the database connection details in the PHP files.
Upload the PHP files to a web server.
Usage
Students can sign up for an account or log in to submit their information.
Administrators can log in to view the student rank list and allocate branches.