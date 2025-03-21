import React, { useState } from "react";
import { Button } from "@equinor/eds-core-react";

const EditMenu = () => {
  const [, setExportText] = useState("");

  const handleExportChange = (event) => {
    setExportText(event.target.value);
  };

  return (
    <div className="ioMenu" id="ioMenu">
      <br />
      <span id="operation" style={{ fontWeight: "bold" }}>
        DataBase
      </span>{" "}
      <br />
      <br />
      <div id="Buttons">
        <Button id="importButton">Import</Button>{" "}
        <Button id="exportButton">Export</Button>
      </div>
    </div>
  );
};

export default EditMenu;
