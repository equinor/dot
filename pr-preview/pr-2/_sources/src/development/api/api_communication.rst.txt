API flowchart
*************

This flowchart provides an overview of the communication between the different modules in our project. It outlines the main components and interactions involved in handling API requests and responses.

.. mermaid::
    :caption: API communication flowchart

    sequenceDiagram
        participant Frontend
        participant Router
        participant Repository
        participant Vertex- & Edge Repository
        participant Schema
        participant Database
        Frontend->>Router: Send API request
        Router->>Repository: Call specific repository methods
        Repository->>Vertex- & Edge Repository: Call vertex and edge methods
        Vertex- & Edge Repository->>Database: Execute Gremlin queries
        Database->>Vertex- & Edge Repository: Return query results
        Vertex- & Edge Repository-->>Schema: Validate data
        Vertex- & Edge Repository->>Repository: Return data as VertexResponse or EdgeResponse
        Repository-->>Schema: Validate data
        Repository->>Router: Return ResponseModel
        Router->>Frontend: Send API response
