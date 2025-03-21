import React, { useState, useContext } from "react";
import { createObjective } from "../services/objective_api";
import { Button, TextField, NativeSelect } from "@equinor/eds-core-react";
import { ProjectContext } from "./context";

function AddObjective({ onSave }) {
  const [project] = useContext(ProjectContext);

  const [objectiveDescription, setObjectiveDescription] = useState("");
  const [objectiveLabelText, setObjectiveLabelText] = useState([]);
  const [objectiveCategoryText, setObjectiveCategoryText] =
    useState("Strategic");

  const handleSave = async () => {
    const objective = {};
    objective.description = objectiveDescription;
    objective.hierarchy = objectiveCategoryText;
    objective.tag = objectiveLabelText;
    await createObjective(project, objective);
    onSave();
    setObjectiveDescription("");
    setObjectiveLabelText([]);
    setObjectiveCategoryText("Strategic");
  };

  const handleDescriptionChange = (event) => {
    setObjectiveDescription(event.target.value);
  };
  const handleLabelChange = (event) => {
    const splitLinesAndCommas = (str) =>
      str.split(/\r?\n/).flatMap((line) => line.split(","));
    setObjectiveLabelText(splitLinesAndCommas(event.target.value));
  };
  const handleCategoryChange = (event) => {
    setObjectiveCategoryText(event.target.value);
  };

  return (
    <div className="addNewIssue">
      <div id="issueTextField">
        <TextField
          id="issueTextFieldInput"
          placeholder="Objective"
          label="Objective"
          autoComplete="off"
          value={objectiveDescription}
          onChange={handleDescriptionChange}
        ></TextField>
      </div>
      <div id="categorySelect">
        <NativeSelect
          label="Category"
          id="categorySelect2"
          value={objectiveCategoryText}
          onChange={handleCategoryChange}
        >
          <option>Strategic</option>
          <option>Fundamental</option>
          <option>Mean</option>
        </NativeSelect>
      </div>
      <div id="labelTextField">
        <TextField
          id="labelTextFieldInput"
          placeholder="Label"
          label="Label"
          autoComplete="off"
          value={objectiveLabelText}
          onChange={handleLabelChange}
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

export default AddObjective;
