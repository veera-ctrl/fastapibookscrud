# FastAPI Angular PostgreSQL

A FastAPI backend with Angular frontend application.

## Docker Setup

### Prerequisites

- Docker installed on your machine
- Google Cloud SDK (gcloud CLI) installed
- A Google Cloud project with Cloud Run API enabled

### Building the Docker Image

```bash
# Build the Docker image
docker build -t fastapi-app .

# Run the container locally
docker run -p 8000:8000 fastapi-app
```

### Testing Locally

```bash
# Build and run with docker-compose (optional)
docker-compose up --build
```

## Deploying to Google Cloud Run

### Option 1: Using gcloud CLI

1. **Set your project:**

   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

2. **Enable required APIs:**

   ```bash
   gcloud services enable run.googleapis.com containerregistry.googleapis.com
   ```

3. **Authenticate Docker:**

   ```bash
   gcloud auth configure-docker
   ```

4. **Build and deploy:**

   ```bash
   # Build the image
   docker build -t gcr.io/YOUR_PROJECT_ID/fastapi-app .

   # Push to Container Registry
   docker push gcr.io/YOUR_PROJECT_ID/fastapi-app

   # Deploy to Cloud Run
   gcloud run deploy fastapi-app \
     --image gcr.io/YOUR_PROJECT_ID/fastapi-app \
     --region us-central1 \
     --platform managed \
     --allow-unauthenticated
   ```

### Option 2: Using Cloud Build

1. **Submit build to Cloud Build:**

   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

2. **Or trigger manually in Google Cloud Console:**
   - Go to Cloud Build > Triggers
   - Create a new trigger
   - Connect to your GitHub repository
   - Use `cloudbuild.yaml` as the configuration file

### Option 3: Using Terraform (Infrastructure as Code)

Create a `terraform` folder with:

```hcl
# main.tf
provider "google" {
  project = "YOUR_PROJECT_ID"
  region  = "us-central1"
}

resource "google_cloud_run_service" "fastapi" {
  name     = "fastapi-app"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/YOUR_PROJECT_ID/fastapi-app"
        ports {
          container_port = 8000
        }
        env {
          name  = "DATABASE_URL"
          value = "sqlite:///./books.db"
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "allUsers" {
  service  = google_cloud_run_service.fastapi.name
  location = google_cloud_run_service.fastapi.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
```

## Environment Variables

The following environment variables can be configured:

| Variable | Description | Default |
| --- | --- | --- |
| DATABASE_URL | SQLite database path | sqlite:///./books.db |
| PYTHONDONTWRITEBYTECODE | Disable .pyc files | 1 |
| PYTHONUNBUFFERED | Unbuffered output | 1 |

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | / | Get all books |
| GET | /all-books | Get all books (alternate) |
| GET | /books/{book_id} | Get a specific book |
| POST | /books/ | Create a new book |
| PUT | /books/{book_id} | Update a book |
| DELETE | /books/{book_id} | Delete a book |

## Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload

# Access API docs
# http://localhost:8000/docs
```

## Notes

- The application uses SQLite for data persistence
- In production (Cloud Run), data will be ephemeral unless you use Cloud Storage or Cloud SQL
- For production with persistent data, consider using Cloud SQL (PostgreSQL/MySQL)

