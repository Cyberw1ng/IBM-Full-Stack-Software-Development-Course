## Car Dealership

This project was created as the capstone project for the IBM full stack developer course, found here: https://www.coursera.org/professional-certificates/ibm-full-stack-cloud-developer?skipBrowseRedirect=true . This project has been left public so that fellow lerners, people who might be interested in the course or people wondering through github can view it.

##### Project concept

The idea of the project is to create a template for a website, that lists car dealerships. The content of course being fictional and made up. 
![image](https://github.com/Jathn/agfzb-CloudAppDevelopment_Capstone/assets/124161756/9b576022-a672-48c6-ab2d-89315b68c8c8)
*This is what I made the front page look like, I know... a little dull :(*

The basics for front end and back end were created with django. The styling was implemented by myself using bootstrap and some parts also using css manually.
As is hinted in the upper right corner, this project used user management for signup and login. The django framework with it's ORM models provided an ease of implementation, also integrating with the html files.
![image](https://github.com/Jathn/agfzb-CloudAppDevelopment_Capstone/assets/124161756/2307131d-bc4b-4268-ba0a-943e289e3077)
*This is how a signup to the site might look*

The project relies on a couple other features too, such as fetching data from databases. The data for the dealerships and reviews for this dealership were originally implemented on IBM cloud functions. 
However in this version I use a locally run flask app for reviews and a node with express server to fetch the dealerships. These are then used by the django server to display information requested by the client.
When displaying the reviews for a dealership their sentiment is analyzed using a sentiment analyzer. They then get a happy face if they are positive and a sad face if they are negative. The sentiment analyzer I used was provided here: https://rapidapi.com/symanto-symanto-default/api/sentiment-analysis9/
![image](https://github.com/Jathn/agfzb-CloudAppDevelopment_Capstone/assets/124161756/110804ca-ef41-4387-bab3-d925c257940c)
