import React, { useState, useContext, useEffect } from "react";
import {
  Button,
  Icon,
  Pagination,
  Card,
  Typography,
  Chip,
} from "@equinor/eds-core-react";
import { add, lock, lock_open, download } from "@equinor/eds-icons";
import { Link, Outlet } from "react-router-dom";
import { allProjects, removeProject } from "../services/project_api";
import "../styles/home.css";
import { useProjectContext } from "../components/context";
import { ProjectContext } from "../components/context";
import ProjectDeleteCheck from "../components/deleteCheck";
import ImportDialog from "../components/importDialog";
import { handleExport } from "../components/handleExport";

function HomeScreen() {
  const [projects, setProjects] = useState(null);
  const [page, setPage] = useState(1);
  const [totalItems, setTotalItems] = useState(0);
  const [project_context, setProjectContext] = useProjectContext();

  const fetchData = async () => {
    const updatedData = await allProjects();
    setProjects(updatedData);
    setTotalItems(updatedData.length);
    setProjectContext(null);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handlePageChange = (event, newPage) => {
    setPage(newPage);
  };
  const itemsPerPage = 12;
  const startIndex = (page - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const visibleProjects = Array.isArray(projects)
    ? projects.slice(startIndex, endIndex)
    : [];

  return (
    <>
      <div>
        <h1 className="equinorHeading">
          Welcome to the Decision Optimization Tool!
        </h1>
      </div>
      <div>
        <p className="paragraph">
          DOT (Decision Optimization Tool) is an innovative platform designed to
          enhance decision-making processes. By providing a comprehensive set of
          tools for structured analysis, evaluation, and collaboration, DOT
          empowers cross-disciplinary teams to optimize their decision-modelling
          strategies. The DOT Tool transforms complex decision scenarios into
          clear, actionable insights. Navigate uncertainties with confidence and
          drive informed choices with DOT, your essential companion for
          effective decision optimization.
        </p>
      </div>

      <div className="newProjectButton">
        <Button
          id="projectButton"
          variant="contained-icon"
          aria-label="add action"
          as={Link}
          to="/project"
          onClick={() => {
            setProjectContext(null);
          }}
        >
          <Icon data={add}></Icon>
        </Button>
        <ImportDialog fetchData={fetchData} />
      </div>
      <div className="existingProjectButton">
        {visibleProjects?.map((project) => (
          <div key={project.uuid} className="existingButton">
            <Card
              className="projectCard"
              data-tag={project.uuid}
              onClick={() => {
                setProjectContext(project.uuid);
              }} //local storage of window
              as={Link}
              to="/framing"
            >
              <Card.Header>
                <Card.HeaderTitle>
                  <Typography className="projectCardHeader" variant="h4">
                    {project.name}
                  </Typography>
                  <Typography
                    className="projectDescription"
                    variant="body_short"
                  >
                    {project.description}
                  </Typography>
                </Card.HeaderTitle>
              </Card.Header>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "0.5fr 2fr",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <Card.Actions>
                  <ProjectDeleteCheck project={project} fetchData={fetchData} />
                  <Button
                    data-tag={project.uuid}
                    id="exportButton"
                    variant="ghost"
                    aria-label="export action"
                    onClick={async (event) => {
                      event.preventDefault();
                      const uuid = event.target.getAttribute("data-tag");
                      await handleExport(uuid);
                    }}
                  >
                    <Icon data={download}></Icon>
                  </Button>
                </Card.Actions>
                <Card.Content style={{ display: "flex" }}>
                  <div
                    style={{
                      display: "flex",
                      flexWrap: "wrap",
                      width: "100%",
                      marginLeft: "auto",
                      marginRight: "0",
                      justifyContent: "flex-end",
                    }}
                  >
                    <Chip
                      style={{ marginBottom: "5px", marginRight: "5px" }}
                      variant={
                        project.sensitivity_label === "Open"
                          ? "active"
                          : project.sensitivity_label === "Restricted" ||
                            project.sensitivity_label === "Confidential"
                          ? "error"
                          : "default"
                      }
                    >
                      <Icon
                        data={
                          project.sensitivity_label === "Open"
                            ? lock_open
                            : lock
                        }
                      />
                      {project.sensitivity_label}
                    </Chip>
                  </div>
                </Card.Content>
              </div>
            </Card>
          </div>
        ))}
      </div>
      <div className="homeFooter">
        {itemsPerPage < totalItems && (
          <Pagination
            totalItems={totalItems}
            itemsPerPage={itemsPerPage}
            defaultValue={page}
            onChange={handlePageChange}
          />
        )}
      </div>
    </>
  );
}

export default HomeScreen;
