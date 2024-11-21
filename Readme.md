# Spotify to Youtube Music Playlist Migrator

## Overview

This python script allows you to transfer your Spotify playlists to YouTube Music. It provides an easy-to-use solution for transfering your favourite music collections between platforms.

## Features

* Fetch all Spotify playlists from your account
* Search and match tracks on YouTube Music
* Create new playlists in Youtube Music
* Detailed migration tracking
* Error handling and logging of failed migrations

## Prerequisites

Before you begin, ensure you have the following:

* Python 3.9+
* Spotify Developer Account
* YouTube Music Account
* pip (Python package manager)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Malegiraldo22/spotify-to-ytmusic-migrator.git
cd spotify-to-yt-music-migrator.git
```

2. Create a virtual environment (recommended):

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

### Spotify Setup

1. Go to Spotify Developer Dashboard
2. Create a new application
3. Get your Client ID and Client Secret
4. Set redirect URI to `http://localhost:8888/callback`

### YouTube Music Authentication

1. Open Chrome/Firefox and go to music.youtube.com
2. Log in to your account
3. Open Developer Tools (F12)
4. Go to Network Tab
5. Reload page and filter by `/browse` using the search bar of the developer tools. If you don't see the request, try scrolling down a bit or clicking on the library button in the top bar
6. 
    * If you are using Firefox, Verify that the request looks like this: **Status** 200, **Method** POST, **Domain** music.youtube.com, **File** `browse?...` and then copy the request headers (right click > copy > copy request headers)

    * If you are using Chromium (Chrome/Edge), verify that the request looks like this: **Status** 200, **Name** `browse?...` and then click on the name of any matching request. In the "Headers" tab, scroll to the section "Request headers" and copy everything starting from "accept: */*" to the end of the section

### Environment Variables

Create a `.env` file in the project root:

```bash
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
```

### Usage

Run the migration script:

```bash
python spotify_to_ytmusic/script.py
```

The script will:

1. Display your Spotify playlists
2. Let you choose which playlist to migrate
3. Search and add tracks to a new YouTube Music playlist
4. Generate a `failed_tracks.json` for tracks that couldn't be migrated

## Troubleshooting

* Refresh YouTube Music authentication headers if migration fails
* Do not use YouTube Music or YouTube while migrating
* Check internet connection
* Ensure all API credentials are correct
* Review `failed_tracks.json`for migration issues

## Limitations

* Exact track matching is not guaranteed
* Some tracks might not be found on YouTube Music
* Authenticacion headers expire periodically

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature)
3. Commit your changes (`git commit -m 'Add some AmazingFeature`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information

## Contact

Alejandro Giraldo - magiraldo2224@gmail.com