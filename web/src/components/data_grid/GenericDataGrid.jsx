import React from "react";
import { EdsDataGrid } from "@equinor/eds-data-grid-react";

const GenericDataGrid = ({ columns, rows }) => {
  return (
    <EdsDataGrid
      columns={columns}
      rows={rows}
      enableColumnFiltering
      enableSorting
      enablePagination
      pageSize={60}
      columnResizeMode="onChange"
      style={{ padding: "20px", width: "95%" }}
    />
  );
};

export default GenericDataGrid;
