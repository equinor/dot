import React from "react";
import GenericDataGrid from "../GenericDataGrid";
import { useEditableGrid } from "../useEditableGrid";
import {
  updateIssue,
  readIssue,
  removeIssue,
} from "../../../services/issue_api";
import { DecisionColumns } from "./DecisionColumns";
import { useIssueList } from "../../allIssueContext";
import { getDecisionRows } from "./DecisionRows";

const DecisionGrid = () => {
  const { issueList, setIssueList } = useIssueList(); //is this correct here?
  const {
    editingCell,
    setEditingCell,
    cellValue,
    setCellValue,
    handleCellClick,
    handleInputChange,
    handleBlur,
    handleLabelChange,
    handleDeleteClick,
  } = useEditableGrid();

  const handleIssueBlur = (cellValue) =>
    handleBlur(cellValue, updateIssue, readIssue);
  const handleDeleteIssue = (event) => handleDeleteClick(event, removeIssue);
  const handleIssueCellClick = (cellId) => handleCellClick(cellId);

  const columns = DecisionColumns(
    editingCell,
    setEditingCell,
    cellValue,
    setCellValue,
    handleIssueCellClick,
    handleInputChange,
    handleIssueBlur,
    handleDeleteIssue,
    handleLabelChange
  );

  console.log("Issue List", issueList);
  const filteredIssueList = issueList.filter(
    (issue) => issue.category === "Decision"
  );
  const rows = getDecisionRows(filteredIssueList);
  console.log("Decision Rows", rows);

  return <GenericDataGrid columns={columns} rows={rows} />;
};

export default DecisionGrid;
