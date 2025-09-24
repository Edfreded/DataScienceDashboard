# Statistics Dashboard

A statistics dashboard created with Python and Dash, featuring a clean ETV (Extract, Transform, View) architecture.

## Architecture

### Containers

**Container 1: PostgreSQL**
- Holds your raw + cleaned dataset
- Exposes port 5432

**Container 2: Python (Dash app)**
- Installed: See Requirements.txt (plotly, dash, dash-bootstrap-components, pandas, sqlalchemy/psycopg2)
- Read from Datasets directory for datasets
- Connects to PostgreSQL for data (Planned)
- Exposes port 8050 (frontend)

### Code Structure (ETV Pattern)

**Extract**
- Module: `Extract` directory
- Handles DB connections
- Queries raw/cleaned tables from PostgreSQL
- Returns DataFrames

**Transform**
- Module: `Transform` directory
- Cleans, aggregates, reshapes data
- Produces chart-ready DataFrames (e.g., group by category, calculate KPIs, etc)

**View (Dash app)**
- Module: `Load` directory
- Imports transformed DataFrames
- Defines Dash layout (multipage setup)
- Uses Bootstrap components for styling
- Handles callbacks for interactivity (e.g., click → drill-down)

**Styling**
- Folder: `assets/` (optional for extra CSS)
- Bootstrap theme via dash-bootstrap-components
- Minimal custom CSS overrides if needed

## Setup

### Requirements
- Docker installed (manages the environment for dashboard app and database)
- Keeps everything isolated and clean
- Docker Hub recommended: https://hub.docker.com/welcome

### Running the App
```bash
# For the dashboard
docker compose up dashboard

# For the database
docker compose up db

# For both
docker compose up
```

## Workflow

Every flow is supervised by an **orchestrator** - this is where to start when creating a new dashboard.

1. Create a new Python file in the `Orchestrator/` directory
2. Define the Extract, Transform and Load scripts in their respective directories

### Extract
- Retrieval of the dataset
- Place in a single py file or split with clear naming scheme
- Currently data is loaded from files in the `Datasets/` directory locally

### Transform
- Altering the dataset - cleaning and modifications
- Can be done in the extract file if more convenient
- Transform step is most typical location

### Load
- Same as View in MVC - this is the dashboard
- May be a template that receives graphs and data, or it may graph data itself
- Styling, interaction and navigation are handled here

### Integration
- These 3 steps are called and linked together in the orchestrator
- Use parent-child naming conventions for easy reading
- Call the orchestrator in `App.py` main() method (entry point)

## Data Flow (Not yet implemented)
1. Data loaded into Postgres (raw → cleaned)
2. Extract queries tables
3. Transform prepares DataFrames
4. View presents multipage interactive dashboards with drill-down

## Development Notes

### Dependencies
- Extra dependencies can be installed directly into the docker container, but will not be shared or saved
- Add dependencies/imports to `Requirements.txt` so they're saved and picked up when containers are created by anyone

### Hot Reload
- **Code**: Hot reload is active - no need to restart environment with code changes
- **Datasets**: Not hot reloaded (for obvious reasons)
- Changes are picked up when saving files

## Benefits
- Clear separation of concerns (ETV)
- Scales well if datasets grow (Postgres handles heavy lifting)
- Professional frontend with Bootstrap
- Easy to dockerize, extend, or deploy