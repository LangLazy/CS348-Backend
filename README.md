# CS348-Backend

This repository holds the code which is used as the Backend of our full stack application.
This application is hosted on an AWS EC2 instance, and as such works in that environment specifically. 
It also requires that certain environemnt variables be set to even communicate with the associated MySql DB.

The features we support are:

1. Finding all direct and indirect citations of a specific paper across the dataset.
2. Find papers based on specific fields such as author name, keywords and paper title.
3. The ability to add your own paper.
4. The ability to update any paper's fields.
5. Account creation.
6. User sign-in.
7. Author elo system, crowd source author ranking to determine which authors are the most influencial.
8. A leaderboard of the top ranking authors. 