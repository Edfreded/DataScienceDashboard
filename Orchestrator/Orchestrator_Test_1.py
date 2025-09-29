from shiny_app import create_app

def orchestrator_test_1():
    """
    Main orchestrator for the car sales dashboard
    Coordinates Extract, Transform, and Load operations
    """
    print("Starting Car Sales Dashboard Orchestrator...")
    print("Step 3: Creating dashboard...")
    
    app = create_app()
    print("Dashboard ready! Starting server...")

    return app