import React, { useState, useContext } from "react";
import { Button, TextField } from "@equinor/eds-core-react";
import { createOpportunity } from "../services/opportunity_api";
import { ProjectContext } from "./context";

function AddOpportunity({ onSave }) {
  const [project] = useContext(ProjectContext);
  // vars
  const [opportunityDescription, setOpportunityDescription] = useState("");

  // actions
  const handleSave = async () => {
    const opportunity = {};
    opportunity.description = opportunityDescription.toString();
    opportunity.tag = [];
    await createOpportunity(project, opportunity);
    onSave();
    setOpportunityDescription("");
  };

  const handleDescriptionChange = (event) => {
    setOpportunityDescription(event.target.value);
  };

  // return
  return (
    <div className="addNewOpportunity">
      <div id="oppoTextField">
        <TextField
          id="oppoTextFieldInput"
          placeholder="Opportunity statement"
          label="Opportunity statement"
          autoComplete="off"
          value={opportunityDescription}
          onChange={handleDescriptionChange}
        ></TextField>
      </div>
      <div id="saveButton">
        <Button id="saveButton" onClick={handleSave}>
          Save
        </Button>
      </div>
    </div>
  );
}

export default AddOpportunity;
