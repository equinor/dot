import React from "react";
import GenericDataGrid from "../GenericDataGrid";
import { useEditableGrid } from "../useEditableGrid";
import {
  updateIssue,
  readIssue,
  removeIssue,
} from "../../../services/issue_api";
import { UncertaintyColumns } from "./UncertaintyColumns";
import { useIssueList } from "../../allIssueContext";
import { getUncertaintyRows } from "./UncertaintyRows";

const UncertaintyGrid = () => {
  const { issueList, setIssueList } = useIssueList();
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

  const columns = UncertaintyColumns(
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

  const filteredIssueList = issueList.filter(
    (issue) => issue.category === "Uncertainty"
  );
  const rows = getUncertaintyRows(filteredIssueList);

  return <GenericDataGrid columns={columns} rows={rows} />;
};

export default UncertaintyGrid;
