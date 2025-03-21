import BaseAPIServices from "./base_api_services";

//add influencing edge based on UUID == ID in the new API/DB structure
// could we use just BaseAPIServices.post(...)?
export const addEdge = async (uuid1, uuid2, label) => {
  try {
    const result = await BaseAPIServices.postEdge(
      "/edges/label/" + label,
      uuid1,
      uuid2
    );
    console.log("Adding edge", result);
    return result;
  } catch (error) {
    console.error(error);
    console.error(error.response);
  }
};

//delete issue
export const removeEdgeID = (id) => {
  try {
    const result = BaseAPIServices.delete("/edges/" + id);
    console.log("Finished api call");
    console.log("result ==> " + JSON.stringify(result.data));
    return result;
  } catch (error) {
    console.log("Failed Deleting");
    console.error(error);
  }
};

export const readOutEdges = (vertexId, edgeLabel) => {
  try {
    const result = BaseAPIServices.get(
      "/vertices/" + vertexId + "/edges/label/" + edgeLabel + "/outgoing"
    );
    console.log("Reading outgoing edges");
    return result;
  } catch (error) {
    console.log("Failed reading");
    console.error(error);
  }
};
export const readInEdges = (vertexId, edgeLabel) => {
  try {
    const result = BaseAPIServices.get(
      "/vertices/" + vertexId + "/edges/label/" + edgeLabel + "/incoming"
    );
    console.log("Reading ingoing edges");
    return result;
  } catch (error) {
    console.log("Failed reading");
    console.error(error);
  }
};
