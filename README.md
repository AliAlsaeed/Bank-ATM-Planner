# Bank-ATM-Planner
This is a bank ATM planner that uses machine learning to help the bank to set its ATM machine's location based on its user's location. 
The bank can build more ATM machines in the area that no ATM machine is rechable in certain miles by a lot of Captital one cosutomers.
We cluster the user based on user's population density in cerntain area using DBSCAN algorithm. Location information (banks, ATMs, customers) is grabbed from Capital One's DataBase, using APIs provided during Daemon Dash Hackthon.
Visualization is done by including Google Maps's Javascript API.

A shell script is provided for integration of getting data, machine learning, and visualization.
# Usage:
./script.sh [1 - 3]
1. A hierarchical clustering algorithm, from Google Map's built-in API.
2. A density-based clustering algorithm, from Google Map's built-in API.
3. A density-based clustering algorithm (DBSCAN), from scikit-learning.
