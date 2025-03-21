import React, { useState, useEffect } from "react";
import { Button, Icon, TextField, NativeSelect } from "@equinor/eds-core-react";
import { save } from "@equinor/eds-icons";
import { Link, useNavigate } from "react-router-dom";
import {
  createProject,
  readProject,
  updateProject,
} from "../services/project_api";
import "../styles/equinor-font.css";
import AppHeader from "../components/NavBar";
import { useProjectContext } from "../components/context";

function ProjectPage() {
  const navigate = useNavigate("");
  const [project, setProject] = useState({});
  const [projectName, setProjectName] = useState(null);
  const [projectDecisionMaker, setProjectDecisionMaker] = useState(null);
  const [projectDescription, setProjectDescription] = useState(null);
  const [projectDecisionDate, setProjectDecisionDate] = useState(null);
  const [projectSensitivityLabel, setProjectSensitivityLabel] = useState(null);
  const [projectUuid, setProjectContext] = useProjectContext();

  project.name = projectName;
  project.description = projectDescription;

  const getProjectData = async () => {
    if (projectUuid === null) {
      return;
    }
    const projectData = await readProject(projectUuid);
    if (projectData) {
      setProject(projectData);
      setProjectName(projectData.name);
      setProjectDescription(projectData.description);
      setProjectDecisionMaker(projectData.decision_maker);
      setProjectDecisionDate(projectData.decision_date);
      setProjectSensitivityLabel(projectData.sensitivity_label);
    }
  };
  const handleSave = async (e) => {
    const updatedProjectData = {};
    updatedProjectData.description = projectDescription;
    updatedProjectData.name = projectName;
    updatedProjectData.decision_date = projectDecisionDate;
    updatedProjectData.decision_maker = projectDecisionMaker;
    updatedProjectData.sensitivity_label = projectSensitivityLabel;

    if (!projectName) {
      alert("Project Name is required.");
      return;
    }

    if (projectUuid) {
      await updateProject(projectUuid, updatedProjectData);
      navigate("/framing");
    } else {
      try {
        const proj = await createProject(updatedProjectData);
        setProjectContext(proj.id);
        navigate("/framing");
      } catch (error) {
        console.error("Error creating project:", error);
        alert("Error creating project. Please try again.");
        return;
      }
    }
  };

  useEffect(() => {
    getProjectData();
  }, []);
  return (
    <>
      <AppHeader />
      <div>
        <h2 className="equinorHeading">Project: {project.name} </h2>
      </div>
      <div id="wrapper">
        <div id="leftContainer">
          <div className="textInputNewProject">
            <TextField
              id="projectName"
              placeholder="Text"
              label="Project Name"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
            />
          </div>
          <div className="textInputNewProject">
            <TextField
              id="decisionMaker"
              placeholder="Text"
              label="Decision Maker"
              value={projectDecisionMaker}
              onChange={(e) => setProjectDecisionMaker(e.target.value)}
            />
          </div>
          <div className="textInputNewProject">
            <TextField
              id="timeline"
              type="date"
              label="Select end date"
              value={projectDecisionDate}
              onChange={(e) => setProjectDecisionDate(e.target.value)}
            />
          </div>
          <div className="textInputNewProject">
            <NativeSelect
              id="sensitivityLevel"
              label="Sensitivity Level"
              value={projectSensitivityLabel}
              onChange={(e) => setProjectSensitivityLabel(e.target.value)}
            >
              <option value="Open">Open</option>
              <option value="Internal">Internal</option>
              <option value="Restricted">Restricted</option>
              <option value="Confidential">Confidential</option>
            </NativeSelect>
          </div>
        </div>
        <div id="rightContainer">
          <div className="textInputNewProject"></div>
          <TextField
            id="description"
            multiline
            rows={10}
            label="Description"
            value={projectDescription}
            onChange={(e) => setProjectDescription(e.target.value)}
          />
        </div>
      </div>
      <div className="createButton">
        <Button id="createProject" onClick={handleSave}>
          <Icon data={save} title="add" />
          Save
        </Button>
      </div>

      {projectUuid && (
        <div className="createButton">
          <Button as={Link} to="/framing">
            Go to Framing
          </Button>
        </div>
      )}
    </>
  );
}

export default ProjectPage;
