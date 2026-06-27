# CyberNote - Cybersecurity Notes Application
**Student ID:** CIT-24-01-0408  
**Module:** CCS3308 - Virtualization and Containers

---

## Application Description
CyberNote is a cybersecurity-themed note-taking web application
built with Flask, PostgreSQL and Redis. Users can add, view,
search and delete notes organized by cybersecurity module categories.

---

## Deployment Requirements
- Docker
- Docker Compose

---

## Container List

| Container | Image | Role | Port |
|---|---|---|---|
| cybernote_flask | Custom (Python/Flask) | Web application | 5000 |
| cybernote_postgres | postgres:15 | Database (stores notes) | 5432 |
| cybernote_redis | redis:7 | Session cache (visit counter) | 6379 |

---

## Network and Volume Details
- **Network:** `cybernet` (bridge) — connects all 3 containers so they can communicate
- **Volume:** `pgdata` — stores PostgreSQL data permanently even after containers stop

---

## Container Configuration
- Flask connects to PostgreSQL and Redis using environment variables
- PostgreSQL stores notes in a persistent named volume
- Redis tracks page visit count in memory
- All containers restart automatically on failure
- Flask depends on PostgreSQL and Redis (starts after them)

---

## Instructions

### Prepare the application
```bash
./prepare-app.sh
```

### Start the application
```bash
./start-app.sh
```

### Stop the application (data is preserved)
```bash
./stop-app.sh
```

### Remove all resources
```bash
./remove-app.sh
```

### Access the application
Open your browser and go to:http://localhost:5000

---

## Example Workflow

```bash
# Create application resources
./prepare-app.sh
Preparing app...
Preparation complete!

# Run the application
./start-app.sh
Running app...
The app is available at http://localhost:5000

# Open browser at http://localhost:5000 and use the app

# Stop the application
./stop-app.sh
Stopping app...
App stopped. Your data is safe.

# Delete all application resources
./remove-app.sh
Removing app...
Removed app.
```

---

## Application Features
- Add notes with title, content and module category
- Search notes in real time
- Delete notes
- Page visit counter powered by Redis
- Notes stored permanently in PostgreSQL
