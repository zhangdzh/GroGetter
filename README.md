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
- Database will constantly be updated
- Web framework created with React
- Each user will be in the key to a dictionary of grocery lists
- Each grocery list has a name as the key and a dictionary of items as the value
- Each item has a name as the key and tuple of grocery type and expiration date as the value

### Team Meeting Notes
[Software Engineering Project Team Notes](https://docs.google.com/document/d/11KMQVGyT2PAPuXw1jjtB6jfMHi0jvwKVs2K-rYYlDuw/edit?usp=sharing)
