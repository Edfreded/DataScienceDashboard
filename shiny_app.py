from shiny import App
from Orchestrator.Orchestrator_Test_1 import orchestrator_test_1
from assets.theme_utils import get_theme_css_file, setup_plotly_colors

def create_app():
    # Change this line to switch themes: 'retro', 'light', 'default', 'dark_blue', 'dark', 'test1'
    theme_name = 'test1'
    
    # Get theme CSS file and set up Plotly colors
    css_file = get_theme_css_file(theme_name)
    setup_plotly_colors(theme_name)
    
    # Create Shiny app
    app = orchestrator_test_1(css_file=css_file)
    
    return app

def main():
    app = create_app()
    
    print("🚀 Starting Dashboard")
    print("📊 Access the dashboard at: http://localhost:8000")
    
    app.run(host='0.0.0.0', port=8000)

# For hot reload mode (used by shiny CLI in Docker)
app = create_app()

if __name__ == "__main__":
    main()