# Safetify (Django + DRF + PostGIS)

Safetify is a Django project that recording incidents, finding nearby technicians, and assigning the nearest available one.

## Features
- Create incidents with coordinates & severity
- Auto-calculated risk score (simple severity-based logic)
- Filter incidents by `status` or bounding box
- Find nearby available technicians
- Assign nearest available technician
- Dockerized with PostGIS & Redis
- Tested with pytest
---

## Quickstart

### Clone & Install
```bash
git clone https://github.com/imiebaka/safetify.git
cd safetify
```
### Environment
Copy .env.example to .env if you have environment variables (optional).

### Run with Docker
```bash
docker-compose up --build
```
This starts:
web — Django app on port 8000
db — PostgreSQL + PostGIS
redis — Redis server
worker — Celery background worker

### API Endpoints
Create Incident
```bash
curl -X POST http://localhost:8000/api/incidents/ \
-H "Content-Type: application/json" \
-d '{"title":"Power Outage","severity":3,"location":[3.3792,6.5244]}'
```

List Incidents (status filter)
```bash
GET /api/incidents/?status=queued
```
List Incidents (bbox filter)
```bash
GET /api/incidents/?bbox=minLon,minLat,maxLon,maxLat
```

Find Nearby Technicians
```bash
GET /api/technicians/nearby?lon=3.3792&lat=6.5244&radius=5000
```
Assign Nearest Technician
```bash
POST /api/incidents/{id}/assign-nearest
```

### Development

Install dependencies (if not using Docker)
```bash
pip install -r requirements.txt
```
requirements.txt
Django
djangorestframework
django-filter
psycopg[binary]
celery
redis
pytest
pytest-django

Note: You’ll need system packages for GeoDjango (GDAL/GEOS/Proj):

sudo apt-get install binutils libproj-dev gdal-bin

Run Migrations
docker-compose exec web python manage.py migrate

Seed Technicians
docker-compose exec web python manage.py seed_technicians

Seed Technicians
docker-compose exec web python manage.py seed_incident

Run Tests
docker-compose exec web pytest -q
