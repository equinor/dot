
.. _api_router:

API Router
##########


project.py
**********

Overview
--------

The `projects.py` module defines a set of RESTful API endpoints for managing project entities within a FastAPI application. It utilizes a `DatabaseClient` for database interactions, specifically tailored for operations on project data. The module is structured around the FastAPI `APIRouter`, facilitating CRUD operations on projects.

Dependencies
------------

- FastAPI: Used for creating the API routes.
- DatabaseClient: A client for database interactions, obtained through dependency injection.
- ProjectRepository: Repository class for handling project-specific database operations.
- Project, ProjectData, ProjectResponse: Pydantic models for request and response data validation.

API Endpoints
-------------

Create Project
~~~~~~~~~~~~~~

- Path: `/projects/create`
- Method: POST
- Description: Creates a new project entity based on the provided project data.
- Request Body: `ProjectData` (Pydantic model)
- Response: `ProjectResponse` (Pydantic model)

Read All Projects
~~~~~~~~~~~~~~~~~

- Path: `/projects/all`
- Method: GET
- Description: Retrieves a list of all project entities.
- Response: List of `ProjectResponse`

Read Project
~~~~~~~~~~~~

- Path: `/projects/read/{project_uuid}`
- Method: GET
- Description: Retrieves a single project entity based on its UUID.
- Path Parameter: `project_uuid` (string)
- Response: `ProjectResponse`

Update Project
~~~~~~~~~~~~~~

- Path: `/projects/update/{project_uuid}`
- Method: PATCH
- Description: Updates an existing project entity identified by its UUID with the provided project data.
- Path Parameter: `project_uuid` (string)
- Request Body: `ProjectData`
- Response: `ProjectResponse`


issues.py
*********

This module defines the API routes for managing issues within a project using FastAPI. It provides endpoints for creating new issues and retrieving issues associated with a specific project.

Dependencies
------------

- fastapi.APIRouter: Used to create route handlers.
- src.database.client.DatabaseClient: Represents the database client for executing database operations.
- src.database.gremlin.get_client: Dependency injection function to get a database client instance.
- src.repository.issue.IssueRepository: Repository class for issue-related database operations.
- src.models.issue: Contains the schema definitions for issues, including Issue, IssueData, and IssueResponse.
- src.models.filter.Filter: Schema for filtering issues.

API Endpoints
-------------

Create Issue
~~~~~~~~~~~~
- Path: `/issues/create`
- Method: POST
- Description: Creates a new issue vertex based on the provided issue data.
- Request Body: `IssueData` (Pydantic model)
- Response: `IssueResponse` (Pydantic model)

Read Issue
~~~~~~~~~~
- Path: `/issues/read/{issue_uuid}`
- Method: GET
- Description: Retrieves a single issue vertex based on its UUID.
- Path Parameter: `issue_uuid` (string)
- Response: `IssueResponse`

Read All Issues
~~~~~~~~~~~~~~~
- Path: `/issues/all/{project_uuid}`
- Method: GET
- Description: Retrieves a list of all issue vertex connected to a project.
- Path Parameter: `project_uuid` (string)
- Response: List of `IssueResponse`

Update Issue
~~~~~~~~~~~~
- Path: `/issues/update/{issue_uuid}`
- Method: PATCH
- Description: Updates an existing issue vertex identified by its UUID with the provided issue data.
- Path Parameter: `issue_uuid` (string)
- Request Body: `IssueData`
- Response: `IssueResponse`

Delete Issue
~~~~~~~~~~~~
- Path: `/issues/delete/{issue_uuid}`
- Method: DELETE
- Description: Deletes an issue vertex based on its UUID.
- Path Parameter: `issue_uuid` (string)

Merge Issues
~~~~~~~~~~~~
- Path: `/issues/merge`
- Method: POST
- Description: Merges two issues into a single issue.
- Request parameter: `project_uuid` (string): The UUID of the project.
- Request Body:
    - `source_issue` (IssueResponse): The source issue to be merged.
    - `destination_issue` (IssueResponse): The destination issue to merge into.
- Response: `IssueResponse`
