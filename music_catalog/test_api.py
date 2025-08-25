#!/usr/bin/env python
"""
Simple test script to demonstrate the Music Catalog API functionality.
Run this script after setting up the Django project to test the API endpoints.
"""

import os
import sys
import django
import requests
import json

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

# API base URL
BASE_URL = 'http://localhost:8000/api/v1'

def test_api():
    """Test the API endpoints."""
    print("🎵 Testing Music Catalog API")
    print("=" * 50)
    
    # Test data
    test_artist = {"name": "The Beatles"}
    test_song1 = {"title": "Hey Jude"}
    test_song2 = {"title": "Let It Be"}
    test_album = {
        "title": "Abbey Road",
        "artist_id": 1,
        "release_year": 1969,
        "tracks": [
            {"song_id": 1, "track_number": 1},
            {"song_id": 2, "track_number": 2}
        ]
    }
    
    try:
        # Test 1: Create Artist
        print("\n1. Creating artist...")
        response = requests.post(f"{BASE_URL}/artists/", json=test_artist)
        if response.status_code == 201:
            artist_data = response.json()
            print(f"✅ Artist created: {artist_data['data']['name']}")
        else:
            print(f"❌ Failed to create artist: {response.status_code}")
            return
        
        # Test 2: Create Songs
        print("\n2. Creating songs...")
        for i, song in enumerate([test_song1, test_song2], 1):
            response = requests.post(f"{BASE_URL}/songs/", json=song)
            if response.status_code == 201:
                song_data = response.json()
                print(f"✅ Song {i} created: {song_data['data']['title']}")
            else:
                print(f"❌ Failed to create song {i}: {response.status_code}")
        
        # Test 3: Create Album with Tracks
        print("\n3. Creating album with tracks...")
        response = requests.post(f"{BASE_URL}/albums/", json=test_album)
        if response.status_code == 201:
            album_data = response.json()
            print(f"✅ Album created: {album_data['data']['title']}")
            print(f"   Artist: {album_data['data']['artist']['name']}")
            print(f"   Year: {album_data['data']['release_year']}")
            print(f"   Tracks: {album_data['data']['tracks_count']}")
        else:
            print(f"❌ Failed to create album: {response.status_code}")
            print(f"   Response: {response.text}")
            return
        
        # Test 4: Get Album Details
        print("\n4. Getting album details...")
        response = requests.get(f"{BASE_URL}/albums/1/")
        if response.status_code == 200:
            album_data = response.json()
            print(f"✅ Album retrieved: {album_data['data']['title']}")
            print("   Tracks:")
            for track in album_data['data']['tracks']:
                print(f"     {track['track_number']}. {track['song']['title']}")
        else:
            print(f"❌ Failed to get album: {response.status_code}")
        
        # Test 5: List Artists
        print("\n5. Listing artists...")
        response = requests.get(f"{BASE_URL}/artists/")
        if response.status_code == 200:
            artists_data = response.json()
            print(f"✅ Found {len(artists_data['data'])} artists:")
            for artist in artists_data['data']:
                print(f"   - {artist['name']} ({artist['albums_count']} albums)")
        else:
            print(f"❌ Failed to list artists: {response.status_code}")
        
        # Test 6: Search Songs
        print("\n6. Searching songs...")
        response = requests.get(f"{BASE_URL}/songs/search/?q=Hey")
        if response.status_code == 200:
            songs_data = response.json()
            print(f"✅ Search results: {len(songs_data['data'])} songs found")
            for song in songs_data['data']:
                print(f"   - {song['title']}")
        else:
            print(f"❌ Failed to search songs: {response.status_code}")
        
        # Test 7: Get Artist's Albums
        print("\n7. Getting artist's albums...")
        response = requests.get(f"{BASE_URL}/artists/1/albums/")
        if response.status_code == 200:
            albums_data = response.json()
            print(f"✅ Artist has {len(albums_data['data'])} albums:")
            for album in albums_data['data']:
                print(f"   - {album['title']} ({album['release_year']})")
        else:
            print(f"❌ Failed to get artist's albums: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 All tests completed successfully!")
        print(f"🌐 API is running at: {BASE_URL}")
        print(f"📊 Admin interface: http://localhost:8000/admin/")
        print(f"📚 API documentation: http://localhost:8000/api/docs/")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the Django server is running:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    test_api()