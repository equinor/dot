import BaseAPIServices from "./base_api_services";

export const createObjective = async (projectId, body) => {
  console.log("Adding new Objective");
  try {
    const result = await BaseAPIServices.post(
      "/projects/" + projectId + "/objectives",
      {},
      body
    );
    console.log("Project created:", result);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};
export const updateObjective = async (projectId, body) => {
  console.log("Adding new Objective");
  try {
    const result = await BaseAPIServices.patch(
      "/objectives/" + projectId,
      body
    );
    console.log("Objective created:", result);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//get projects
export const allObjectives = async (projectId) => {
  console.log("Page updated");
  try {
    const result = await BaseAPIServices.get(
      "/projects/" + projectId + "/objectives"
    );
    console.log(result);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};
export const readObjectives = async (objectiveId) => {
  console.log("Page updated");
  try {
    const result = await BaseAPIServices.get("/objectives/" + objectiveId);
    console.log(result);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//delete project
export const removeObjective = (opportunityId) => {
  try {
    const result = BaseAPIServices.delete("/objectives/" + opportunityId);
    console.log("Finished deleting");
    return result;
  } catch (error) {
    console.log("Failed Deleting");
    console.error(error);
  }
};
