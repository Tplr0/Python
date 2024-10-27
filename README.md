# Python
**Spotify Stats Viewer**
spotify_stats.py is a Python script that allows you to view your top tracks, artists, genres, and recently played tracks from your Spotify account. It uses the Spotify API to retrieve data, displaying it in a user-friendly GUI built with Tkinter.

**Features**
- Top Tracks: View your top 50 tracks based on your listening habits over different time ranges.
- Top Artists: See your top 50 artists over different periods.
- Genres: Get a list of genres based on your top artists.
- Recently Played Tracks: View your most recently played tracks on Spotify.
- Theme Toggle: Switch between light and dark themes.
- Last Updated Timestamp: Displays the time of the latest data refresh.
  
**Prerequisites**
To run this project, you'll need:
- Python 3.6+
- Spotify Developer Account: You'll need to create a Spotify application to obtain Client ID and Client Secret.

**Getting Started**
*Clone the Repository:*

[https://github.com/Tplr0/spotifystats-python/blob/main/spotify_stats.py](https://github.com/Tplr0/spotifystats-python/blob/main/spotify_stats.py
)

```
git clone https://github.com/Tplr0/spotifystats-python.git
cd spotifystats-python
```
or
```
gh repo clone Tplr0/spotifystats-python
```


*Install Dependencies: Use pip to install the required packages:*

```python -m pip install spotipy tk```
or
```py -m pip install spotipy tk```

*Create a Spotify Application:*

1. - Go to the Spotify Developer Dashboard and log in with your Spotify account.
2. - Create a new application.
3. - In the application settings, add a Redirect URI: http://localhost:8888/callback.
4. - Copy the Client ID and Client Secret from the application settings.

*Create the Required Text Files: To store your Client ID and Client Secret, create two text files in the same directory as spotify_stats.py:*

- Clientid.txt: Create a text file named Clientid.txt and paste your Client ID as the only content of this file.
- Clientsecret.txt: Create a text file named Clientsecret.txt and paste your Client Secret as the only content of this file.

*Run the Script: After completing the setup, you can run the script by:*

```python spotify_stats.py```
or
```py spotify_stats.py```

**Usage**

- Time Range Selection: Choose the time range (Last 4 weeks, Last 6 months, or All time) from the dropdown menu to view your top tracks and artists based on that period.
- Fetch Data: Click the "Fetch Data" button to retrieve and display your Spotify stats.
- Theme Toggle: Use the "Toggle Theme" button to switch between light and dark modes.
- Double-click on Tracks: Double-clicking on a track in the "Top Tracks" list opens it in your default browser.
- Last Updated: The "Last Updated" label displays the last time data was fetched from Spotify.

**Troubleshooting**
- ModuleNotFoundError: No module named 'spotipy': Ensure spotipy is installed using pip install spotipy and try running the script again.
- SpotifyOAuthError: No client_id: Double-check that Clientid.txt and Clientsecret.txt files are correctly placed in the same directory as spotify_stats.py and contain the correct values.
