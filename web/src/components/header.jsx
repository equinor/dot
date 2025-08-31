import React, { useState, useRef, useContext, useEffect } from "react";
import {
  Button,
  Icon,
  TopBar,
  Popover,
  Typography,
  Chip,
} from "@equinor/eds-core-react";
import {
  home,
  apps,
  account_circle,
  notifications,
  help_outline,
  file_description,
  download,
  file,
} from "@equinor/eds-icons";
import { Link, Outlet } from "react-router-dom";
import { useProjectContext } from "./context";
import { readProject } from "../services/project_api";
import { handleExport } from "./handleExport";
import ReportDialog from "../components/reportDialog";

function Header() {
  const [isOpen, setIsOpen] = useState(false);
  const [project_data, setProjectData] = useState(null);
  const anchorRef = useRef(null);
  const openPopover = () => setIsOpen(true);
  const closePopover = () => setIsOpen(false);
  const [project, setProjectContext] = useProjectContext();

  const [isReportDialogOpen, setIsReportDialogOpen] = useState(false); // State to control dialog visibility
  const [reportDialogArgs, setReportDialogArgs] = useState({}); // State to store dialog arguments

  const openReportDialog = (args) => {
    setReportDialogArgs(args); // Store the arguments in state
    setIsReportDialogOpen(true); // Open the dialog with the UUID
  };

  const closeReportDialog = () => {
    setIsReportDialogOpen(false); // Close the dialog
    setReportDialogArgs({}); // Clear the arguments
  };

  const fetchData = async () => {
    if (project) {
      const project_read = await readProject(project);
      setProjectData(project_read);
    } else {
      setProjectData(null);
    }
  };

  useEffect(() => {
    console.log("Header project:", project);
    fetchData();
  }, [project]);

  return (
    <>
      <TopBar>
        <TopBar.Header className="icons">
          <Button
            aria-haspopup
            aria-expanded={isOpen}
            aria-label="app launcher"
            ref={anchorRef}
            variant="ghost_icon"
            onClick={openPopover}
          >
            <Icon data={apps} />
          </Button>
          <Popover
            anchorEl={anchorRef.current}
            open={isOpen}
            onClose={closePopover}
            placement="top"
            trapFocus
            withinPortal
          >
            <Popover.Content>
              <Button
                className="homeButton"
                variant="ghost_icon"
                as={Link}
                to="/"
              >
                <Icon data={home} />
              </Button>
              <div>
                {project_data ? (
                  <div>
                    <Button
                      className="projectButton"
                      variant="ghost_icon"
                      as={Link}
                      to="/project"
                    >
                      <Icon data={file_description} />
                    </Button>
                    <Button
                      className="exportButton"
                      variant="ghost_icon"
                      onClick={async () => {
                        try {
                          await handleExport(project_data.uuid);
                        } catch (error) {
                          console.error("Error exporting project:", error);
                        }
                      }}
                    >
                      <Icon data={download} />
                    </Button>
                    <Button
                      className="reportButton"
                      variant="ghost_icon"
                      onClick={async (event) => {
                        event.preventDefault();
                        openReportDialog({ uuid: project_data.uuid });
                      }}
                    >
                      <Icon data={file} />
                    </Button>
                    {isReportDialogOpen && (
                      <ReportDialog
                        uuid={reportDialogArgs.uuid}
                        onClose={closeReportDialog}
                      />
                    )}
                  </div>
                ) : null}
              </div>
            </Popover.Content>
          </Popover>
        </TopBar.Header>
        <TopBar.CustomContent>
          <div className="customContent">
            {project_data ? (
              <div style={{ display: "flex", alignItems: "center" }}>
                <Typography>Project: {project_data.name}</Typography>
                <Chip style={{ marginLeft: "10px" }}>
                  {project_data.sensitivity_label}
                </Chip>
              </div>
            ) : (
              <Typography>Decision Optimization Tool</Typography>
            )}
          </div>
        </TopBar.CustomContent>
        <TopBar.Actions>
          <div className="icons">
            <Button variant="ghost_icon">
              <Icon data={account_circle} />
            </Button>
            <Button variant="ghost_icon">
              <Icon data={notifications} />
            </Button>
            <Button
              variant="ghost_icon"
              as={Link}
              target="_blank"
              to="https://equinor.github.io/dot/"
            >
              <Icon data={help_outline} />
            </Button>
          </div>
        </TopBar.Actions>
      </TopBar>
    </>
  );
}

export default Header;
