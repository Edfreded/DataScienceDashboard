# Statistics Dashboard Project Context

## Project Overview
This is a Python-based statistics dashboard built with **Shiny for Python** and **Plotly** for interactive data visualization. The project follows a clean **ETV (Extract, Transform, View)** architecture pattern and is containerized with Docker for easy deployment.

## Core Technologies
- **Frontend**: Shiny for Python (reactive web framework)
- **Visualization**: Plotly (interactive charts and maps)
- **Data Processing**: Pandas, NumPy
- **Database**: PostgreSQL (planned, currently using CSV files)
- **Containerization**: Docker & Docker Compose
- **Styling**: Custom CSS themes with multiple options

## Architecture Pattern: ETV (Extract, Transform, View)

### 1. Extract (`Extract/` directory)
- **Purpose**: Data retrieval and initial loading
- **Current Implementation**: Loads CSV files from `Datasets/` directory
- **Future**: Will connect to PostgreSQL database
- **Key File**: `Extract_PWT.py` - loads Penn World Table dataset

### 2. Transform (`Transform/` directory)
- **Purpose**: Data cleaning, processing, and preparation
- **Functions**:
  - `clean_and_transform_data()`: Creates calculated fields (GDP per capita, growth rates, net exports)
  - `create_summary_stats()`: Generates dashboard statistics and metadata
- **Key File**: `Transform_PWT.py`

### 3. View/Load (`Load/` directory)
- **Purpose**: Dashboard UI and server logic (equivalent to MVC's View + Controller)
- **Structure**:
  - `UI/Layouts/`: Page layouts and structure
  - `UI/Components/`: Reusable UI components (cards, rows, containers)
  - `Server/`: Reactive server functions and data binding
- **Key Files**: 
  - `Load_PWT.py`: Main entry point
  - `UI/Layouts/Layout_PWT.py`: Dashboard layout
  - `Server/Server_PWT.py`: Server-side reactive logic

## Orchestration Pattern

### Orchestrator (`Orchestrator/` directory)
- **Purpose**: Coordinates the entire ETV pipeline
- **Pattern**: Each dashboard has its own orchestrator function
- **Key Function**: `orchestrator_PWT()` in `Orchestrator_PWT.py`

**Flow**:
```python
def orchestrator_PWT(css_file=None):
    # 1. Extract
    raw_data = extract_PWT()
    
    # 2. Transform  
    cleaned_data = clean_and_transform_data(raw_data)
    summary_stats = create_summary_stats(cleaned_data)
    
    # 3. View/Load
    app_ui = create_dashboard_ui(css_file=css_file)
    app_server = create_dashboard_server(cleaned_data, summary_stats)
    
    # 4. Return Shiny App
    return App(app_ui, app_server, static_assets=ASSETS_PATH)
```

## Dashboard Components

### Current Dashboard: Penn World Table (PWT)
**Data Source**: Economic indicators from Penn World Table dataset
**Visualizations**:
- **Stat Cards**: Total countries, latest year, average GDP, richest country
- **World Maps**: GDP per capita and GDP growth rate (choropleth with year selector)
- **Bar Chart**: Top 5 countries by GDP per capita
- **Line Chart**: Global GDP trend over time

### UI Component Structure
- **Cards**: Stat cards and chart containers
- **Rows**: Layout system for responsive design
- **Containers**: Wrapper components for styling

## Theming System

### Theme Architecture (`assets/` directory)
- **CSS Themes**: Multiple themes available (retro, light, dark, dark_blue, test1)
- **Plotly Integration**: Automatic color palette matching
- **Configuration**: `theme_config.py` and `theme_utils.py`
- **Theme Selection**: Set in `shiny_app.py` via `theme_name` variable

### Available Themes
- `default`: Standard theme
- `retro`: Retro-styled theme  
- `light`: Light color scheme
- `dark`: Dark theme
- `dark_blue`: Dark blue variant
- `test1`: Custom test theme

## Data Flow

### Current Implementation
1. **CSV Loading**: Data loaded from `Datasets/pwt110_cleaned.csv`
2. **Processing**: GDP calculations, growth rates, data cleaning
3. **Reactive Updates**: Shiny reactive functions update visualizations
4. **Interactive Features**: Year selectors on maps, hover tooltips

### Planned Database Integration
1. **PostgreSQL**: Raw and cleaned data storage
2. **Extract Layer**: Database queries instead of CSV loading
3. **Scalability**: Handle larger datasets efficiently

## Development Environment

### Docker Setup
- **Container 1**: PostgreSQL database (port 5432)
- **Container 2**: Python Shiny app (port 8000)
- **Hot Reload**: Code changes automatically reflected
- **Commands**:
  - `docker compose up` - Start both containers
  - `docker compose up dashboard` - Dashboard only
  - `docker compose up db` - Database only

### Project Structure
```
├── Extract/           # Data extraction modules
├── Transform/         # Data transformation modules  
├── Load/             # Dashboard UI and server
│   ├── UI/           # User interface components
│   └── Server/       # Server-side logic
├── Orchestrator/     # Pipeline coordination
├── Datasets/         # Data files
├── assets/           # Themes and static assets
├── Config.py         # Configuration settings
├── shiny_app.py      # Main application entry
└── Requirements.txt  # Python dependencies
```

## Key Dependencies
- `shiny`: Web framework
- `plotly`: Interactive visualizations
- `pandas`: Data manipulation
- `shinywidgets`: Enhanced UI components
- `sqlalchemy`, `psycopg2-binary`: Database connectivity (planned)

## Development Patterns

### Adding New Dashboards
1. Create orchestrator in `Orchestrator/Orchestrator_[NAME].py`
2. Implement Extract, Transform, Load modules
3. Update `shiny_app.py` to call new orchestrator
4. Follow naming convention: `[Module]_[Dataset].py`

### Reactive Programming
- Use `@reactive.calc` for computed values
- Use `@output` and `@render.*` for UI updates
- Data flows reactively through the application

### Styling Guidelines
- CSS classes follow dashboard-specific naming
- Plotly charts automatically inherit theme colors
- Responsive design using row/column system

## Current Status
- ✅ ETV architecture implemented
- ✅ PWT dashboard functional
- ✅ Multiple theme support
- ✅ Docker containerization
- ✅ Interactive Plotly visualizations
- 🔄 PostgreSQL integration (planned)
- 🔄 Additional datasets (planned)

This context should help AI assistants understand the project's architecture, patterns, and current implementation when working on future enhancements or debugging.