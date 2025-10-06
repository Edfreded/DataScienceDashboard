from shiny import App
from Load.Load_Test_1 import create_dashboard_ui, create_dashboard_server
from assets.theme_utils import get_theme_css_file, setup_plotly_colors
from Config import ASSETS_PATH

def create_app():
    """Create and configure the Shiny app"""
    # Change this line to switch themes: 'retro', 'light', 'default', 'dark_blue', 'dark'
    theme_name = 'dark'
    
    # Get theme CSS file and set up Plotly colors
    css_file = get_theme_css_file(theme_name)
    setup_plotly_colors(theme_name)
    
    # Create app with theme
    app_ui = create_dashboard_ui(css_file=css_file)
    app_server = create_dashboard_server()
    
    return App(app_ui, app_server, static_assets=ASSETS_PATH)

def main():
    """Main entry point"""
    app = create_app()
    
    print("🚀 Starting Dashboard")
    print("📊 Access the dashboard at: http://localhost:8000")
    
    app.run(host='0.0.0.0', port=8000)

# For hot reload mode (used by shiny CLI in Docker)
app = create_app()

if __name__ == "__main__":
    main()