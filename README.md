# CSC 4350 Project 1 Milestone 2 by Naima Mohamed 

### A webpage that displays data on a random artist from the list of a user's saved artists. 
- User signs up / log in with their username to view their account page. 
- If first time user, page simply displays a form that instructs them to add a spotify artist ID.
- If the artist ID is valid, it is added to the list of the user's saved artists. User can add multiple artists.
- Then, the page displays data on a random artist from the list of the user's saved artists. 

### View the website here: [https://ourmusic.herokuapp.com/](https://ourmusic.herokuapp.com/ "website link").


## Technologies, Frameworks, Libraries, and APIs used
* Developed in Azure VM using VS Code. 
* Version tracking using Git & Github.
* Deployed using Heroku.
* PYTHON - 
  * os & dotenv (modules) - to get values in .env file and set them as environment variables in spot.py.
  * Spotify (library) - simplifies the process of accessing music data through Spotify's Web API.
  * flask (framework) - allows the web app to developed easily / fetches python data and displays it on the webpage.
    * Flask-Login - flask extension that manages user sessions

    * Flask-SQLAlchemy - flask extension that provides object-relational mapping between the Postgres database & the python logic.
* HTML - displays the data on a webpage & creates forms that send HTTP POST requests to the DB Server.
* CSS - styles the data in a readable & visually appealing way.
* Spotify API - used to get information on: 
   *  artist: name, image, top tracks.
   *  song: name, song image, preview URL.
* Genius API - used to get lyrics of the current song.
 * PostgreSQL - Database management system that allows a user's username and favorite artist data to be saved.
 
## Setup
1. Install in terminal: os, dotenv, spotipy, random, requests, flask, psycopg2-binary, flask-login, flask-sqlalchemy, PostgreSQL

2. Create [Spotify APP](https://developer.spotify.com/documentation/web-api/ "Spotify API") and copy the Client ID and Client Secret.
3. Create [Genius APP](https://docs.genius.com/ "Genius API") and copy the genius token.
4. Set up your PostgreSQL DB using [Heroku Postgres](https://devcenter.heroku.com/articles/heroku-postgresql "Heroku PostGress" ) and copy the Database URL.
5. Create .env file in the project directory and store your:
    - Spotify client id & client secret
    - Genius access token.
    - Heroku DB URL
    - Flask app secret key: can be any value you want, 
    [but preferred to be a long random string](https://www.acunetix.com/vulnerabilities/web/flask-weak-secret-key/) 

    Do so with the following code:
    ```python
      export CLIENT_ID = "your-spotify-client-id"
      export CLIENT_SECRET = "your-spotify-client-secret"
      export GENIUS_TOKEN = "your-genius-access-token"
      export DATABASE_URL = "your-heroku-db-url"
      export SECRET_KEY = "your-super-secret-app-key"
    ```
6. If want to run on localhost: run app.py and follow the link to your browser to view the site! 


## Technical Issues / Problems

### Milestone 1
1. Git was not letting me push to my main branch, so I searched on stack overflow for a solution. I found out I could use the command "git push -f origin main." It worked; however, I lost all of my previous commits.
2. Another issue I found was that when I deployed my app to Heroku, I got an "Application Error." When I checked the logs, I found that I had the error "Heroku H10-App crashed". After searching through my code, I discovered that I had not initialized port to "port=int(os.getenv('PORT', 8080))".
3. An issue I had was figuring out how to return multiple values in my get methods in spot.py, and then access them in my Flask app. By checking out stack overflow, I was able to figure out how to do so. By using methodName[i], you can access the variables the function returns.

### Milestone 2
1. I could not figure out how to separate my DB models into another file without getting a circular import error. I also could not focus figuring it out due to fast approaching deadline. Therefore, I kept all my code DB & routes in one file: app.py.
2. I was pushing to my Heroku master branch, but my app was not updating with my changes. After googling, I figured out that I had to [clear my build cache](https://help.heroku.com/18PI5RSY/how-do-i-clear-the-build-cache) to rebuild my app.
3. When I was trying the figure out the problem in 2, I tested pushing to Heroku using non-specific commits like "asdfseff," not knowing that it also pushed to my GitHub branch. I attempted to use the 'rebase' command to delete those commits. However, when I deleted the commits, I had to merge my main branch into my second, and the commits appeared again.

## Additional Features To Implement
### Milestone 1:
1. Using Twitter API to access tweets mentioning the artist name & song - was going to include this, but there is an approval application that takes time.
2. Use other languages such as Javascript to make the webpage more visually appealing. For example, creating a custom music player with javascript.
3. Display more information on artists using the Spotify API, such as their albums and related artists.
### Milestone 2:
1. Make sign-up/login forms more in-depth: adding email & password authentication - was going to include passwords but could not due to time. 
2. Display more complex user-specific information, such as the names of all of their saved artists.
3. Allow more interaction between the user and the database, such as the ability for the user to delete artists.

## Experience on Milestone 2
-  How did your experience working on this milestone differ from what you pictured while working through the planning process? What was unexpectedly hard? Was anything unexpectedly easy?
* I found the planning process to be very helpful in making me understand exactly what I needed to do for this milestone and in what order. This made my experience with this milestone much better than in milestone 1.
* Something that was unexpectedly hard was setting up the database using SQL-Alchemy. At first, I tried setting up my database modelin a file called models.py, but I kept recieving a circular import error.
* It was unexpectedly easy using Flask-Login and making it interact with the database.
