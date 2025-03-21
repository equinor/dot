import React, { useState } from "react";
import { Button, Icon, Typography, Dialog } from "@equinor/eds-core-react";
import { delete_forever } from "@equinor/eds-icons";
import { removeProject } from "../services/project_api";
import "../styles/home.css";

export default function ProjectDeleteCheck({ project, fetchData }) {
  const [isOpen, setIsOpen] = useState(false);

  const handleOpen = (event) => {
    event.preventDefault();
    setIsOpen(true);
  };
  const handleClose = (event) => {
    if (event) {
      event.preventDefault();
    }
    setIsOpen(false);
  };

  const handleRemoveClick = async (event) => {
    event.preventDefault();
    const projectID = event.target.getAttribute("data-tag");
    console.log("Project to be deleted: ", projectID);
    await removeProject(projectID)
      .then(fetchData)
      .catch((error) => {
        console.error("Error: ", error);
      });
    setIsOpen(false);
  };

  return (
    <div>
      <Button
        variant="ghost"
        data-tag={project.uuid}
        className="removeButton"
        onClick={(e) => {
          console.log("Hello");
          handleOpen(e);
        }}
      >
        <Icon data={delete_forever} title="delete" />
      </Button>
      <Dialog
        className="projectDeleteDialog" //need to be added to css
        open={isOpen}
        isDismissable
        onClose={handleClose}
      >
        <Dialog.Header>
          <Dialog.Title>
            Do you want to delete the Project {project.name}?
          </Dialog.Title>
        </Dialog.Header>
        <Dialog.CustomContent>
          <Typography variant="body_short">
            You are about to delete the project {project.name}. Do you want to
            continue?
          </Typography>
        </Dialog.CustomContent>
        <Dialog.Actions>
          <div className="buttonContainer">
            <Button
              data-tag={project.uuid}
              className="deleteButton" //add to css
              onClick={handleRemoveClick}
            >
              YES, delete!
            </Button>
            <Button className="cancelButton" onClick={handleClose}>
              NO, cancel
            </Button>
          </div>
        </Dialog.Actions>
      </Dialog>
    </div>
  );
}
