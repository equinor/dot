import React, { useState } from "react";
import { Button, Icon, Dialog, TextField } from "@equinor/eds-core-react";
import { upload } from "@equinor/eds-icons";
import { importProject } from "../services/project_api";
import "../styles/home.css";

export default function ImportDialog({ fetchData }) {
  const [isOpen, setIsOpen] = useState(false);
  const [jsonInput, setJsonInput] = useState("");

  const handleOpen = () => {
    setIsOpen(true);
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  const handleImportClick = async () => {
    const parsedJson = JSON.parse(jsonInput);
    await importProject(parsedJson)
      .then(handleClose)
      .then(fetchData)
      .catch((error) => {
        console.error("Error importing project:", error);
      });
  };

  return (
    <div>
      <Button id="projectButton" onClick={handleOpen}>
        <Icon data={upload} title="import" />
      </Button>
      <Dialog
        open={isOpen}
        isDismissable
        onClose={handleClose}
        style={{ width: "600px", height: "550px", overflow: "auto" }}
      >
        <Dialog.Header>
          <Dialog.Title>Import Project</Dialog.Title>
        </Dialog.Header>
        <Dialog.CustomContent>
          <TextField
            label="JSON Input"
            multiline
            rows={15}
            value={jsonInput}
            onChange={(e) => setJsonInput(e.target.value)}
          />
        </Dialog.CustomContent>
        <Dialog.Actions>
          <div className="buttonContainer">
            <Button
              className="importButton"
              onClick={handleImportClick}
              style={{ marginRight: "10px" }}
            >
              Import
            </Button>
            <Button className="cancelButton" onClick={handleClose}>
              Cancel
            </Button>
          </div>
        </Dialog.Actions>
      </Dialog>
    </div>
  );
}
