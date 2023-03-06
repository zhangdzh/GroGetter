# Groceries Tracker
A project for software engineering class. The project idea is to create 
an application to help customers keep track of groceries: current items and items to buy.

### Group Members: 
- Dorothy Zhang
- Jeffery Tse
- Jun Hyung Kim
- Yeseon Kim

### Web link:
http://zhangdzh.pythonanywhere.com/

### Build Instructions (makefile instructions)
To build production, type `make prod`.
Automatic deploy to PythonAnywhere is done by GitHub Actions.
To create the env for a new developer, run `make dev_env`.
To run all tests, type `make all_tests`.
To lint everything including tests, type `make lint_all`.
To test or lint a specific directory, type `make tests` or `make lint` 
respectively.
To push changes to github, type `make github`.

### Run in your localhost
Frontend repository: https://github.com/zhangdzh/GroGetterFrontend
To run locally, type `npm start`.
Make sure you have node.js or npm installed.

### User Endpoints
- User sign in
- List all available users
- Add a new user
- Remove an existing user
- Get descriptive details of a user

### Groceries Endpoints
- List items in grocery list
- Create a new list
- Delete a list
- Get descriptive details of a list
- List items by type
- Update item details
    - Expiration date
    - Quantity

### Design
- Required features will correspond to API endpoints
- Database will store user information as a dictionary
- Database will constantly be updated
- Web framework created with React

### Team Meeting Notes
[Software Engineering Project Team Notes](https://docs.google.com/document/d/11KMQVGyT2PAPuXw1jjtB6jfMHi0jvwKVs2K-rYYlDuw/edit?usp=sharing)
