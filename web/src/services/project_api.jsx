import BaseAPIServices from "./base_api_services";

//new project
export const createProject = async (project) => {
  console.log("Adding new Project");
  try {
    const result = await BaseAPIServices.postProj("/projects", project);
    console.log("Project created:", result);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//get projects
export const allProjects = async () => {
  console.log("Page updated here projects");
  try {
    const result = await BaseAPIServices.get("/projects");
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};
export const readProject = async (projectUuid) => {
  console.log("Page updated here");
  try {
    const result = await BaseAPIServices.get("/projects/" + projectUuid);
    console.log(result);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//delete project
export const removeProject = (projectUuid) => {
  try {
    const result = BaseAPIServices.delete("/projects/" + projectUuid);
    console.log("Finished deleting");
    return result;
  } catch (error) {
    console.log("Failed Deleting");
    console.error(error);
  }
};

//export project
export const exportProject = (projectID) => {
  try {
    const result = BaseAPIServices.get("/projects/" + projectID + "/export");
    return result;
  } catch (error) {
    console.log("Failed Exporting");
    console.error(error);
  }
};

//new project
export const importProject = async (project) => {
  console.log("Adding new Project");
  try {
    const result = await BaseAPIServices.postProj("/projects/import", project);
    console.log("Project created:", result);
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//update project
export const updateProject = async (project_uuid, project) => {
  console.log("Project ", project_uuid, " is updating ...");
  try {
    const result = await BaseAPIServices.patch(
      "/projects/" + project_uuid,
      project
    );
    console.log("Finished updating");
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};
