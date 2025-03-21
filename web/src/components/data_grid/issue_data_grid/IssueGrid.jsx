import React from "react";
import GenericDataGrid from "../GenericDataGrid";
import { useEditableGrid } from "../useEditableGrid";
import {
  updateIssue,
  readIssue,
  removeIssue,
} from "../../../services/issue_api";
import { IssueColumns } from "./IssueTableColumns";
import { useIssueList } from "../../allIssueContext";
import { getIssueRows } from "./IssueRows";

const IssueGrid = () => {
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
    handleCommentChange,
    handleDeleteComment,
  } = useEditableGrid();

  const handleIssueBlur = (cellValue) =>
    handleBlur(cellValue, updateIssue, readIssue);
  const handleDeleteIssue = (event) => handleDeleteClick(event, removeIssue);
  const handleIssueCellClick = (cellId) => handleCellClick(cellId);
  const handleDeleteCommentClick = (cellId, index) =>
    handleDeleteComment(cellId, index, updateIssue, readIssue);

  const columns = IssueColumns(
    editingCell,
    setEditingCell,
    cellValue,
    setCellValue,
    handleIssueCellClick,
    handleInputChange,
    handleIssueBlur,
    handleDeleteIssue,
    handleLabelChange,
    handleCommentChange,
    handleDeleteCommentClick
  );

  //default sorting - should probably be a bit different implemented using Tanstack?
  const rows = getIssueRows(issueList).sort(
    (a, b) => new Date(b.date) - new Date(a.date)
  );

  return <GenericDataGrid columns={columns} rows={rows} />;
};

export default IssueGrid;
