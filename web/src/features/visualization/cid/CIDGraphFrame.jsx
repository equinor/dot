import React, { useState, useEffect, createRef } from "react";
import { Network } from "vis-network/standalone";
import CIDGraph from "./CIDGraph";
import { readInfluenceDiagram } from "../../../services/structures_api";
import EditMenu from "./EditMenu";
import { useProjectContext } from "../../../components/context";
import "../../../styles/id.css";

function Graph() {
  const graph = new CIDGraph();
  const [project] = useProjectContext();

  const [influenceDiagram, setInfluenceDiagram] = useState("");
  const [, setProj] = useState(null);
  const [options, setOptions] = useState(null);
  const [data, setData] = useState({ nodes: [], edges: [] });
  const [selectedNode, setSelectedNode] = useState(null);

  const fetchData = async () => {
    try {
      const updatedID = await readInfluenceDiagram(project);
      console.log("ID:", updatedID);
      setInfluenceDiagram(updatedID);
      const visData = graph.toVisData(updatedID);
      console.log("visData ", visData);
      const options = {
        physics: {
          enabled: false, // Disable physics simulation
        },
      };
      const visOptions = graph.toVisOptions(options);

      setData(visData);
      setOptions(visOptions);
      console.log("updating graph data...");
    } catch (error) {
      console.error("Error fetching or processing data", error);
    }
  };

  useEffect(() => {
    fetchData();
    console.log("Updating Graph...");
  }, []);

  const container = createRef();

  useEffect(() => {
    document.getElementById("addEdgeButton").onclick = addEdgeClick;
    document.getElementById("deleteSelected").onclick = deleteClick;
    document.getElementById("editNodeButton").onclick = editNode;

    var inAddEdgeMode = false;

    function deleteClick() {
      network.deleteSelected();
    }

    function editNode() {
      //if a node is selected enable edit mode
      //network.editNode()
      const selection = network.getSelection(); //get ID
      console.log(selection);
      const nodeData = data.nodes.find(
        (node) => node.id === selection.nodes[0]
      );
      if (nodeData) {
        console.log("node data", nodeData);
        setSelectedNode(nodeData);
      } else {
        console.log("No Node Selected");
        setSelectedNode(null);
      }
      //if no node is selected, give a warning
    }

    function addEdgeClick() {
      console.log("Edge: ", inAddEdgeMode);
      if (inAddEdgeMode) {
        console.log("not in edit mode");
        network.disableEditMode();
        inAddEdgeMode = false;
      } else {
        console.log("In Edge adding mode");
        network.addEdgeMode();
        inAddEdgeMode = false;
      }
    }
    console.log("Rendering Graph");
    const network =
      container.current && new Network(container.current, data, options);
  }, [container, data, options]);
  console.log("selected?", selectedNode);
  return (
    <>
      <div className="container">
        <EditMenu
          className="mainEditMenu"
          graphData={influenceDiagram}
          updateGraphData={fetchData}
          selectedNode={selectedNode}
        />
        <div
          className="idVis"
          id="network"
          ref={container}
          style={{ height: "900px" }}
        />
      </div>
    </>
  );
}

export default Graph;
