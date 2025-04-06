import axios from "axios";
import { getAccessToken } from "../auth";

export const API_BASEURL ="/api"

const API_VERSION = "latest";

class BaseApiServices {
  async test(path) {
    var array_def_projects;
    return array_def_projects;
  }
  async get(path, params) {  
    console.log(window.injectEnv);
    try {
      const accessToken = await getAccessToken()
      
      const response = await axios.get(API_BASEURL + API_VERSION + path, {
        method: "GET",
        params: params,

        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authorization":`Bearer ${accessToken}`
        },
      });
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }

  async post(path, projectID, input, queryParams = {}) {
    var url_str = API_BASEURL + API_VERSION + path;
    var json_str = JSON.stringify(input);
    const params = { project_uuid: projectID, ...queryParams };
    const accessToken = await getAccessToken()
    return await axios
      .post(url_str, json_str, {
        params: params,
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authorization":`Bearer ${accessToken}`

        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error("error ==>" + error.response);
        return null;
      });
  }

  async postProj(path, input) {
    var url_str = API_BASEURL + API_VERSION + path;
    var json_str = JSON.stringify(input);
    const accessToken = await getAccessToken()
    return await axios
      .post(url_str, json_str, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authorization":`Bearer ${accessToken}`

        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error("error ==>" + error);
        return null;
      });
  }

  async patch(path, input) {
    var url_str = API_BASEURL + API_VERSION + path;
    var json_str = JSON.stringify(input);
    const accessToken = await getAccessToken()
    return await axios
      .patch(url_str, json_str, {
        method: "PATCH",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authorization":`Bearer ${accessToken}`

        },
      })
      .then((response) => console.log("Done ", response.data))
      .catch((error) => {
        console.error(error);
        console.error(error.response);
      });
  }

  async patchProps(path, issueID, propsDict) {
    var url_str = API_BASEURL + API_VERSION + path + "/" + issueID;
    var json_str = JSON.stringify(propsDict);
    const accessToken = await getAccessToken()
    return await axios
      .patch(url_str, json_str, {
        method: "PATCH",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authorization":`Bearer ${accessToken}`

        },
      })
      .then((response) => console.log("Done ", response.data))
      .catch((error) => {
        console.error(error);
        console.error(error.response);
      });
  }

  async delete(path) {
    var url_str = API_BASEURL + API_VERSION + path;
    try {
      const accessToken = await getAccessToken()
      const response = await axios.delete(url_str, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authorization":`Bearer ${accessToken}`

        },
        method: "DELETE",
      });
    } catch (error) {
      console.log("Something went wrong!");
      console.error(error);
      console.log(error.response);
    }
  }

  async postEdge(path, uuid1, uuid2) {
    var url_str = API_BASEURL + API_VERSION + path;
    const accessToken = await getAccessToken()
    return await axios
      .post(url_str, "", {
        params: {
          out_vertex_uuid: uuid1,
          in_vertex_uuid: uuid2,
        },
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          "Authorization":`Bearer ${accessToken}`

        },
      })
      .then((response) => response.data)
      .catch((error) => {
        console.error("error ==>" + error);
        return null;
      });
  }
}
export default new BaseApiServices();
