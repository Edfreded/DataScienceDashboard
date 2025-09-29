from shiny import App
from Load.Load_Test_1 import create_dashboard_ui, create_dashboard_server
from assets.theme_config import setup_plotly_theme, THEMES
from Config import ASSETS_PATH

def create_app():
    """Create and configure the Shiny app"""
    # Change this line to switch themes
    theme_name = 'retro'
    
    # Get theme configuration
    theme_config = THEMES[theme_name]
    
    # Set up theme
    setup_plotly_theme(theme_config['plotly_theme'])
    app_ui = create_dashboard_ui(css_file=theme_config['css_file'])
    app_server = create_dashboard_server()
    
    return App(app_ui, app_server, static_assets=ASSETS_PATH)

def main():
    """Main entry point"""
    app = create_app()
    
    print("🚀 Starting Car Sales Dashboard with dark_blue theme")
    print("📊 Access the dashboard at: http://localhost:8000")
    
    app.run(host='0.0.0.0', port=8000)

# For hot reload mode (used by shiny CLI in Docker)
app = create_app()

if __name__ == "__main__":
    main()