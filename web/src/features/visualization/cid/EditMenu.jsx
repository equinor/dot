import React, { useState } from "react";
import {
  Button,
  TextField,
  NativeSelect,
  Dialog,
  Typography,
} from "@equinor/eds-core-react";
import { addIssue, readIssue, updateIssue } from "../../../services/issue_api";
import "../../../styles/id.css";
import { useProjectContext } from "../../../components/context";

function EditMenu({ graphData, updateGraphData, selectedNode = null }) {
  const [project] = useProjectContext();
  const [newNodeCategoryText, setNewNodeCategoryText] = useState("Decision");
  const [newNodeLabelText, setNewNodeLabelText] = useState([]);
  const [newNodeDescriptionText, setNewNodeDescriptionText] = useState("");
  const [newNodeShortNameText, setNewNodeShortNameText] = useState("");
  const [isOpen, setIsOpen] = useState(false);

  const handleClose = () => {
    setNewNodeCategoryText("Decision");
    setNewNodeLabelText([]);
    setNewNodeDescriptionText("");
    setNewNodeShortNameText("");
    setIsOpen(false);
  };

  const handleOpen = () => {
    setIsOpen(true);
  };

  const handleDescriptionChange = (event) => {
    setNewNodeDescriptionText(event.target.value);
  };
  const handleLabelChange = (event) => {
    setNewNodeLabelText(event.target.value);
  };
  const handleShortNameChange = (event) => {
    setNewNodeShortNameText(event.target.value);
  };
  const handleCategoryChange = (event) => {
    setNewNodeCategoryText(event.target.value);
  };

  const Issue = {};
  Issue.category = newNodeCategoryText;
  if (newNodeCategoryText === "Decision") {
    Issue.decisionType = "Focus";
  } else if (newNodeCategoryText === "Uncertainty") {
    Issue.keyUncertainty = "true";
  }
  Issue.boundary = "in";
  Issue.shortname = newNodeShortNameText;
  let formatedTags = Array.isArray(newNodeLabelText)
    ? newNodeLabelText.map((item) => item.trim()).filter((item) => item !== "")
    : newNodeLabelText === ""
    ? []
    : newNodeLabelText
        .split(",")
        .map((item) => item.trim())
        .filter((item) => item !== "");
  Issue.tag = formatedTags;
  Issue.description = newNodeDescriptionText;

  const handleSave = async () => {
    //might need to distinguish between add a new issue vs. editing a new issue
    if (selectedNode) {
      console.log("Editing Node");
      console.log("Selected NOde:", selectedNode);
      const issueRead = await readIssue(selectedNode.id);
      issueRead.shortname = newNodeShortNameText;
      issueRead.description = newNodeDescriptionText;
      issueRead.category = newNodeCategoryText;
      if (newNodeCategoryText === "Decision") {
        issueRead.decisionType = "Focus";
      } else if (newNodeCategoryText === "Uncertainty") {
        issueRead.keyUncertainty = "true";
      }
      issueRead.tag = formatedTags; //should be a valid list
      const updatedData = {
        shortname: newNodeShortNameText,
        description: newNodeDescriptionText,
        category: newNodeCategoryText,
        tag: formatedTags,
      };
      if (newNodeCategoryText === "Decision") {
        updatedData.decisionType = "Focus";
      } else if (newNodeCategoryText === "Uncertainty") {
        updatedData.keyUncertainty = "true";
      }
      await updateIssue(issueRead.uuid, updatedData).then(updateGraphData());
      updateGraphData();
      handleClose();
    } else {
      console.log("saving a new issue", Issue);
      const newElement = await addIssue(project, Issue).then(updateGraphData());

      console.log("Added new issue: ", newElement);
      updateGraphData();
      handleClose();
    }
  };

  const handleOpenEdit = async () => {
    //get node ID from selected node
    console.log("selectedNode:", selectedNode);
    if (selectedNode) {
      //get information from Node
      setNewNodeShortNameText(selectedNode.label);
      setNewNodeCategoryText(selectedNode.group);

      //get more information via API
      const nodeToUpdate = await readIssue(selectedNode.uuid);
      console.log("Data: ", nodeToUpdate);

      //set values in text fields
      setNewNodeDescriptionText(nodeToUpdate.description);
      setNewNodeDescriptionText(nodeToUpdate.description);
      setNewNodeLabelText(nodeToUpdate.tag);

      //open dialog
      setIsOpen(true);
    } else {
      alert("No Node selected.");
    }
  };

  return (
    <div className="editMenu">
      <Button className="idActionButton" onClick={handleOpen}>
        Add Node
      </Button>
      <Button
        className="idActionButton"
        id="editNodeButton"
        onClick={handleOpenEdit}
      >
        Edit Node{" "}
      </Button>
      <Button
        className="idActionButton"
        id="addEdgeButton" /* onClick={CIDGraph.addEdgeClick} */
      >
        Add Edge{" "}
      </Button>
      <Button className="idActionButton" id="deleteSelected">
        Delete Selected{" "}
      </Button>

      <Dialog
        className="idDialog"
        id="idDialog"
        open={isOpen}
        onClose={handleClose}
        style={{ minWidth: "500px" }}
      >
        <Dialog.Header>
          <Dialog.Title> Add and Edit Node </Dialog.Title>
        </Dialog.Header>
        <Dialog.CustomContent>
          <Typography>
            <div className="EditMenu" id="EditMenu">
              Please add a node:
              <div id="NodeCategorySelect" style={{ marginTop: "10px" }}>
                <NativeSelect
                  label="Category"
                  className="NodeCategorySelect2"
                  value={newNodeCategoryText}
                  onChange={handleCategoryChange}
                >
                  <option value="Unassigned">Unassigned</option>
                  <option value="Decision">Decision</option>
                  <option value="Uncertainty">Uncertainty</option>
                  <option value="Value Metric">Value</option>
                </NativeSelect>
              </div>
              <div id="NodeShortNameField" style={{ marginTop: "10px" }}>
                <TextField
                  id="NodeShortNameTextField"
                  placeholder="Short Name"
                  label="Short Name"
                  autoComplete="off"
                  value={newNodeShortNameText}
                  onChange={handleShortNameChange}
                ></TextField>
              </div>
              <div id="NodeDescriptionField" style={{ marginTop: "10px" }}>
                <TextField
                  id="NodeDescriptionTextField"
                  placeholder="Description"
                  label="Description"
                  autoComplete="off"
                  value={newNodeDescriptionText}
                  onChange={handleDescriptionChange}
                ></TextField>
              </div>
              <div id="NodeLabelField" style={{ marginTop: "10px" }}>
                <TextField
                  id="NodeLabelTextField"
                  placeholder="Label"
                  label="Label"
                  autoComplete="off"
                  value={newNodeLabelText}
                  onChange={handleLabelChange}
                ></TextField>
              </div>
              <br />
            </div>
          </Typography>
        </Dialog.CustomContent>
        <Dialog.Actions>
          <div id="Buttons">
            <Button className="saveButton" onClick={handleSave}>
              Save
            </Button>{" "}
            <Button id="cancelButton" onClick={handleClose}>
              Cancel
            </Button>
          </div>
        </Dialog.Actions>
      </Dialog>
    </div>
  );
}

export default EditMenu;
