class abstractGraph {
  constructor() {
    this.height = "100%";
    this.width = "100%";
    this.nodes = {
      shadow: true,
      labelHighlightBold: true,
      heightConstraint: 35,
      widthConstraint: 35,
    };
    this.physics = false;
    this.layout = { randomSeed: 99 };

    // need to be define in concrete classes
    this.edges = null;
    this.groups = null;
    this.manipulation = { enabled: true };

    if (this.constructor === abstractGraph) {
      throw new Error("Abstract classes can't be instantiated.");
    }
  }

  static formatGroups() {
    throw new Error("Method 'formatGroups()' must be implemented.");
  }

  static formatTitle() {
    throw new Error("Method 'formatTitle()' must be implemented.");
  }

  static formatNode() {
    throw new Error("Method 'formatNode()' must be implemented.");
  }

  static formatEdge() {
    throw new Error("Method 'formatEdge()' must be implemented.");
  }

  static NodeFont(type) {
    throw new Error("Method 'NodeFont()' must be implemented.");
  }

  static MakeGraphNodes(obj) {
    throw new Error("Method 'MakeGraphNodes()' must be implemented.");
  }

  static MakeGraphEdges(obj) {
    // create an array with edges
    return obj.edges;
  }

  toVisData(graph) {
    const data = {
      nodes: this.constructor.MakeGraphNodes(graph),
      edges: this.constructor.MakeGraphEdges(graph),
    };
    return data;
  }

  toVisOptions() {
    // just for clarity of reading code
    return this;
  }
}

export default abstractGraph;
