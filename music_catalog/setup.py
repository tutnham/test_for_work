#!/usr/bin/env python
"""
Setup script for Music Catalog API.
This script helps with initial project setup and database initialization.
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def setup_django():
    """Setup Django environment."""
    print("🔧 Setting up Django environment...")
    
    # Add project directory to Python path
    project_dir = Path(__file__).parent
    sys.path.insert(0, str(project_dir))
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
    
    # Setup Django
    django.setup()
    print("✅ Django environment setup completed")

def create_superuser():
    """Create a superuser for Django admin."""
    print("\n👤 Creating superuser for Django admin...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superuser already exists")
            return True
        
        # Create superuser
        username = input("Enter username for superuser (default: admin): ").strip() or "admin"
        email = input("Enter email for superuser (optional): ").strip() or ""
        password = input("Enter password for superuser: ").strip()
        
        if not password:
            print("❌ Password is required")
            return False
        
        User.objects.create_superuser(username, email, password)
        print(f"✅ Superuser '{username}' created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create superuser: {e}")
        return False

def create_sample_data():
    """Create sample data for testing."""
    print("\n📝 Creating sample data...")
    
    try:
        from music.models import Artist, Song, Album, AlbumSong
        
        # Create sample artist
        artist, created = Artist.objects.get_or_create(
            name="The Beatles",
            defaults={'name': "The Beatles"}
        )
        if created:
            print(f"✅ Created artist: {artist.name}")
        else:
            print(f"ℹ️  Artist already exists: {artist.name}")
        
        # Create sample songs
        songs_data = [
            "Hey Jude",
            "Let It Be", 
            "Yesterday",
            "Come Together",
            "Here Comes the Sun"
        ]
        
        songs = []
        for title in songs_data:
            song, created = Song.objects.get_or_create(
                title=title,
                defaults={'title': title}
            )
            songs.append(song)
            if created:
                print(f"✅ Created song: {song.title}")
            else:
                print(f"ℹ️  Song already exists: {song.title}")
        
        # Create sample album
        album, created = Album.objects.get_or_create(
            title="Abbey Road",
            artist=artist,
            defaults={
                'title': "Abbey Road",
                'artist': artist,
                'release_year': 1969
            }
        )
        if created:
            print(f"✅ Created album: {album.title}")
        else:
            print(f"ℹ️  Album already exists: {album.title}")
        
        # Add tracks to album
        for i, song in enumerate(songs[:3], 1):  # Add first 3 songs
            album_song, created = AlbumSong.objects.get_or_create(
                album=album,
                song=song,
                defaults={
                    'album': album,
                    'song': song,
                    'track_number': i
                }
            )
            if created:
                print(f"✅ Added track {i}: {song.title}")
            else:
                print(f"ℹ️  Track already exists: {song.title}")
        
        print("✅ Sample data creation completed")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create sample data: {e}")
        return False

def main():
    """Main setup function."""
    print("🎵 Music Catalog API Setup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("❌ Please run this script from the music_catalog directory")
        return
    
    # Setup Django
    setup_django()
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        return
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        return
    
    # Create superuser
    create_superuser()
    
    # Create sample data
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the development server:")
    print("   python manage.py runserver")
    print("\n2. Access the admin interface:")
    print("   http://localhost:8000/admin/")
    print("\n3. Access the API:")
    print("   http://localhost:8000/api/v1/")
    print("\n4. View API documentation:")
    print("   http://localhost:8000/api/docs/")
    print("\n5. Run the test script:")
    print("   python test_api.py")

if __name__ == "__main__":
    main()