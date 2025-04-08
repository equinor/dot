import {
  removeIssue,
  readIssue,
  updateIssue,
} from "../../../services/issue_api";
import { removeEdgeID, addEdge } from "../../../services/edge_api";
import abstractGraph from "../abstractGraph";

class CIDGraph extends abstractGraph {
  constructor() {
    super();
    this.edges = CIDGraph.formatEdge();
    this.groups = CIDGraph.formatGroups();
    this.manipulation = {
      enabled: false,
      initiallyActive: false,
      addNode: false, //CIDGraph.onAddNode,
      editNode: CIDGraph.editNode,
      addEdge: CIDGraph.addEdge,
      deleteNode: CIDGraph.deleteNode,
      deleteEdge: CIDGraph.deleteEdge, //need to be defined
    };
  }

  static clearPopUp() {
    document.getElementById("saveButton").onclick = null;
    document.getElementById("cancelButton").onclick = null;
    document.getElementById("EditMenu").style.display = "none";
  }

  static cancelEdit(callback) {
    CIDGraph.clearPopUp();
    callback(null);
  }

  static saveData(data, callback) {
    if (document.getElementById("NodeCategorySelect2").value !== "") {
      data.group = document.getElementById("NodeCategorySelect2").value;
      data.label = document.getElementById("NodeLabelTextField").value;
      data.title = CIDGraph.formatTitle(
        document.getElementById("NodeDescriptionTextField").value
      );
      data.font = CIDGraph.NodeFont(data.group);
      console.log("Saving???", data);
      callback(data);
      console.log("Saved??", data);
      CIDGraph.formatNode(data);
      CIDGraph.clearPopUp();
    }
  }

  /* static onAddNode(data, callback) {
      // filling in the popup DOM elements
      //document.getElementsByClassName("dialogContainer").style.display = "block"
      //document.getElementById("NodeCategorySelect2").value = "Uncertainty";
      console.log("Hello! Adding new Node");
      callback(data);
      document.getElementsByClassName("saveButton").onclick = CIDGraph.saveData.bind(
        this,
        data,
        callback
      );

      document.getElementsByClassName("cancelButton").onclick = CIDGraph.clearPopUp.bind();
      //document.getElementById("EditMenu").style.display = "block";

    } */

  static async editNode(data, callback) {
    // filling in the popup DOM elements
    console.log("Editing Node: ", data);
  }

  static async addEdge(data, callback) {
    // callback(data);
    if (data.from === data.to) {
      if (window.confirm("Do you want to connect the node to itself?")) {
        callback(data);
      }
    } else {
      //add API call format of data = from: index , to: index (but the one of the node, not the property)
      console.log("adding edge", data);
      console.log(data.from);
      await addEdge(data.from, data.to, "influences");
      // need to set the disable Edit Mode again
      // need to update influencingNode in the Node
      callback(data);
    }
  }

  static async deleteNode(data, callback) {
    console.log("Deleting", data);
    console.log("Delete Node: ", data.nodes[0]);
    const identifier = data.nodes[0];
    const regexExp =
      /^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$/i;
    if (regexExp.test(identifier)) {
      //read the node
      let deleteNode = await readIssue(identifier);
      console.log("Delete Node: ", deleteNode);
      let updatedData = {};
      if (deleteNode.category === "Uncertainty") {
        updatedData.keyUncertainty = null;
        await updateIssue(identifier, updatedData);
      } else if (deleteNode.category === "Decision") {
        updatedData.category = null;
        await updateIssue(identifier, updatedData);
      } else if (deleteNode.category === "Value Metric") {
        console.log("Hmmm... remove");
        //TODO: what to do with Value Metrics?
      }
    }

    callback(data);
  }

  static async deleteEdge(data, callback) {
    console.log("Deleting Edge", data);
    const edgeID = data.edges[0];
    console.log(edgeID);
    //need to figure out how to delete an edge
    await removeEdgeID(edgeID);
    callback(data);
  }

  static formatGroups() {
    return {
      Uncertainty: {
        shape: "circle",
        color: "#53E008",
        widthConstraint: { maximum: 80 },
      },
      Decision: {
        shape: "box",
        shapeProperties: { borderRadius: 4 },
        color: "#fffa00",
        widthConstraint: { maximum: 80 },
      },
      "Value Metric": {
        shape: "diamond",
        shapeProperties: { borderRadius: 4 },
        color: "#00d0ff",
        widthConstraint: { maximum: 80 }, //max width of node, maybe min is also useful?
      },
    };
  }

  static formatTitle(text, nodeType, probabilities, alternatives, infNode) {
    //split alternatives into array elements
    let tool_tip = "";
    tool_tip += "<h4> Description: </h4>";
    tool_tip += text;
    if (nodeType === "Uncertainty") {
      if (probabilities) {
        const altArray = probabilities?.toString().split(",");
        tool_tip += "<h4> Probabilities </h4>";
        tool_tip += "type: " + probabilities.dtype + "<br>";
        tool_tip += "variables: <br>";
        Object.entries(probabilities.variables).map((entry) => {
          tool_tip += "&nbsp;&nbsp;&nbsp;&nbsp;" + entry[0] + " : ";
          tool_tip += entry[1] + "<br>";
        });
        tool_tip += "function: " + probabilities.probability_function;
      }
    } else if (nodeType === "Decision") {
      if (alternatives) {
        const altArray = alternatives?.toString().split(",");
        console.log("Alt arrat", altArray);
        tool_tip += "<h4> Alternatives </h4>";
        tool_tip += `<ul> ${altArray
          ?.map((alt) => `<li> ${alt} </li>`)
          .join(" ")} </ul>`;
      }
    }
    /* <tr> ${probabilities?.map(
        (probs) => `<td> ${probs} </td> `
      )}</tr>  */
    const container = document.createElement("div");
    container.innerHTML = tool_tip;
    return container;
  }

  static NodeFont(type) {
    const color = {
      Decision: "#111111",
      Value: "#333333",
      Uncertainty: "#555555",
    };
    return { size: 14, color: color[type], face: "equinor" };
  }

  static formatNode(data) {
    const groups = CIDGraph.formatGroups();
    console.log(groups);
    console.log(data);
    data.shape = groups[data.group].shape;
    data.color = groups[data.group].color;
    if (data.group !== "Uncertainty") {
      data.shapeProperties = {};
      data.shapeProperties.borderRadius =
        groups[data.group].shapeProperties.borderRadius;
    }
    return data;
  }

  static formatEdge() {
    return { arrows: { to: { enabled: true } }, color: "#707070" };
  }

  static MakeGraphNodes(obj) {
    // create an array with nodes
    //const groups = CIDGraph.formatNode(obj);
    console.log("MakeGraphNode", Object.keys(obj));
    console.log("MakeGraphNode", Object.keys(obj.vertices));
    let categories = Object.keys(obj.vertices);
    let nodes = [];
    for (let category of categories) {
      console.log(category);
      console.log("Test", obj.vertices);
      //for (let node of obj.vertices[category]) {
      let node_ = {
        id: obj.vertices[category].id,
        uuid: obj.vertices[category].uuid, //uuid = id
        label: obj.vertices[category].shortname,
        title: CIDGraph.formatTitle(
          obj.vertices[category].description,
          obj.vertices[category].category,
          obj.vertices[category].probabilities,
          obj.vertices[category].alternatives,
          obj.vertices[category].influenceNodeUUID
        ),
        group: obj.vertices[category].category,
        font: CIDGraph.NodeFont(category),
      };
      CIDGraph.formatNode(node_);
      nodes.push(node_);
    }
    console.log(nodes);
    return nodes;
  }

  static MakeGraphEdges(obj) {
    let edge_list = obj.edges;
    let edges = [];
    for (let edge of edge_list) {
      console.log(edge);
      let edge_ = {
        id: edge.uuid,
        to: edge.inV,
        from: edge.outV,
      };
      edges.push(edge_);
      console.log(edge_);
    }
    console.log(edges);
    return edges;
  }
}

export default CIDGraph;
