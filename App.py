from Orchestrator.Orchestrator_Test_1 import orchestrator_test_1

def main():
    # place orchestrator here
    app = orchestrator_test_1()

    # Run the app
    print("Access the dashboard at: http://localhost:8050")
    app.run(host='0.0.0.0', port=8050, debug=True)


# Autorun
if __name__ == "__main__":
    main()