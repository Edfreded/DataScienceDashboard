from shiny import App
from Load.Load_Test_1 import create_dashboard_ui, create_dashboard_server
from assets.theme_config import setup_retro_plotly_theme, THEME_CONFIG
from Config import ASSETS_PATH

def create_app():
    """Create and configure the Shiny app"""
    # Set up the Plotly theme
    setup_retro_plotly_theme()
    
    # Create the app with theme configuration
    app_ui = create_dashboard_ui(css_file=THEME_CONFIG['css_file'])
    app_server = create_dashboard_server()
    
    return App(app_ui, app_server, static_assets=ASSETS_PATH)

def main():
    """Main entry point for Docker"""
    app = create_app()
    print("🚀 Starting Car Sales Dashboard")
    print("📊 Access the dashboard at: http://localhost:8000")
    app.run(host='0.0.0.0', port=8000)

# For hot reload mode (used by shiny CLI in Docker)
app = create_app()

# Autorun
if __name__ == "__main__":
    main()