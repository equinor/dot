import abstractGraph from "../abstractGraph";

class DBGraph extends abstractGraph {
  constructor() {
    super();
    this.edges = DBGraph.formatEdge();
    this.groups = DBGraph.formatGroups();
    this.manipulation = { enabled: false };
  }

  static formatGroups() {
    return {
      Project: { shape: "circle", color: "#69717d" },
      Objective: { shape: "circle", color: "#506680" },
      Issue: { shape: "circle", color: "#00d0ff" },
      Decision: { shape: "square", color: "#00d0ff" },
    };
  }

  static NodeFont(type) {
    const color = {
      Project: "#eeeeee",
      Objective: "#f5f5f5",
      Issue: "#555555",
    };
    return { size: 12, color: color[type], face: "arial" };
  }

  static formatIssueGroups() {
    return {
      Decision: { shape: "square", color: "#53E008" },
      Uncertainty: { shape: "circle", color: "#53E008" },
      Fact: { shape: "circle", color: "#fffa00" },
      "Value Metric": { shape: "circle", color: "#00d0ff" },
      "Action Item": { shape: "circle", color: "#55ddff" },
    };
  }

  static formatTitle(text) {
    let tool_tip = "";
    tool_tip += "<h4> Description: </h4>";
    tool_tip += text;
    // tool_tip += '<h4> Probability: </h4>';
    const container = document.createElement("div");
    container.innerHTML = tool_tip;
    return container;
  }

  static formatNode(data) {
    const groups = DBGraph.formatGroups();
    const issueGroups = DBGraph.formatIssueGroups();
    data.color = groups[data.group].color;
    if (
      data.group === "Issue" ||
      data.group === "Decision" ||
      data.group === "Uncertainty"
    ) {
      data.color = issueGroups[data.type].color;
    }
    return data;
  }

  static formatEdge() {
    return { arrows: { to: { enabled: true } }, color: "#707070" };
  }

  static parseProject(node) {
    const category = "Project";
    return {
      id: node.uuid,
      label: node.shortname,
      title: DBGraph.formatTitle(node.description),
      group: category,
      font: DBGraph.NodeFont(category),
    };
  }

  static parseObjective(node) {
    const category = "Objective";
    return {
      id: node.uuid,
      label: node.shortname,
      title: DBGraph.formatTitle(node.description),
      group: category,
      font: DBGraph.NodeFont(category),
    };
  }

  static parseIssue(node) {
    const category = "Issue";
    return {
      id: node.uuid,
      label: node.shortname,
      title: DBGraph.formatTitle(node.description),
      group: category,
      font: DBGraph.NodeFont(category),
      category: node.category,
    };
  }

  static MakeGraphNodes(obj) {
    // create an array with nodes
    let nodes = [];
    let node_ = DBGraph.parseProject(obj.nodes.Project);
    DBGraph.formatNode(node_);
    nodes.push(node_);
    for (let node of obj.nodes.Objective) {
      let node_ = DBGraph.parseObjective(node);
      DBGraph.formatNode(node_);
      nodes.push(node_);
    }
    for (let node of obj.nodes.Issue) {
      let node_ = DBGraph.parseIssue(node);
      //DBGraph.formatNode(node_);
      nodes.push(node_);
    }
    return nodes;
  }
}

export default DBGraph;
