import React, { useState, useEffect } from "react";
import {
  Button,
  TextField,
  Dialog,
  Typography,
  Icon,
} from "@equinor/eds-core-react";
import { addIssue, readIssue } from "../services/issue_api";
import { add } from "@equinor/eds-icons";
import { addEdge, readOutEdges } from "../services/edge_api";
import { useProjectContext } from "./context";

export default function ValueMetricDialog({ objective, onEditIssue }) {
  const [project] = useProjectContext();

  const [valueMetricList, setValueMetricList] = useState([]);
  const [isOpen, setIsOpen] = useState(false);
  const [vmDescription, setVmDescription] = useState("");
  const [vmShortName, setVmShortName] = useState("");
  const [vmLabel, setVmLabel] = useState([]);

  /*---------------------
  Read all related Value Metrics
  -----------------------*/
  useEffect(() => {
    const readValueMetrics = async (objective) => {
      // read outgoing edges
      const outEdgeList = await readOutEdges(objective.id, "has_value_metric");
      //if they are not empty, get "inV" -id property
      if (outEdgeList.length > 0) {
        const newVmList = [];
        for (let edge of outEdgeList) {
          const inVid = edge.inV;
          console.log(inVid);
          const newVM = await readIssue(inVid);
          newVmList.push(newVM);
        }
        setValueMetricList(newVmList);
      }
    };
    readValueMetrics(objective);
  }, [objective]);
  /*---------------------
    Close the dialog
    ---------------------*/
  const handleClose = () => {
    onEditIssue();
    setIsOpen(false);
  };

  /*---------------------
    Save the inputted data
    ---------------------*/
  const handleSave = async () => {
    //create a new issue
    const newValueMetric = {};
    newValueMetric.category = "Value Metric";
    newValueMetric.description = vmDescription;
    newValueMetric.shortname = vmShortName;
    const splitLinesAndCommas = (str) =>
      str.split(/\r?\n/).flatMap((line) => line.split(","));
    newValueMetric.tag =
      typeof vmLabel === "string" ? splitLinesAndCommas(vmLabel) : vmLabel;
    const newValueMetricSend = await addIssue(project, newValueMetric)
      .then((result) => {
        addEdge(objective.id, result.id, "has_value_metric");
      })
      .catch((error) => {
        console.error(error);
      });

    onEditIssue();
    handleClose();
  };
  const handleOpen = () => {
    console.log(objective);
    setIsOpen(true);
  };

  return (
    <div>
      <ul>
        {" "}
        {valueMetricList.map((vm) => (
          <li key={vm.id}>{vm.shortname}</li>
        ))}
      </ul>
      <Button
        aria-haspopup="dialog"
        className="uncertaintyEditButton"
        data-tag={objective}
        variant="ghost"
        onClick={handleOpen}
      >
        <Icon data={add} title="edit" />
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
              <div id="NodeNameField" style={{ marginTop: "10px" }}>
                <TextField
                  id="NodeNameTextField"
                  placeholder="Description"
                  label="Description"
                  autoComplete="off"
                  value={vmDescription}
                  onChange={(event) => setVmDescription(event.target.value)}
                ></TextField>
              </div>
              <div id="NodeShortNameField" style={{ marginTop: "10px" }}>
                <TextField
                  id="NodeShortNameTextField"
                  placeholder="Short Name"
                  label="Short Name"
                  autoComplete="off"
                  value={vmShortName}
                  onChange={(event) => setVmShortName(event.target.value)}
                ></TextField>
              </div>
              <div id="NodeLabelField" style={{ marginTop: "10px" }}>
                <TextField
                  id="NodeLabelTextField"
                  placeholder="Label"
                  label="Label"
                  autoComplete="off"
                  value={vmLabel}
                  onChange={(event) => setVmLabel(event.target.value)}
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
