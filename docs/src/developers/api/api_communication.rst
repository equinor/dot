API flowchart
*************

This flowchart provides an overview of the communication between the different modules in our project. It outlines the main components and interactions involved in handling API requests and responses.

.. mermaid::
    :caption: API communication flowchart

    sequenceDiagram
        participant Frontend
        participant Route
        participant Service
        participant Repository
        participant Vertex- & Edge Repository
        participant Data model
        participant Database
        Frontend->>Route: Send API request
        Route->>Service: Call specific service methods
        Service->>Repository: Call specific repository methods
        Repository->>Vertex- & Edge Repository: Call vertex and edge methods
        Vertex- & Edge Repository->>Database: Execute Gremlin queries
        Database->>Vertex- & Edge Repository: Return query results
        Vertex- & Edge Repository-->>Data model: Validate data
        Vertex- & Edge Repository->>Repository: Return data as VertexResponse or EdgeResponse
        Repository-->>Data model: Validate data
        Service->>Route: Return ResponseModel
        Route->>Frontend: Send API response
