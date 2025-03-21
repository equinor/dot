import { useState } from "react";
import { useIssueList } from "../allIssueContext";

export const useEditableGrid = () => {
  const [editingCell, setEditingCell] = useState(null);
  const [cellValue, setCellValue] = useState({});
  const { issueList, setIssueList } = useIssueList();

  const handleCellClick = (e, cellId) => {
    setEditingCell(cellId);
    console.log("CellId", cellId);
  };

  const handleInputChange = (e, cellId) => {
    setCellValue({
      ...cellValue,
      [cellId]: e.target.value,
    });
  };

  const handleLabelChange = (e, cellId) => {
    const lines = e.target.value.split(",");
    setCellValue({
      ...cellValue,
      [cellId]: lines,
    });
  };
  const handleCommentChange = (e, cellId) => {
    setCellValue({
      [cellId]: e.target.value,
    });
  };

  const handleDeleteComment = async (cellId, index, updateItem, readItem) => {
    const [uuid, columnName] = cellId.split("_");
    const issue = await readItem(uuid);
    if (columnName === "comments") {
      const reversedComments = issue.comments.slice().reverse();
      const updatedComments = reversedComments.filter((_, i) => i !== index);
      const finalComments = updatedComments.slice().reverse();
      issue.comments = finalComments;
      await updateItem(uuid, issue);
      setCellValue((prevCellValue) => ({
        ...prevCellValue,
        [cellId]: finalComments,
      }));
    }
  };

  const handleBlur = async (cellValueInput = {}, updateItem, readItem) => {
    const valueToUpdate =
      Object.keys(cellValueInput).length === 0 ? cellValue : cellValueInput;
    if (!valueToUpdate || Object.keys(valueToUpdate).length === 0) {
      setEditingCell(null);
      console.log("No cell value to update", valueToUpdate);
      return;
    }
    const [uuid, columnName] = Object.keys(valueToUpdate)[0].split("_");
    const updatedValue = valueToUpdate[`${uuid}_${columnName}`];

    // Create a dictionary with the property and the value to be updated
    const issue = await readItem(uuid);
    let updateData = {};
    switch (columnName) {
      case "outcomes": {
        const firstKey = Object.keys(issue.probabilities.variables)[0];
        issue.probabilities.variables[firstKey] = updatedValue;
        updateData = { probabilities: issue.probabilities };
        console.log("updateData", updateData);
        console.log(issue.probabilities);
        break;
      }
      case "comments": {
        updateData = { comments: [{ comment: updatedValue, author: "User" }] };
        break;
      }
      case "keyUncertainty": {
        updateData = {
          keyUncertainty: updatedValue === "Key" ? "true" : "false",
        };
        break;
      }
      case "category": {
        updateData = {
          category: updatedValue === "Unassigned" ? "" : updatedValue,
        };
        break;
      }
      case "boundary": {
        updateData = { boundary: updatedValue === "Unset" ? "" : updatedValue };
        break;
      }
      default: {
        updateData = { [columnName]: updatedValue };
        break;
      }
    }

    try {
      await updateItem(uuid, updateData);
      setEditingCell(null);
      setCellValue({});
      setIssueList((prevIssues) => {
        return prevIssues.map((item) => {
          if (item.uuid === uuid) {
            switch (columnName) {
              case "outcomes": {
                const firstKey = Object.keys(item.probabilities.variables)[0];
                return {
                  ...item,
                  probabilities: {
                    ...item.probabilities,
                    variables: {
                      ...item.probabilities.variables,
                      [firstKey]: updatedValue,
                    },
                  },
                };
              }
              case "comments": {
                return {
                  ...item,
                  comments: [
                    ...(item.comments || []),
                    { comment: updatedValue, author: "User" },
                  ],
                };
              }

              case "keyUncertainty": {
                if (updatedValue === "Key") {
                  return { ...item, keyUncertainty: "true" };
                } else {
                  return { ...item, keyUncertainty: "false" };
                }
              }
              case "category": {
                if (updatedValue === "Unassigned") {
                  return { ...item, category: "" };
                } else {
                  return { ...item, category: updatedValue };
                }
              }
              case "boundary": {
                if (updatedValue === "Unset") {
                  return { ...item, boundary: "" };
                } else {
                  return { ...item, boundary: updatedValue };
                }
              }
              default: {
                return { ...item, [columnName]: updatedValue };
              }
            }
          }
          return item;
        });
      });
    } catch (error) {
      console.error("Failed to update issue:", error);
    }
  };
  /*--------------
    Remove Row
    ----------------*/
  const handleDeleteClick = async (event, removeItem) => {
    const cellId = event.target.getAttribute("data-tag").toString();
    console.log("event", event, "cell", cellId);
    const [uuid, columnName] = cellId.split("_");
    try {
      await removeItem(uuid);
      setIssueList((prevIssues) => {
        return prevIssues.filter((item) => item.uuid !== uuid);
      });
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  return {
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
  };
};
