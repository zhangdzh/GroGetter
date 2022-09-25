# Groceries Tracker
A project for software engineering class. The project idea is to create 
an application to help customers keep track of groceries: current items and items to buy.

### Group Members: 
- Dorothy Zhang
- Jeffery Tse
- Jun Hyung Kim
- Yeseon Kim

### Build Instructions
To build production, type `make prod`.
To create the env for a new developer, run `make dev_env`.
To test locally, type `make unit`.

### Required Features
- Allow users to create account with user authentication
- Display login/logout page
- Keep track of expiration dates for each grocery item
- Keep track of the number of items a user already has at home
- Suggest items to be thrown away/purchased depending on the expiration dates
- Allow user entry of new grocery items to buy
- Allow user to edit how many of a specific item should be bought/any description to the item 
- Allow user entry of purchased items and expiration dates
- Suggest expiration date if user does not manually input
- List all current groceries (purchased)
- List items on grocery list
- Provide sorted expiration dates and corresponding items
- Allow user to share grocery list with other users

### Design
- Required features will correspond to API endpoints
- Database will store user information 
- Web framework created with React

### Team Meeting Notes
[Software Engineering Project Team Notes](https://docs.google.com/document/d/11KMQVGyT2PAPuXw1jjtB6jfMHi0jvwKVs2K-rYYlDuw/edit?usp=sharing)
