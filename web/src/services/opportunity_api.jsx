import BaseAPIServices from "./base_api_services";

export const createOpportunity = async (projectId, body) => {
  console.log("Adding new Opportunity");
  try {
    const result = await BaseAPIServices.post(
      "/projects/" + projectId + "/opportunities",
      {},
      body
    );
    console.log("Opportunity created:", result);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};
export const updateOpportunity = async (projectId, body) => {
  console.log("Adding new Opportunity");
  try {
    const result = await BaseAPIServices.patch(
      "/opportunities/" + projectId,
      body
    );
    console.log("Opportunity created:", result);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//get projects
export const allOpportunities = async (projectId) => {
  console.log("Page updated");
  try {
    const result = await BaseAPIServices.get(
      "/projects/" + projectId + "/opportunities"
    );
    console.log(result);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};
export const readOpportunities = async (opportunityId) => {
  console.log("Page updated");
  try {
    const result = await BaseAPIServices.get("/opportunities/" + opportunityId);
    console.log(result);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//delete project
export const removeOpportunity = (opportunityId) => {
  try {
    const result = BaseAPIServices.delete("/opportunities/" + opportunityId);
    console.log("Finished deleting");
    return result;
  } catch (error) {
    console.log("Failed Deleting");
    console.error(error);
  }
};
