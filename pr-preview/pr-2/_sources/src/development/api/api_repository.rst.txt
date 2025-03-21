.. _repository:

The API repositories
********************

The API repositories are the main interface with the database. They are used to interact with the database and to perform CRUD operations on the different entities. The repositories are used by the FastAPI routers to handle the different requests.
The repositories are structured around the `DatabaseClient` class, which is a client for database interactions. The `DatabaseClient` class is obtained through dependency injection and is used to perform operations on the database.
The repositories are also dependent on the Pydantic models for request and response data validation. These models are used to validate the data before interacting with the database.

*graph.py* repository
======================
The *graph.py* repository contains a class `VertexRepository` and `EdgeRepository` that are responsible for handling graph-specific database operations. Both classes create and execute queries on the database based on the given input from the other repositories.
The `VertexRepository` class is used to handle operations on the vertices of the graph, while the `EdgeRepository` class is used to handle operations on the edges of the graph.

VertexRepository
----------------

The `VertexRepository` class has the following methods:

- `create`: Creates a new node/vertex in the database with the provided label and properties. The query to add a new vertex will be created based on the `VertexData` and is generic for different types of nodes which are identified through different labels. This function will return the created vertex as a `VertexResponse`.
    The used labels are:
        - *project*
        - *objective*
        - *opportunity*
        - *issue*
- `all`: Retrieves a list of all nodes/vertices with a specific label and a filter dictionary `filter_dict`. This function will return a list of `VertexResponse` objects.
- `read`: Retrieves a single node/vertex based on its UUID. This function will return a `VertexResponse` object.
- `update`: Modifies an existing node/vertex in the database by updating its properties with the provided `vertex_prop` as `VertexData` model. This function will return the updated vertex as a `VertexResponse`.
- `delete`: Deletes a node/vertex based on its UUID.
- `read_out_vertex`: Retrieves outgoing vertices based on edge label and filter of a specific vertex based on its UUID. This function will return a list of `VertexResponse` objects.

EdgeRepository
--------------

The `EdgeRepository` class has the following methods:

- `all_from_project`: Retrieves all edges from a project node based on the project UUID and the edge label. This function will return a list of `EdgeResponse` objects.
- `create`: Creates a new edge in the database with the provided label between two vertices. This function will return the created edge as an `EdgeResponse`.
- `read_out_edge_from_vertex`: Retrieves outgoing edges based on edge label from a vertex. This function will return a list of `EdgeResponse` objects.
- `read_in_edge_from_vertex`: Retrieves incoming edges based on edge label from a vertex. This function will return a list of `EdgeResponse` objects.
- `read`: Retrieves a single edge based on the edge UUID. This function will return an `EdgeResponse` object.
- `update`: Modifies an existing edge in the database by updating its properties with the provided `edge_prop` as dictionary. This function will return the updated edge as an `EdgeResponse`.
- `delete`: Deletes an edge based on its edge UUID.
- `delete_edge_from_vertex`: Deletes all edges going in and out of a specified vertex based on the vertex UUID.




*project.py* repository
=========================

The *project.py* repository contains a class `ProjectRepository` that is responsible for handling project-specific database operations.
The repository provides methods for creating, reading, updating, and deleting project entities in the database. It utilizes the `DatabaseClient` for database interactions and the Pydantic models for data validation.
The `ProjectRepository` calls methods of the `VertexRepository` which will create and execute the Gremlin queries to the database.

The `ProjectRepository` class has the following methods:

- `create`: Creates a new node/vertex in the database with the label "project". The properties of the node are assigned based on the provided *project_data* of a pydantic model *ProjectData*. This function will return a *ProjectResponse* object with the created project
- `all`: Retrieves a list of all project nodes. This function will return a list of *ProjectResponse* objects.
- `read`: Retrieves a single project node based on its UUID. This function will return a *ProjectResponse* object.
- `update`: Modifies an existing project node in the database by updating its properties with the provided *project_data*, which is a pydantic model *ProjectData*.
- `delete`: Deletes a project node based on its UUID.
