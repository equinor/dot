.. _database_overview:


This documentation provides an insight into the database structure of the Decision Model Tool and its elements.

Visual representation
*********************

Here is a visual representation of the database. The database can have several `Project` vertices which might not be connected through edges.

.. mermaid::
    :caption: Database Overview

    graph TD
        A[Project 1] --> |contains| B[Issue A1];
        A -->|contains| C[Issue A2];
        A -->|contains| D[Issue A3];
        D -->|influences| C;
        B --> |influences| C;
        A --> |contains| OBJ[Objective 1];
        A --> |contains| OPP[Opportunity 1];
        OBJ --> |has_value_metric| VM[Issue VM1];
        B --> |influences| VM;
        C --> |influences| VM;
        E[Issue M1] --> |merged_into| D;
        F[Issue M2] --> |merged_into| D;


Data models
*************

Elements of the database are defined as data models. and are found
`$DOTDIR/api/src/v0/models`.


Metadata
---------

|

All database components
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autopydantic_model:: src.v0.models.meta.MetaData

Vertices
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autopydantic_model:: src.v0.models.meta.VertexMetaData

Edges
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autopydantic_model:: src.v0.models.meta.EdgeMetaData



Project
---------


.. autopydantic_model:: src.v0.models.project.ProjectCreate


Opportunity
------------

.. autopydantic_model:: src.v0.models.opportunity.OpportunityCreate


Objective
----------

.. autopydantic_model:: src.v0.models.objective.ObjectiveCreate


Issue
---------

.. autopydantic_model:: src.v0.models.issue.IssueCreate
   :field-list-validators: False


Edge
---------

.. autopydantic_model:: src.v0.models.edge.EdgeCreate



.. Relationships
.. --------------

.. .. autopydantic_model:: src.v0.models.project.ProjectCreate
..    :model-erdantic-figure: True
..    :model-erdantic-figure-collapsed: False



.. The database is composed of the following elements:

.. Vertices:

..     - VertexMetaData: metadata added to all vertices.
..         - *version*: the version of the database.
..         - *uuid*: the uuid of the vertex.
..         - *timestamp*: timestamp of vertex creation.
..         - *date*: date of vertex creation.
..         - *ids*: partition key for Azure cosmos DB.

..     - Project: A project is a collection of issues, objectives, and opportunities.
..         A project has the following properties:
..             - *id*: The unique identifier of the vertex (same as uuid, added by Gremlin).
..             - *label*: the label of the vertex (added by Gremlin).
..             - *name*: The name of the project.
..             - *description*: The description of the project.
..             - *tag*: list of tags (keywords).
..             - *decision_maker*: The decision maker of the project.
..             - *decision_date*: The expected end date of the project and thus the date when the decision has to be made.
..             - *sensitivity_label*: Security level (open, confidential, restricted) of the project
..             - *index*: The index of the project to be able to order different projects.  [WIP]

..         .. literalinclude:: ../../../api/src/v0/models/project.py
..             :language: python
..             :lines: 11-30

..     - Issue: An issue contains information about the decision problem. There are different types of issues:
..         - Fact
..         - Uncertainty
..         - Decision
..         - Value Metric

..     Issues have the following properties:
..         - *id*: The unique identifier of the vertex (same as uuid, added by Gremlin).
..         - *label*: the label of the vertex (added by Gremlin).
..         - *shortname*: The shorter version of the name of the issue.
..         - *description*: The description of the issue.
..         - *tag*: list of tags (keywords).
..         - *category*: The category of the issue (Fact, Uncertainty, Decision, Value Metric).
..         - *index*: The index of the issue to be able to order different issues. [WIP]
..         - *decisionType*: The type of decision (Policy, Focus, Tactical).
..         - *alternatives*: A list of possible alternatives for the decision.
..         - *keyUncertainty*: statement if the uncertainty is a key uncertainty.
..         - *probabilities*: A dictionary with information about probabilities. (see ProbabilityData).
..         - *influenceNodeUUID*: Not used anymore.
..         - *boundary*: Boundary (*in*, *on*, or *out*) of the issue.
..         - *comments*: Some added comments added to the issue.

..         .. literalinclude:: ../../../api/src/v0/models/issue.py
..             :language: python
..             :lines: 23-64

..     - Objective: An objective is a goal that the decision maker wants to achieve. Objectives have the following properties:
..         - *id*: The unique identifier of the vertex (same as uuid, added by Gremlin).
..         - *label*: the label of the vertex (added by Gremlin).
..         - *description*: The description of the objective.
..         - *index*: The index of the objective to be able to order different objectives. [WIP]
..         - *tag*: A list of possible tags or labels for a better grouping of objectives.
..         - *hierarchy*: The hierarchy of the objective (Strategic, Fundamental, Mean).


..         .. literalinclude:: ../../../api/src/v0/models/objective.py
..             :language: python
..             :lines: 9-31

..     - Opportunity: An opportunity is a statement why the decision problem is important. Opportunities have the following properties:
..         - *id*: The unique identifier of the vertex (same as uuid, added by Gremlin).
..         - *label*: the label of the vertex (added by Gremlin).
..         - *description*: The description of the opportunity.
..         - *index*: The index of the opportunity to be able to order different opportunities. [WIP]
..         - *tag*: A list of possible tags or labels for a better grouping of opportunities.

..         .. literalinclude:: ../../../api/src/v0/models/opportunity.py
..             :language: python
..             :lines: 10-28

.. Edges:
..     - EdgeMetaData: metadata added to all edges.
..         - *version*: the version of the database.
..         - *uuid*: the uuid of the vertex.
..     - Edge: An edge linking two vertices.
..         - *id*: The unique identifier of the edge (same as uuid, added by Gremlin).
..         - *label*: the label of the edge (added by Gremlin). See below for accepted labels
..         - *outV*: the uuid of the tail vertex
..         - *inV*: the uuid of the head vertex

..     - Edge labels can be:
..         - *contains*: This edge is used to show that an issue or objective or opportunity is part of a project.

..         .. mermaid::
..             :caption: *contains* edge

..             graph TD
..                 A[Project 1] --> |contains| B[Issue A1];
..                 A -->|contains| C[Issue A2];
..                 A -->|contains| D[Objective 1];


..         - *influences*: This edge is used to show that an issue influences another issue.

..         .. mermaid::
..             :caption: *influences* edge

..             graph TD
..                 A[Issue A1] --> |influences| B[Issue A2];
..                 A -->|influences| C[Issue A3];
..                 D[Issue A3] --> |influences| C[Issue A2];

..         - *has_value_metric*: This edge is used to show that an objective has a related value metric.

..         .. mermaid::
..             :caption: *has_value_metric* edge

..             graph TD
..                 A[Objective 1] --> |has_value_metric| B[Issue VM1];

..         - *merged_into*: This edge is used to show that an issue has been merged into another issue.

..         .. mermaid::
..             :caption: *merged_into* edge

..             graph TD
..                 A[Issue M1] --> |merged_into| D[Issue A3];
..                 B[Issue M2] --> |merged_into| D[Issue A3];
