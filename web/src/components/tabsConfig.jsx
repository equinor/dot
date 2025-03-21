export const tabsConfig = [
  //main tabs
  { id: "framingTab", label: "Framing", path: "/framing" },
  { id: "structuringTab", label: "Structuring", path: "/structuring" },
  { id: "analysisTab", label: "Analysis", path: "/analysis" },
  // framing tabs
  {
    id: "opportunityTab",
    label: "Opportunity",
    path: "/framing/opportunity",
    parent: "framing",
  },
  {
    id: "objectivesTab",
    label: "Objectives",
    path: "/framing/objectives",
    parent: "framing",
  },
  {
    id: "issueListTab",
    label: "Issue List",
    path: "/framing/issuelist",
    parent: "framing",
  },
  {
    id: "issueClusteringTab",
    label: "Issue Clustering",
    path: "/framing/clustering",
    parent: "framing",
  },
  {
    id: "decisionHierarchyTab",
    label: "Decision Hierarchy",
    path: "/framing/decisionHierarchy",
    parent: "framing",
  },
  {
    id: "uncertaintiesTab",
    label: "Uncertainties",
    path: "/framing/uncertainties",
    parent: "framing",
  },
  // structuring tabs
  {
    id: "influenceDiagramTab",
    label: "Influence Diagram",
    path: "/structuring/id",
    parent: "structuring",
  },
  {
    id: "decisionTreeTab",
    label: "Decision Tree",
    path: "/structuring/dt",
    parent: "structuring",
  },
  // Add more tabs here as needed
];
