API Schema Documentation
==========================

Introduction
------------

This documentation provides an overview of the schema files used in the API module of our project. The schema files define the structure and validation rules for the data exchanged between different components of the API.

File Structure
--------------

The schema files are located in the `api/src/models` directory. Each schema file represents a specific data entity or resource and is named accordingly.

.. code-block:: bash

    api/src/models/
    ├── vertex.py
    ├── edge.py
    └── ...

Usage
-----

To use a schema file, follow these steps:

1. Import the schema file in your code:

    .. code-block:: python

        from api.src.models.vertex import VertexData

2. Validate data against the schema:

    .. code-block:: python

        def validate_vertex(vertex_data):
             try:
                  VertexData.validate(vertex_data)
                  print("Vertex data is valid.")
             except ValidationError as e:
                  print("Vertex data is invalid. Error details:")
                  print(e)


Schema Definitions
------------------

Below are the details of each schema file:
