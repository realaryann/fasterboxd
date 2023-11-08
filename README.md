# Fasterboxd 🏎️💨

<h2>Fasterboxd is a desktop python app capable of using web scraping technologies to deliver accurate recommendations</h2>
<p>It uses the following tech-stack</p>
<ul>
  <li>BeautifulSoup</li>
  <li>OOP</li>
  <li>python requests</li>
  <li>Pickle</li>
  <li>TKinter</li>
</ul>

![image](https://github.com/realaryann/fasterboxd/assets/70107111/0c151bc5-aa1d-4ee4-b6b5-373263f9036a)
<br>
<p>Home Page for FasterBoxd</p>

<p>Data for recommendations was obtained from the following websites</p>
<ul>
  <li>Rotten Tomatoes - TV Shows</li>
  <li>LetterBoxd - Movies</li>
</ul>
<p>LetterBoxd was used due to its efficient url creation and large number of recommendations for each movie. Unfortunately, LetterBoxd does not support TV Shows.</p>
<p>Rotten Tomatoes was used due to its efficient url creation. Number of recommendations are capped at 5 for each TV Show.</p>

<p>The reason why this app is known as "FasterBoxd" is due to the behind-the-scenes of every query<br>
  <ol>
    <li>Every time a movie or show and a number of recommendations are inputed, FasterBoxd converts the input into a SHOW or MOVIE object.</li>
    <li>Then, the shows.pickle or movies.pickle files are browsed to see if this movie was previously queryed.</li>
    <li>If they were, no web scraping is done and the previous query is loaded using pickle.</li>
    <li>the SHOW and MOVIE classes contain attributes which inclue list of similar movies, making it easy to print it via TKinter</li>
 </ol>
</p>

<h3>This allows for efficient and offline querying of movies and tv shows.</h3>

<h2>Currently in-development processes: </h2>
<p>The third major use of FasterBoxd is the ability to log or record movies and tv shows that the user has already seen.</p>
<p>Current idea is to use the time library to generate unique filenames for users that they can re-use to record their recently watched movies/shows</p>
