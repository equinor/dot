import React from "react";
import { FilterWrapper } from "@equinor/eds-data-grid-react";
import {
  Chip,
  Typography,
  TextField,
  Autocomplete,
  Button,
  Icon,
} from "@equinor/eds-core-react";
import { delete_forever } from "@equinor/eds-icons";
import { ContainsFilterComponent } from "../containsFilter";
import EditableCell from "../../editableCell";
import { arrIncludes, SelectFilterComponent } from "../filterLogic";
import { CommentCell } from "../CommentTable";

function EmptyEditableCell({ setEditingCell, cellId }) {
  return (
    <div
      onClick={(e) => setEditingCell(cellId)}
      style={{ display: "flex", alignItems: "center" }}
    >
      {" "}
      <p> </p>{" "}
    </div>
  );
}

export function IssueColumns(
  editingCell,
  setEditingCell,
  cellValue,
  setCellValue,
  handleCellClick,
  handleInputChange,
  handleBlur,
  handleDeleteClick,
  handleLabelChange,
  handleCommentChange,
  handleDeleteComment
) {
  return [
    {
      accessorKey: "index",
      header: "Index",
      size: 50,
    },
    {
      accessorKey: "description",
      header: (header) => {
        return (
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <Typography variant={"cell_header"} group={"table"}>
              Description
            </Typography>
            <FilterWrapper
              column={header.column}
              CustomComponent={ContainsFilterComponent}
            />
          </div>
        );
      },
      cell: (info) => {
        const cellId = `${info.row.original.uuid}_description`;
        return (
          <EditableCell
            editingCell={editingCell}
            cellId={cellId}
            cellValue={cellValue}
            handleInputChange={handleInputChange}
            handleBlur={() => handleBlur(cellValue)}
            setEditingCell={setEditingCell}
            getValue={() => info.getValue()}
          />
        );
      },
      filterFn: "includesString",
      meta: {
        customFilterInput: true,
      },
      size: 500,
    },
    {
      accessorKey: "category",
      header: "Category",
      size: 150,
      cell: (info) => {
        const cellId = `${info.row.original.uuid}_category`;
        return editingCell === cellId ? (
          <div>
            <Autocomplete
              value={cellValue[cellId] || info.getValue()}
              options={[
                "Unassigned",
                "Fact",
                "Uncertainty",
                "Decision",
                "Value Metric",
              ]}
              onOptionsChange={(e) => {
                handleBlur({ [cellId]: e.selectedItems[0] });
                setCellValue({
                  [cellId]: e.selectedItems[0],
                });
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleBlur();
                } else if (e.key === "Escape") {
                  setEditingCell(null);
                }
              }}
              autoFocus
            />
          </div>
        ) : info.getValue() ? (
          <div
            style={{
              whiteSpace: "normal",
              overflow: "hidden",
              textOverflow: "ellipsis",
              cursor: "pointer",
              minHeight: "20px",
            }}
            onClick={(e) => setEditingCell(cellId)}
          >
            <Chip
              style={{
                //Decision: yellow, Uncertainty: green, Value Metric: blue
                background:
                  info.getValue() === "Decision"
                    ? "#FFF5B7"
                    : info.getValue() === "Value Metric"
                    ? "#C1DAEB"
                    : info.getValue() === "Uncertainty"
                    ? "#C3E4CE"
                    : undefined,
                paddingLeft: "15px",
                paddingRight: "15px",
                minWidth: "75px",
                color: "rgba(61, 61, 61, 1)",
                fontSize: "0.875rem",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
              }}
              onClick={(e) => setEditingCell(cellId)}
              label={info.getValue() || ""}
            >
              {info.getValue() || ""}
            </Chip>
          </div>
        ) : (
          EmptyEditableCell({ setEditingCell, cellId })
        );
      },
    },
    {
      accessorKey: "boundary",
      header: "Boundary",
      size: 150,
      cell: (info) => {
        const cellId = `${info.row.original.uuid}_boundary`;
        return editingCell === cellId ? (
          <div>
            <Autocomplete
              value={cellValue[cellId] || info.getValue()}
              options={["Unset", "in", "out", "on"]}
              onOptionsChange={(e) => {
                handleBlur({ [cellId]: e.selectedItems[0] });
                setCellValue({
                  [cellId]: e.selectedItems[0],
                });
              }}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleBlur();
                } else if (e.key === "Escape") {
                  setEditingCell(null);
                }
              }}
              autoFocus
            />
          </div>
        ) : info.getValue() ? (
          <Chip
            style={{
              // in: green, on: orange, out: red
              background:
                info.getValue() === "in"
                  ? "#E6F9EB"
                  : info.getValue() === "on"
                  ? "#FDDFC6"
                  : info.getValue() === "out"
                  ? "#E8937C"
                  : undefined,
              paddingLeft: "25px",
              paddingRight: "25px",
              color: "rgba(61, 61, 61, 1)",
              fontSize: "0.875rem",
              minWidth: "30px",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
            onClick={(e) => setEditingCell(cellId)}
            label={info.getValue() || ""}
          >
            {info.getValue() || ""}
          </Chip>
        ) : (
          EmptyEditableCell({ setEditingCell, cellId })
        );
      },
    },
    {
      accessorKey: "tag",
      header: (header) => {
        return (
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <Typography variant={"cell_header"} group={"table"}>
              Label
            </Typography>
            <FilterWrapper
              column={header.column}
              CustomComponent={SelectFilterComponent}
            />
          </div>
        );
      },
      cell: (info) => {
        const cellId = `${info.row.original.uuid}_tag`;
        const currentValue = cellValue[cellId] || info.row.getValue("tag");
        return editingCell === cellId ? (
          <TextField
            value={currentValue}
            onChange={(e) => handleLabelChange(e, cellId)}
            onBlur={handleBlur}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                //ToDo: add a new line on enter but how to accept the change then?
                setCellValue({
                  ...cellValue,
                  [cellId]: [...(cellValue[cellId] || info.getValue()), ""],
                });
                handleBlur();
              } else if (e.key === "Escape") {
                setEditingCell(null);
              }
            }}
            autoFocus
          />
        ) : (
          <div onClick={(e) => setEditingCell(cellId)}>
            {currentValue && currentValue.length > 0 && currentValue[0]
              ? info.getValue().map((label, index) => (
                  <Chip
                    style={{ margin: "4px" }}
                    key={index}
                    label={label}
                    title={label}
                  >
                    {label}
                  </Chip>
                ))
              : EmptyEditableCell({ setEditingCell, cellId })}
          </div>
        );
      },
      filterFn: arrIncludes,
      meta: {
        customFilterInput: true,
      },
      size: 100,
    },
    {
      accessorKey: "shortname",
      header: (header) => {
        return (
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <Typography variant={"cell_header"} group={"table"}>
              Short Name
            </Typography>
            <FilterWrapper
              column={header.column}
              CustomComponent={ContainsFilterComponent}
            />
          </div>
        );
      },
      cell: (info) => {
        const cellId = `${info.row.original.uuid}_shortname`;
        return (
          <EditableCell
            editingCell={editingCell}
            cellId={cellId}
            cellValue={cellValue}
            handleInputChange={handleInputChange}
            handleBlur={() => handleBlur(cellValue)}
            setEditingCell={setEditingCell}
            getValue={() => info.getValue()}
          />
        );
      },
      filterFn: "includesString",
      meta: {
        customFilterInput: true,
      },
      size: 200,
    },
    {
      accessorKey: "comments",
      header: (header) => {
        return (
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <Typography variant={"cell_header"} group={"table"}>
              Comments
            </Typography>
          </div>
        );
      },
      cell: (info) => (
        <CommentCell
          cellValue={cellValue}
          handleCommentChange={handleCommentChange}
          handleBlur={handleBlur}
          editingCell={editingCell}
          setEditingCell={setEditingCell}
          setCellValue={setCellValue}
          handleDeleteComment={handleDeleteComment}
          info={info}
        />
      ),
      size: 400,
      enableColumnFilter: false,
    },
    {
      accessorKey: "actions",
      header: (header) => {
        return (
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <Typography variant={"cell_header"} group={"table"}>
              Actions
            </Typography>
          </div>
        );
      },
      size: 100,
      enableColumnFilter: false,
      cell: (info) => {
        const cellId = `${info.row.original.uuid}_actions`;
        return (
          <>
            <Button
              variant="ghost"
              onClick={handleDeleteClick}
              data-tag={cellId}
              id="actionButton"
            >
              <Icon data={delete_forever} title="delete" />
            </Button>
          </>
        );
      },
    },
  ];
}
