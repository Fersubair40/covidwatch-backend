# What is it

This is a simple backend, written in Django, for storing the random identifiers created by the CovidWatch bluetooth project

# How to run it

* Check out the repo
* Make sure you have a PostgreSQL instance running
  * on localhost
  * database `covid19`
  * username `postgres`
* (optional) make a virtualenv
* install python requirements: `pip install -r requirements.txt`
  * On Mac/Catalina, you may need to comment out django_heroku to get this to run
* set a SECRET_KEY (random 50 character string) and an ENV (dev) in your environment
  * Best to do this with a script, or as part of virtualenv's `activate`

* `./manage.py migrate`
* `./manage.py runserver`

You now have the API running on localhost:8000

# Final Design Specification

The database will perform two functionalities: storing contact event numbers that are successfully authenticated, and transmitting contact event numbers to phones that request this information. 

The storage and bandwidth requirements of the database are a function of the number of infected and total users. Since the system is primarily decentralized, the server is used to pass messages but not to perform comparisons. This prevents anyone with access to the server from inferring the network structure and potentially user identities. For a small to mid-sized user base, every packet from an infected user can be transmitted to every other user.

Below is a rough estimate of the log file size for a single user:
- 50 bytes per contact event
- 3 nearby phones at a time
- Measurement every 5 minutes
- Active 12 hours a day
- Storage for 21 days

50\*3\*60/5\*12\*21 = 0.45 MB

The storage requirements scale linearly with the number of infected users. For example, with 200,000 infected users this would be on the order of 100GB. For a small number of infected users it is feasible to periodically download any updates to the dataset to the phones of all app users. The app can then compare the newly posted contact event numbers against their own history to check for matches. For a larger number of infected users, the dataset can be split using very low resolution location data. This way users can just download the portion of the dataset where there is the possibility of a match, lowering bandwidth requirements considerably.

There are several ways to implement the packet authentication procedure. The purpose of this procedure is to prevent undiagnosed users from falsely claiming to have the disease. Depending on the capacity of local health authorities, this could be achieved using an anonymous permission number provided to individuals with a positive diagnosis. More technically simple implementations include only allowing uploads from specific locations, or trusting users to report their diagnosis accurately.

If an unauthenticated user does manage to post to the server, the damage is minimized because the space of possible CENs is so large that they will not be able to guess additional CENs. They would only be able to send a false warning to people they had been in contact with.

The overall specification for the database is simple: it is publicly readable and stores Contact Event Numbers. If protections against false alarms are required permission numbers can be used, and if the database grows too large it can be fragmented based on general location.

