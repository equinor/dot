import BaseAPIServices from "./base_api_services";

//get graph db data
export const readGraphData = async (projectID) => {
  console.log("Retrieving GraphData; ProjectID:", projectID);
  try {
    const result = await BaseAPIServices.get(
      "/structures/readGraphData",
      projectID
    );
    console.log(result);
    console.log("Finished reading graph data");
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//get ID
export const readInfluenceDiagram = async (projectID) => {
  console.log("Retrieving ID GraphData; ProjectID:", projectID);
  try {
    const result = await BaseAPIServices.get(
      "/projects/" + projectID + "/influence-diagram"
    );
    console.log(result);
    console.log("Finished reading graph data");
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//get ID
export const id2dt = async (projectID) => {
  console.log("Transforming ID 2 DT; ProjectID:", projectID);
  try {
    const result = await BaseAPIServices.get(
      "/projects/" + projectID + "/decision-tree"
    );
    console.log(result);
    console.log("Finished reading graph data");
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};
