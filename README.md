# Groceries Tracker
A project for software engineering class. The project idea is to create 
an application to help customers keep track of groceries: current items and items to buy.

### Group Members: 
- Dorothy Zhang
- Jeffery Tse
- Jun Hyung Kim
- Yeseon Kim

### Build Instructions (makefile instructions)
To build production, type `make prod`.
To create the env for a new developer, run `make dev_env`.
To run all tests, type `make all_tests`.
To lint everything including tests, type `make lint_all`.
To test or lint a specific directory, type `make tests` or `make lint` 
respectively.
To push changes to github, type `make github`.

### User Endpoints
- User sign up
- User sign in
- List all available users
- Get description of a user
- Delete a user

### Grocery List Endpoints
- List all active user lists
- Create a list
- Delete a list
- Get description of a list

### Grocery Type Endpoints
- List all grocery types
- Get descriptions of each grocery type

### List Manager Actions
- Enter expiration dates
- Add information to a list
- Sort list items by expiration date
- Add items to list

### Design
- Required features will correspond to API endpoints
- Database will store user information as a dictionary
- Each user information in the database will have a username, grocery list name, number of items, and grocery list
- Grocery list in the database is a dictionary with item name as the keys and expiration date as values
- Database will constantly be updated
- Web framework created with React

### Team Meeting Notes
[Software Engineering Project Team Notes](https://docs.google.com/document/d/11KMQVGyT2PAPuXw1jjtB6jfMHi0jvwKVs2K-rYYlDuw/edit?usp=sharing)
