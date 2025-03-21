import BaseAPIServices from "./base_api_services";

//delete issue -- new API ok
export const removeIssue = (issueID) => {
  try {
    const result = BaseAPIServices.delete("/issues/" + issueID);
    console.log("Finished api call");
    console.log("result ==> " + JSON.stringify(result.data));
    return result;
  } catch (error) {
    console.log("Failed Deleting");
    console.error(error);
  }
};

//add issue -- new API ok
export const addIssue = async (projectID, issue) => {
  console.log("Adding new Issue...");
  try {
    const result = await BaseAPIServices.post(
      "/projects/" + projectID + "/issues",
      {},
      issue
    );
    console.log(result, "Finished adding new Issue");
    console.log("result ==> " + JSON.stringify(result));
    return result;
  } catch (error) {
    console.log(error);
  }
};
//merge issue
export const mergeIssue = async (projectID, sourceIssue, destinationIssue) => {
  console.log("Merging Issues...");
  const payload = {
    source_issue: sourceIssue,
    destination_issue: destinationIssue,
  };

  try {
    const result = await BaseAPIServices.post(
      "/projects/" + projectID + "/merge",
      {},
      payload
    );
    console.log(result, "Finished adding new Issue");
    console.log("result ==> " + JSON.stringify(result));
    return result;
  } catch (error) {
    console.log(error);
  }
};
//unmerge issue
export const unMergeIssue = async (projectID, mergedIssueUUID) => {
  console.log("unmerging Issues...");
  const payload = {};

  try {
    const result = await BaseAPIServices.post(
      "/projects/" + projectID + "/un-merge/issues/" + mergedIssueUUID,
      {},
      payload
    );
    console.log(result, "Finished adding new Issue");
    console.log("result ==> " + JSON.stringify(result));
    return result;
  } catch (error) {
    console.log(error);
  }
};

//get issues -- new API OK
export const readIssues = async (projectID, params = null) => {
  console.log("Page updated");
  try {
    const result = await BaseAPIServices.get(
      "/projects/" + projectID + "/issues",
      params
    );
    console.log(result);
    console.log("Finished reading", params);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//get issue -- new API ok
export const readIssue = async (uuid) => {
  console.log(uuid);
  try {
    const result = await BaseAPIServices.get("/issues/" + uuid);
    console.log(result);
    console.log("Finished reading", uuid);
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};

//update issues -- new API ok
export const updateIssue = async (issueId, updatedDict) => {
  console.log("Issue ", issueId, " is updating ...");
  try {
    const result = await BaseAPIServices.patch(
      "/issues/" + issueId,
      updatedDict
    );
    console.log("Finished updating");
    return result;
  } catch (error) {
    console.log(error);
    console.error(error.response);
  }
};
