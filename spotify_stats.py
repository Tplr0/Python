import tkinter as tk
import webbrowser
import spotipy
import datetime
from spotipy.oauth2 import SpotifyOAuth
from tkinter import ttk
from itertools import islice
from tkinter.messagebox import showwarning

def Client_Id():
    try:
        with open('Clientid.txt', 'r') as f:
            clientid = f.readline().strip()
        return clientid
    except FileNotFoundError:
        print("Client ID file not found.")
        return None

def Client_Secret():
    try:
        with open('Clientsecret.txt', 'r') as f:
            clientsecret = f.readline().strip()
        return clientsecret
    except FileNotFoundError:
        print("Client secret file not found.")
        return None

# Set up Spotify authentication
CLIENT_ID = Client_Id()
CLIENT_SECRET = Client_Secret()
REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-top-read user-read-recently-played"

# Spotify authentication manager
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))

# Function to get top tracks, artists, genres, and recently played tracks
def get_top_data():
    try:
        selected_time_range = time_range_var.get()
        api_time_range = 'short_term' if selected_time_range == 'Last 4 weeks' else 'medium_term' if selected_time_range == 'Last 6 months' else 'long_term'

        # Fetch top tracks with numbering
        track_listbox.delete(0, tk.END)
        track_urls.clear()
        results = sp.current_user_top_tracks(limit=50, time_range=api_time_range)
        for idx, track in enumerate(results['items'], start=1):
            track_name = track['name']
            artist_name = ", ".join([artist['name'] for artist in track['artists']])
            spotify_url = track['external_urls']['spotify']
            track_listbox.insert(tk.END, f"{idx}. {track_name} - {artist_name}")
            track_urls.append(spotify_url)

        # Fetch top artists with numbering
        artist_listbox.delete(0, tk.END)
        top_artists = sp.current_user_top_artists(limit=50, time_range=api_time_range)
        for idx, artist in enumerate(top_artists['items'], start=1):
            artist_listbox.insert(tk.END, f"{idx}. {artist['name']}")

        # Set the maximum number of genres to display
        MAX_GENRES = 50  # Adjust this limit as needed

        # Fetch genres with numbering and apply the limit
        genre_listbox.delete(0, tk.END)
        genres = set(genre for artist in top_artists['items'] for genre in artist['genres'])
        for idx, genre in enumerate(islice(genres, MAX_GENRES), start=1):
            genre_listbox.insert(tk.END, f"{idx}. {genre}")

        # Fetch recently played tracks with numbering
        recently_played_listbox.delete(0, tk.END)
        recently_played = sp.current_user_recently_played(limit=50)
        for idx, item in enumerate(recently_played['items'], start=1):
            track = item['track']
            track_name = track['name']
            artist_name = ", ".join([artist['name'] for artist in track['artists']])
            recently_played_listbox.insert(tk.END, f"{idx}. {track_name} - {artist_name}")

        # Update last updated timestamp
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_updated_label.config(text=f"Last Updated: {update_time}")

    except Exception as e:
        showwarning("Error", f"Failed to retrieve data: {str(e)}")


# Function to open Spotify track in browser
def open_spotify_track(event):
    try:
        selection = track_listbox.curselection()
        if selection:
            webbrowser.open(track_urls[selection[0]])
    except IndexError:
        showwarning("Error", "Please select a valid track.")

# Toggle theme function
def toggle_theme():
    global is_dark_mode
    if is_dark_mode:
        apply_light_mode()
    else:
        apply_dark_mode()
    is_dark_mode = not is_dark_mode

# Apply Dark Mode
def apply_dark_mode():
    root.configure(bg="black")
    style.configure("TFrame", background="black")
    style.configure("TLabel", foreground="white", background="black")
    style.configure("TButton", foreground="white", background="black")
    style.configure("TCombobox", foreground="white", fieldbackground="black", background="black")
    style.map("TCombobox",
              fieldbackground=[('readonly', 'black')],
              foreground=[('readonly', 'white')],
              background=[('readonly', 'black')]
              )
    track_listbox.configure(bg="black", fg="white", highlightbackground="black", highlightcolor="black", selectbackground="gray")
    artist_listbox.configure(bg="black", fg="white", highlightbackground="black", highlightcolor="black", selectbackground="gray")
    genre_listbox.configure(bg="black", fg="white", highlightbackground="black", highlightcolor="black", selectbackground="gray")
    recently_played_listbox.configure(bg="black", fg="white", highlightbackground="black", highlightcolor="black", selectbackground="gray")
    fetch_button.configure(style="TButton")
    theme_toggle_button.configure(style="TButton")

# Apply Light Mode
def apply_light_mode():
    root.configure(bg="white")
    style.configure("TFrame", background="white")
    style.configure("TLabel", foreground="black", background="white")
    style.configure("TButton", foreground="black", background="white")
    style.configure("TCombobox", foreground="black", fieldbackground="white", background="white")
    style.map("TCombobox",
              fieldbackground=[('readonly', 'white')],
              foreground=[('readonly', 'black')],
              background=[('readonly', 'white')]
              )
    track_listbox.configure(bg="white", fg="black", highlightbackground="white", highlightcolor="white", selectbackground="lightgray")
    artist_listbox.configure(bg="white", fg="black", highlightbackground="white", highlightcolor="white", selectbackground="lightgray")
    genre_listbox.configure(bg="white", fg="black", highlightbackground="white", highlightcolor="white", selectbackground="lightgray")
    recently_played_listbox.configure(bg="white", fg="black", highlightbackground="white", highlightcolor="white", selectbackground="lightgray")
    fetch_button.configure(style="TButton")
    theme_toggle_button.configure(style="TButton")

# Set up Tkinter window
root = tk.Tk()
root.title("Spotify Data")

# Initialize theme settings
is_dark_mode = False
style = ttk.Style()
style.theme_use('clam')

# Make window resizable
root.geometry("1000x800")
root.rowconfigure(1, weight=1)
root.columnconfigure(0, weight=1)

# Open the window in maximized (windowed fullscreen) mode
root.state('zoomed')

# Dropdown for Time Range at the top
time_range_var = tk.StringVar(value='Last 4 weeks')
time_range_label = ttk.Label(root, text="Select Time Range:", style="TLabel")
time_range_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

time_range_dropdown = ttk.Combobox(root, textvariable=time_range_var, state="readonly", style="TCombobox")
time_range_dropdown['values'] = ['Last 4 weeks', 'Last 6 months', 'All time']
time_range_dropdown.grid(row=0, column=0, padx=150, pady=5, sticky="ew")

# Last Updated Label
last_updated_label = ttk.Label(root, text="Last Updated: Not yet updated", style="TLabel")
last_updated_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")

# Frame for the listboxes (tracks, artists, genres)
listbox_frame = ttk.Frame(root, padding="10", style="TFrame")
listbox_frame.grid(row=1, column=0, sticky="nsew")

# Configure the grid for the listboxes to be horizontally next to each other
listbox_frame.columnconfigure(0, weight=1)
listbox_frame.columnconfigure(1, weight=1)
listbox_frame.columnconfigure(2, weight=1)
listbox_frame.rowconfigure(1, weight=1)

# Labels for each Listbox
track_listbox_label = ttk.Label(listbox_frame, text="Top 50 Tracks:", style="TLabel")
track_listbox_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

artist_listbox_label = ttk.Label(listbox_frame, text="Top 50 Artists:", style="TLabel")
artist_listbox_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")

genre_listbox_label = ttk.Label(listbox_frame, text="Top 50 Genres:", style="TLabel")
genre_listbox_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

# Listbox for Top Tracks
track_listbox = tk.Listbox(listbox_frame, height=5)
track_listbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
track_urls = []

# Listbox for Top Artists
artist_listbox = tk.Listbox(listbox_frame, height=5)
artist_listbox.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

# Listbox for Genres
genre_listbox = tk.Listbox(listbox_frame, height=5)
genre_listbox.grid(row=1, column=2, padx=10, pady=5, sticky="nsew")

# Bind double-click action to open Spotify track in browser
track_listbox.bind("<Double-1>", open_spotify_track)

# Label and Listbox for Recently Played Tracks
recently_played_label = ttk.Label(listbox_frame, text="Recently Played Tracks:", style="TLabel")
recently_played_label.grid(row=2, column=1, padx=10, pady=5, sticky="n")

recently_played_listbox = tk.Listbox(listbox_frame, height=13)
recently_played_listbox.grid(row=3, column=1, padx=10, pady=5, sticky="nsew")

# Button to fetch the top data
fetch_button = ttk.Button(root, text="Fetch Data", command=get_top_data, style="TButton")
fetch_button.grid(row=2, column=0, padx=150, pady=10, sticky="w")

# Theme toggle button
theme_toggle_button = ttk.Button(root, text="Toggle Theme", command=toggle_theme, style="TButton")
theme_toggle_button.grid(row=2, column=0, padx=150, pady=10, sticky="e")

# Apply initial light mode (default)
apply_light_mode()

# Run the Tkinter event loop
root.mainloop()
