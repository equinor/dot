.. _fullstack:

The full stack
##############

.. important:: The software is currently under development; please expect changes.


The tool is implemented as a full stack with both the :ref:`frontend <frontend>` and the :ref:`backend <backend>` developed simultaneously, although using different directories.


.. mermaid::
   :caption: the full stack aggregated by the frontend and the backend

    flowchart LR
        subgraph frontend[fa:fa-users frontend]
            ui[fa:fa-keyboard ui]
        end
        ui --> api
        subgraph backend[fa:fa-server backend]
            api[fa:fa-gears api] --> db[fa:fa-database db]
            lib[fa:fa-book lib] <--> api
        end


The tool is developed as a monorepo and it is version controlled using git through GitHub in the `dot repository <https://github.com/equinor/dot>`_.
The intention is to fragment this repository in different repositories in the future.

The stack is controlled using `Docker compose file <https://github.com/equinor/dot/blob/main/docker-compose.yaml>`_ that runs each application using a specific container (`frontend.Dockerfile <https://github.com/equinor/dot/blob/main/frontend.Dockerfile>`_, `backend.Dockerfile <https://github.com/equinor/dot/blob/main/backend.Dockerfile>`_, and `database.Dockerfile <https://github.com/equinor/dot/blob/main/database.Dockerfile>`_).


.. _frontend:

The frontend
************

The frontend is the main interface of the users with the tool.
It includes the :ref:`UI <ui>` and its related components.
This UI allows users to create Decision Model projects and follow
the iterative and step-by-step process of building quality decisions.
Information is directly read from the database and new pieces of
information is directly stored in the database.

.. warning::
    The current version focuses only on the framing, editing of the
    influence diagram and visualization of the equivalent symmetric
    decision tree.



.. _ui:

The User Interface (UI)
=======================

The UI is mainly implemented using `React <https://react.dev/>`_ and `Equinor Design System (EDS) <https://github.com/equinor/design-system>`_.
The detailed list of dependencies used to build the UI is present in the file `package.json <https://github.com/equinor/dot/blob/main/web/package.json>`_.


.. _backend:

The backend
***********

The backend provides the tool with all the needed services to run and connect to the :ref:`database <database>`, and to connect the :ref:`frontend <frontend>` to the :ref:`backend <database>`.
It includes the :ref:`library <library>`, the :ref:`database <database>` and the :ref:`api <api>`.


.. _library:

The library
===========

The library collects the implementation of all the relevant Decision Quality (DQ) (TODO: links) methods for the tool.
The library will be developed independently than the services needed to have the :ref:`fullstack <fullstack>` available for users, although it is crucial for the application.
The role of the library is to convert information from the database to objects which can be easily manipulated and eventually converted to external package formats.
This allows testing different existing methodologies for analysis and evaluation of the decision model.

The library is written in python.


.. warning::
    The current version allows only symmetric problems.

.. warning::
    The current approach is to convert the influence diagram to either `pyAgrum <https://pyagrum.readthedocs.io/en/latest/>`_
    or `pycid <https://github.com/causalincentives/pycid/tree/master/notebooks>`_ and use those tools to evaluate the decision model.



.. _database:

The database
============

The database consists of a graph-based database implementation provided by `Apache TinkerPop™ <https://tinkerpop.apache.org/index.html>`_ and using the `Gremlin <https://tinkerpop.apache.org/gremlin.html>`_ graph traversal language.
The decision models of the tool are structured using graphs (TODO: link), so the choice for a graph-based database seemed natural.

To account for a native and cloud first solution, we aim to server our databases using the available solution in Azure CosmosDB.
Until decided otherwise, we will provide support for both types of servers.


.. _api:

The API
=========

The API is mainly implemented using `FastAPI <https://fastapi.tiangolo.com/>`_.
The detailed list of dependencies used to build the API is present in the file `pyproject.toml <https://github.com/equinor/dot/blob/main/api/pyproject.toml>`_.

The API consists of several services to implement a `CRUD (Create, read, update and delete) <https://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`_ interface with the graph database.
The access to the database is abstracted using a repository pattern layer for the vertices (``VertexRepository``) and edges (``EdgeRepository``) in the graph database.
This is further specialized for the project (``ProjectRepository``), objectives (``ObjectivesRepository``), opportunities (``OpportunityRepository``), issues (``IssueRepository``), and structures (``StructureRepository``).
