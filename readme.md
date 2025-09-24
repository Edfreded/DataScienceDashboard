setup:
    requirements:
        make sure to have docker installed, this manages the environment for the dashboard app and the database. It keeps everything belonging to this app isolated and clean
        dockerhub is recommended:
            https://hub.docker.com/welcome
    
    running the app            
        for the dashboard, run "docker compose up -Dashboard" 
        for the db, run "docker compose up -Dashboard"



workflow
Every flow is supervised by an orchestator, this is where to start when creation a new dashboard. Simply create a new python file in the Orchestrator directory and define the Extract, Transform and Load scripts.

    The Extract is the retrieval of the dataset, place this in a single py file or split it up with a clear naming scheme that indicates the parent flow.
    Currently data is loaded from files in the Datasets directory you have localy. 

    The Transform is mainly for altering the dataset. this can be any cleaning and modificating as you wish. it can also be done in the extract file, whatever is most convenient. Inside the transform step is most typical

    The Load is the same as View in MVC here, this is the dashboard. the dashboard may or may not be a template that you pass graphs and data, or it may graph data itself. again, what you prefer.
    Styling, interaction and navigation are done here aswell. 

These 3 steps are called and linked together in the orchestrator to keep things clean. make sure to use parent-child naming conventions for easy reading and avoiding confusion

lastly, make sure to call the orchestrator in App.py main() method. This is the entry point for the app



Note:

any extra dependencies can be installed into the docker container directly but will not be shared across the rest of the group. add dependencies/ imports to the Requrements.txt file so they are picked up when a container is created by anyone

Hot reload is active for code, meaning you dont have to restart the environment with code changes, it should be picked up when saving a file. The datasets are not hot reloaded for obvious reasons