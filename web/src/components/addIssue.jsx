import React, { useState, useContext } from "react";
import { addIssue } from "../services/issue_api";
import { Button, TextField, NativeSelect } from "@equinor/eds-core-react";
import "../styles/addNewIssueStyle.css";
import { ProjectContext } from "./context";

function AddIssue({ onSave }) {
  const defaultCategory = null;
  const [project] = useContext(ProjectContext);
  const [issueDescriptionText, setIssueDescriptionText] = useState("");
  const [issueLabelText, setIssueLabelText] = useState("");
  const [issueShortName, setIssueShortName] = useState("");
  const [issueCategoryText, setIssueCategoryText] = useState(defaultCategory); //default state is empty?

  const handleSave = async () => {
    const Issue = {};
    let formatedTags = Array.isArray(issueLabelText)
      ? issueLabelText.map((item) => item.trim()).filter((item) => item !== "")
      : issueLabelText === ""
      ? []
      : [issueLabelText];
    Issue.tag = formatedTags;
    Issue.category = issueCategoryText;
    Issue.description = issueDescriptionText;
    Issue.shortname = issueShortName;
    console.log(Issue);
    await addIssue(project, Issue);
    onSave();
    setIssueDescriptionText("");
    setIssueCategoryText(defaultCategory);
    setIssueLabelText([]);
    setIssueShortName("");
  };

  const handleDescriptionChange = (event) => {
    setIssueDescriptionText(event.target.value);
  };

  const handleLabelChange = (event) => {
    console.log(event.target.value);
    const splitLinesAndCommas = (str) =>
      str.split(/\r?\n/).flatMap((line) => line.split(","));
    setIssueLabelText(splitLinesAndCommas(event.target.value));
    // setIssueLabelText(event.target.value);
  };

  const handleShortNameChange = (event) => {
    setIssueShortName(event.target.value);
  };
  const handleCategoryChange = (event) => {
    setIssueCategoryText(event.target.value);
  };

  return (
    <div className="addNewIssue">
      <div id="issueTextField">
        <TextField
          id="issueTextFieldInput"
          placeholder="Issue"
          label="Issue"
          autoComplete="off"
          value={issueDescriptionText}
          onChange={handleDescriptionChange}
        ></TextField>
      </div>
      <div id="categorySelect">
        <NativeSelect
          label="Category"
          id="categorySelect2"
          value={issueCategoryText}
          onChange={handleCategoryChange}
        >
          <option value="">Unassigned</option>
          <option value="Fact">Fact</option>
          <option value="Uncertainty">Uncertainty</option>
          <option value="Decision">Decision</option>
          <option value="Value Metric">Value Metric</option>
          <option value="Action Item">Action Item</option>
        </NativeSelect>
      </div>
      <div id="issueTextField">
        <TextField
          id="issueTextFieldInput"
          placeholder="Label"
          label="Label"
          autoComplete="off"
          value={issueLabelText}
          onChange={handleLabelChange}
        ></TextField>
      </div>
      <div id="issueTextField">
        <TextField
          id="issueTextFieldInput"
          placeholder="Short Name"
          label="Short Name"
          autoComplete="off"
          value={issueShortName}
          onChange={handleShortNameChange}
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

export default AddIssue;
