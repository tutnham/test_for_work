# Music Catalog API

A robust and scalable RESTful API built with Django REST Framework for managing a music catalog with artists, albums, and songs. The API supports the complex relationship where a single song can appear in multiple albums with different track numbers.

## Features

- **Complete CRUD Operations**: Full Create, Read, Update, Delete operations for all entities
- **Complex Relationships**: Support for songs appearing in multiple albums with different track numbers
- **RESTful Design**: Follows REST principles with proper HTTP methods and status codes
- **Comprehensive Validation**: Model-level and serializer-level validation with custom validators
- **Django Admin Integration**: Full admin interface in Russian for easy data management
- **JWT Authentication**: Secure token-based authentication
- **Filtering & Search**: Advanced filtering, searching, and ordering capabilities
- **Pagination**: Standardized pagination across all list endpoints
- **Error Handling**: Unified error response format with proper HTTP status codes
- **Internationalization**: Russian language support throughout the application
- **Performance Optimized**: Query optimization with select_related and prefetch_related

## Project Structure

```
music_catalog/
├── config/                 # Project configuration
│   ├── settings/          # Django settings
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── core/                  # Core utilities
│   ├── responses.py      # Unified response structures
│   ├── pagination.py     # Custom pagination classes
│   ├── exceptions.py     # Custom exception handler
│   └── validators.py     # Reusable validators
├── music/                # Music app
│   ├── models.py         # Database models
│   ├── serializers.py    # DRF serializers
│   ├── views.py          # ViewSets
│   ├── admin.py          # Django admin configuration
│   └── urls.py           # App URL configuration
├── api/                  # API structure
│   └── v1/              # API version 1
│       └── urls.py      # API URL configuration
├── static/              # Static files
├── templates/           # Templates
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Data Models

### Artist
- `name` (CharField): Artist/band name (unique)
- `created_at`, `updated_at`: Timestamps

### Album
- `title` (CharField): Album title
- `artist` (ForeignKey): Reference to Artist
- `release_year` (IntegerField): Year of release (validated)
- `songs` (ManyToManyField): Songs through AlbumSong
- `created_at`, `updated_at`: Timestamps

### Song
- `title` (CharField): Song title
- `created_at`, `updated_at`: Timestamps

### AlbumSong (Through Model)
- `album` (ForeignKey): Reference to Album
- `song` (ForeignKey): Reference to Song
- `track_number` (PositiveSmallIntegerField): Track number in album
- `created_at`, `updated_at`: Timestamps

**Unique Constraints:**
- No duplicate track numbers within an album
- No duplicate songs in the same album
- Same song can appear in different albums with different track numbers

## API Endpoints

### Artists
- `GET /api/v1/artists/` - List all artists
- `POST /api/v1/artists/` - Create a new artist
- `GET /api/v1/artists/{id}/` - Retrieve specific artist
- `PUT /api/v1/artists/{id}/` - Update artist
- `PATCH /api/v1/artists/{id}/` - Partial update artist
- `DELETE /api/v1/artists/{id}/` - Delete artist
- `GET /api/v1/artists/{id}/albums/` - Get artist's albums
- `GET /api/v1/artists/popular/` - Get popular artists

### Albums
- `GET /api/v1/albums/` - List all albums
- `POST /api/v1/albums/` - Create a new album
- `GET /api/v1/albums/{id}/` - Retrieve specific album
- `PUT /api/v1/albums/{id}/` - Update album
- `PATCH /api/v1/albums/{id}/` - Partial update album
- `DELETE /api/v1/albums/{id}/` - Delete album
- `GET /api/v1/albums/{id}/tracks/` - Get album tracks
- `GET /api/v1/albums/recent/` - Get recent albums
- `GET /api/v1/albums/by_year/` - Get albums by year

### Songs
- `GET /api/v1/songs/` - List all songs
- `POST /api/v1/songs/` - Create a new song
- `GET /api/v1/songs/{id}/` - Retrieve specific song
- `PUT /api/v1/songs/{id}/` - Update song
- `PATCH /api/v1/songs/{id}/` - Partial update song
- `DELETE /api/v1/songs/{id}/` - Delete song
- `GET /api/v1/songs/{id}/albums/` - Get albums containing song
- `GET /api/v1/songs/popular/` - Get popular songs
- `GET /api/v1/songs/search/` - Search songs

### Authentication
- `POST /api/v1/auth/token/` - Obtain JWT token
- `POST /api/v1/auth/token/refresh/` - Refresh JWT token
- `POST /api/v1/auth/token/verify/` - Verify JWT token

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd music_catalog
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

## Usage Examples

### Creating an Artist
```bash
curl -X POST http://localhost:8000/api/v1/artists/ \
  -H "Content-Type: application/json" \
  -d '{"name": "The Beatles"}'
```

### Creating a Song
```bash
curl -X POST http://localhost:8000/api/v1/songs/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Hey Jude"}'
```

### Creating an Album with Tracks
```bash
curl -X POST http://localhost:8000/api/v1/albums/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Abbey Road",
    "artist_id": 1,
    "release_year": 1969,
    "tracks": [
      {"song_id": 1, "track_number": 1},
      {"song_id": 2, "track_number": 2}
    ]
  }'
```

### Getting Album Details with Tracks
```bash
curl -X GET http://localhost:8000/api/v1/albums/1/
```

### Filtering Albums by Artist
```bash
curl -X GET "http://localhost:8000/api/v1/albums/?artist=1"
```

### Searching Songs
```bash
curl -X GET "http://localhost:8000/api/v1/songs/search/?q=Hey"
```

## Django Admin

Access the Django admin interface at `http://localhost:8000/admin/` to manage:

- **Artists**: Add, edit, and delete artists
- **Songs**: Manage song catalog
- **Albums**: Create albums with inline track management
- **Album Songs**: Direct management of track relationships

The admin interface is fully translated to Russian and provides an intuitive way to manage the music catalog.

## API Response Format

### Success Response
```json
{
  "success": true,
  "message": "Success",
  "data": {
    // Response data here
  },
  "pagination": {
    "count": 100,
    "next": "http://localhost:8000/api/v1/albums/?page=2",
    "previous": null,
    "current_page": 1,
    "total_pages": 5,
    "page_size": 20
  }
}
```

### Error Response
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "field_name": ["Specific error details"]
  },
  "error_code": "VALIDATION_ERROR"
}
```

## Validation Rules

### Artist
- Name must be 2-200 characters
- Name must be unique

### Album
- Title must be 1-200 characters
- Release year cannot be in the future
- Artist must exist

### Song
- Title must be 1-200 characters

### AlbumSong (Track)
- Track number must be 1-999
- No duplicate track numbers within an album
- No duplicate songs in the same album
- Same song can appear in different albums

## Testing

Run the test suite:

```bash
python manage.py test
```

## Deployment

### Production Settings

1. Set environment variables:
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```

2. Use production settings:
   ```bash
   export DJANGO_SETTINGS_MODULE=config.settings.production
   ```

3. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

4. Use a production WSGI server like Gunicorn:
   ```bash
   gunicorn config.wsgi:application
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions, please open an issue in the repository.