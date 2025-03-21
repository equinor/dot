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

export function DecisionColumns(
  editingCell,
  setEditingCell,
  cellValue,
  setCellValue,
  handleCellClick,
  handleInputChange,
  handleBlur,
  handleDeleteClick,
  handleLabelChange
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
      accessorKey: "decisionType",
      header: "Decision Type",
      size: 150,
      cell: (info) => {
        const cellId = `${info.row.original.uuid}_decisionType`;
        return editingCell === cellId ? (
          <div>
            <Autocomplete
              value={cellValue[cellId] || info.getValue()}
              options={["Policy", "Focus", "Tactical", " "]}
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
        ) : (
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
            {info.getValue() || ""}
          </div>
        );
      },
    },
    {
      size: 100,
      accessorKey: "tag",
      filterFn: arrIncludes,
      meta: {
        customFilterInput: true,
      },
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
              CustomComponent={(props) => (
                <SelectFilterComponent {...props} listNum={1} />
              )}
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
                // setCellValue({
                //   ...cellValue,
                //   [cellId]: [...(cellValue[cellId] || info.getValue()), ""],
                // });
                handleBlur();
              } else if (e.key === "Escape") {
                setEditingCell(null);
              }
            }}
            autoFocus
          />
        ) : (
          <div onClick={(e) => setEditingCell(cellId)}>
            {currentValue && currentValue.length > 0 && currentValue[0] ? (
              currentValue.map((label, index) => (
                <Chip
                  style={{ margin: "4px" }}
                  key={index}
                  label={label}
                  title={label}
                >
                  {label}
                </Chip>
              ))
            ) : (
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                }}
              >
                {" "}
                <p> </p>{" "}
              </div>
            )}
          </div>
        );
      },
    },
    {
      accessorKey: "alternatives",
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
              Alternatives
            </Typography>
            <FilterWrapper
              column={header.column}
              CustomComponent={(props) => (
                <SelectFilterComponent {...props} listNum={0} />
              )}
            />
          </div>
        );
      },
      cell: (info) => {
        const cellId = `${info.row.original.uuid}_alternatives`;
        const currentValue =
          cellValue[cellId] || info.row.getValue("alternatives");
        return editingCell === cellId ? (
          <TextField
            value={currentValue}
            onChange={(e) => handleLabelChange(e, cellId)}
            onBlur={handleBlur}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                //ToDo: add a new line on enter but how to accept the change then?
                console.log("CellVale", cellValue, info.getValue());
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
            {currentValue && currentValue.length > 0 && currentValue[0] ? (
              <ul>
                {currentValue.map((alternatives, index) => (
                  <li key={index}>{alternatives}</li>
                ))}
              </ul>
            ) : (
              <div style={{ display: "flex", alignItems: "center" }}>
                {" "}
                <p> </p>{" "}
              </div>
            )}
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
    /*   {
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
            <FilterWrapper
              column={header.column}
              CustomComponent={ContainsFilterComponent}
            />
          </div>
        );
      },
      size: 400,
      filterFn: "includesString",
      meta: {
        customFilterInput: true,
      },
    }, */
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
