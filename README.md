# Library Management System
This repository implements a library management system with two user roles: LIBRARIAN and MEMBER. The system provides user authentication using JWT and allows each role to perform specific tasks as described below.

## Features:
### User Authentication:
* Users can sign up as either a LIBRARIAN or MEMBER with a username and password.
* Users can log in using their credentials and obtain a JWT access token.
### Librarian Capabilities:
* Manage books: Add, update, and remove books from the library.
* Manage members: Add, update, view, and delete members.
* View member history: View all issue and return records of books borrowed by members.
* View active and deleted members.
### Member Capabilities:
* View available books and borrow or return them.
* Book status changes to BORROWED once issued, and back to AVAILABLE once returned.
* Delete their account.
* View personal borrowing history.

## API endpoints working demo (can consider watching at 2x speed!)
https://drive.google.com/file/d/1VnnnuCssWBc6hCUoJLzlth32RXhpQKH7/view?usp=sharing

## Admin login 
https://librarymanagementsystem-oc6y.onrender.com/admin/

username: admin 
password: password

## API Documentation
All APIs have been documented in a folder called Library Management using the open-source tool Bruno. This collection can be directly imported into Bruno for fast and easy access.
