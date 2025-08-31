import React, { useState, useEffect } from "react";
import {
  Button,
  TextField,
  Dialog,
  Typography,
  NativeSelect,
} from "@equinor/eds-core-react";
import { readProject, reportProject } from "../services/project_api";

// Dialog Component
const ReportDialog = ({ uuid, onClose }) => {
  console.log("ReportDialog - uuid/onClose", uuid, onClose);
  const [projectData, setProjectData] = useState(null);
  const [fileFormat, setFileFormat] = useState("docx");
  const [filePath, setFilePath] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      console.log("ReportDialog - useEffect");
      if (!uuid) return;
      try {
        const project_data = await readProject(uuid);
        console.log("ReportDialog - fetchData", project_data);
        setProjectData(project_data);
        setFilePath(project_data.name);
      } catch (error) {
        console.error("reportProject - Error:: ", error);
      }
    };
    fetchData(uuid);
  }, [uuid]);

  const handleReport = () => {
    console.log("handleReport - Reporting Project:");
    console.log("handleReport - Format:", fileFormat);
    console.log("handleReport - Filepath:", filePath);
    console.log("handleReport - Project Data:", projectData);

    try {
      const project_data = reportProject(uuid);
      console.log("handleReport - ReportDialog - reportProject", project_data);
    } catch (error) {
      console.error("handleReport - reportProject - Error:: ", error);
    }
    onClose(); // Close the dialog after saving
  };

  const addExtensionToFilepath = (path, ext) => {
    return path + "." + ext;
  };

  return (
    <>
      <div>
        {projectData && (
          <Dialog
            className="idReportDialog"
            id="idReportDialog"
            open={true}
            onClose={onClose}
            style={{ minWidth: "500px" }}
          >
            <Dialog.Header>
              <Dialog.Title>Reporting of project </Dialog.Title>
            </Dialog.Header>
            <Dialog.CustomContent>
              <Typography>
                <div className="ReportMenu" id="ReportMenu">
                  <div id="FormatField" style={{ marginTop: "10px" }}>
                    <NativeSelect
                      id="native-select"
                      label="Output file format"
                      value={fileFormat}
                      onChange={(event) => setFileFormat(event.target.value)}
                    >
                      <option>md</option>
                      <option>docx</option>
                      <option>odt</option>
                      <option>pptx</option>
                    </NativeSelect>
                  </div>
                  <div id="FilePathField" style={{ marginTop: "10px" }}>
                    <TextField
                      id="FilePathTextField"
                      placeholder={projectData.name}
                      label="Output filepath"
                      autoComplete="off"
                      value={addExtensionToFilepath(filePath, fileFormat)}
                      onChange={(event) => setFilePath(event.target.value)}
                    ></TextField>
                  </div>
                  <br />
                </div>
              </Typography>
            </Dialog.CustomContent>

            <Dialog.Actions>
              <div id="Buttons">
                <Button
                  className="saveButton"
                  onClick={handleReport}
                  disabled={!projectData || !filePath}
                >
                  Create report
                </Button>{" "}
                <Button id="cancelButton" onClick={onClose}>
                  Cancel
                </Button>
              </div>
            </Dialog.Actions>
          </Dialog>
        )}
      </div>
    </>
  );
};

export default ReportDialog;
