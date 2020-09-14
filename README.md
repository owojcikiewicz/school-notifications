### School Notifications
Due to the COVID-19 pandemic all schools in Poland were shut down in March, by the 25th of March the government has ordered schools to start remote teaching. In order to get attendance in class, a student was required to mark" the message sent from his teacher as "read" using our online gradebooks and reply when they recieved homework, I decided to completely automate this task using my gradebook's mobile API.

The initial project was a Discord bot created in Lua, I decided to re-write it in Python and use webhooks instead of bots. 

### Installation 
Open the configuration file located at `school-notifications/config.py`, enter the necessary data and install all necessary dependencies. After that, simply run the script using `python school-notifications/main.py`. 
