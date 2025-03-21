import { React, createContext, useContext, useState, useEffect } from "react";

export const ProjectContext = createContext(undefined);

export function useProjectContext() {
  const project = useContext(ProjectContext);
  if (project === undefined) {
    throw new Error(
      "useProjectContext must be used with a ProjectContext - Project undefined"
    );
  }
  return project;
}

export function ProjectProvider({ children }) {
  const [project, setProjectContext] = useState(() => {
    const storedProject = localStorage.getItem("project");
    return storedProject ? JSON.parse(storedProject) : null;
  });

  useEffect(() => {
    localStorage.setItem("project", JSON.stringify(project));
  }, [project]);

  return (
    <ProjectContext.Provider value={[project, setProjectContext]}>
      {children}
    </ProjectContext.Provider>
  );
}
