Container diagram
==================

.. image:: container.svg

.. mermaid::

    C4Container
        Enterprise_Boundary(b0, "Decision Modelling Process", "Process") {
            Person(person, "User", "A user of the Decision Model tool")
            Person(person2, "Decision Maker", "The decision maker of the project")
            Enterprise_Boundary(b1, "Decision Optimization Tool", "App") {
                System(system, "WebApp", "JavaScript", "The main interface of the users with the tool")
                System(system2, "API Application" , "FastAPI", "The backend provides the tool with all the needed services to run and connect to the database, \n and to connect the frontend to the backend")
                System(system3, "Database" , "TinkerPop GraphDB", "The database stores all the information of the projects")
            }
        }
        Rel(person, system, "Adds, edits, and visualizes the decision problem")
        BiRel(system, system2, "Send Requests and return responses")
        BiRel(system2, system3, "Store and retrieve data")
        Rel(person2, system, "View status and entered information of project approve steps")
        Rel(system, person2, "Provides basis for strucutured decision making")
