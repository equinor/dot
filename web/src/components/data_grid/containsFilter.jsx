import React from "react";
import { TextField, Button, Icon } from "@equinor/eds-core-react";
import { clear } from "@equinor/eds-icons";

export const ContainsFilterComponent = ({ onChange, value }) => {
  return (
    <div style={{ display: "flex", alignItems: "center" }}>
      <TextField
        label="contains filter"
        id="contains-filter"
        value={value || ""}
        onChange={(e) => onChange(e.currentTarget.value)}
      />
      <Button
        variant="contained_icon"
        onClick={(e) => onChange(null)}
        style={{ marginLeft: "10px", marginTop: "4px", width: "15%" }}
      >
        <Icon data={clear} title="clear" />
      </Button>
    </div>
  );
};
