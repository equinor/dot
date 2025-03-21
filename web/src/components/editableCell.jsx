import React from "react";
import { TextField } from "@equinor/eds-core-react";

const EditableCell = ({
  editingCell,
  cellId,
  cellValue,
  handleInputChange,
  handleBlur,
  setEditingCell,
  getValue,
}) => {
  return editingCell === cellId ? (
    <TextField
      value={cellValue[cellId] || getValue()}
      onChange={(e) => handleInputChange(e, cellId)}
      onBlur={handleBlur}
      onKeyDown={(e) => {
        if (e.key === "Enter") {
          handleBlur();
        } else if (e.key === "Escape") {
          setEditingCell(null);
        }
      }}
      autoFocus
    />
  ) : (
    <div
      style={{
        whiteSpace: "normal",
        overflow: "hidden",
        textOverflow: "ellipsis",
        cursor: "pointer",
        minHeight: "20px",
      }}
      onClick={() => setEditingCell(cellId)}
    >
      {getValue()}
    </div>
  );
};

export default EditableCell;
