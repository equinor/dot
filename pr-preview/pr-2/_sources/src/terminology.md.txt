# Terminology

The terminology found in the literature may not be unique and we explain here the main terms used in the DOT.

## Process

Understanding the general decision making process will help understanding the terminology used across the tool.

## Terms

### Decision Modelling

Decision Modelling is the process of creating a structured and visual representation of the dependencies between decisions and uncertainties for a decision problem.
By using Decision Modelling complex decision-making processes can be broken down into understandable components.
In addition, a visual representation can help understanding the decision model.

### Framing

The Framing process is a step in decision-making. It involves defining the decision problem clearly and ensuring that the analysis team works on the right problem towards the objectives and values given by the decision maker. During this process the objectives, values, boundaries, opportunities and issues are identified. The framing is a cross-collaborative and iterative process.

### Influence Diagram

An influence diagram (ID) is a compact graphical and mathematical representation of a decision problem. It contains all important decisions (Focus Decisions) and uncertainties (Key Uncertainties) and their relationships and influences. From an ID a decision tree representation can be derived. An influence diagram can be solved and evaluated making it possible to perform analysis without a decision tree.

### Decision Tree

A decision tree (DT) is a graphical and mathematical representation of a decision model which has a hierarchical, tree-like structure. Different branches in a decision tree will represent potential outcomes and alternatives.

### Issue

An Issue contains any information about the decision modelling process.

#### Fact

A Fact is an issue which is either true and known or an assumption.

#### Uncertainty

An Uncertainty is an issue whose outcomes are unknown. Each uncertainty should contain outcomes (discrete or continuous) describing different possible events of the uncertainty.
We further distinguish key uncertainties which are uncertainties which impact the decision sufficiently.

#### Decision

A Decision is an issue which the decision maker can influence and which is in line with the defined objectives and available information. Each decision should contain several alternatives which are the possible choices of the decision.
We distinguish between three different types of decisions.

##### Policy Decision

A Policy Decision is a high-level decision that sets the overall direction and guidelines for an organization or system. It establishes the principles and rules that guide decision-making in specific situations.

##### Focus Decision

A Focus Decision is a decision that addresses a specific problem or objective within the context of a larger decision-making process. It involves selecting the best alternative among a set of options to achieve a specific goal. The decision treated in the decision problem can be thought of as a focus decision which is made in context of policy decisions and might result in tactical decisions.

##### Tactical Decision

A Tactical Decision is a short-term decision that focuses on the implementation of specific actions as a result of the focus decisions. It involves making choices and taking actions to address operational issues and optimize resources which are decisions which can be treated at a later stage.

#### Value Metric

A Value Metric is an issue which allows us to quantify an objective and assign a value to the decisions. A value metric will then based on logical reasoning guide to the optimal decision.

### Objective

An objective refers to a desired outcome or goal that an individual or organization aims to achieve through the decision-making process.

#### Strategic Objective

A strategic objective is a high-level goal that aligns with the long-term vision and mission of an organization. It sets the overall direction and priorities for decision-making and guides the allocation of resources and efforts towards achieving strategic goals.

#### Fundamental Objective

A fundamental objective represents a core value or principle that underlies decision-making. It reflects the fundamental beliefs and priorities of an individual or organization and serves as a guiding principle in evaluating and selecting alternatives.

#### Mean Objective

A mean objective refers to an intermediate or sub-goal that contributes to the achievement of a higher-level objective. It represents a specific target or milestone that needs to be accomplished in order to make progress towards the overall objective.

### Opportunity

An opportunity is a favorable situation or circumstance that presents a chance to improve the objectives based on high quality decisions.

### Probabilistic graph model

### Structuring

### Node

A node (also called vertex) is a fundamental building block of a graph. We are using nodes to represent the data for the decision modelling process. Nodes can have different labels, like `project`, `issue`, `opportunity` or `objective`. Each node will then represent one element of the decision problem with specified properties and information.
The nodes are also components of influence diagrams and decision trees.

### Edge

Edges (also called arcs, in particular for directional graphs) represent a connection or relationship between two nodes. This way we are representing that issues, objectives and opportunities belong to a project and that issues influence each other.

## Literature

- Reidar B. Bratvold, Steve H. Begg (2010), Making Good Decisions, Society of Petroleum Engineers, https://doi.org/10.2118/9781555632588
- https://en.wikipedia.org/wiki/Decision_model
- https://en.wikipedia.org/wiki/Decision-making_models
