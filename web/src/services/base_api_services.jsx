import axios from "axios";

export const API_BASEURL =
  process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

const API_VERSION = "/latest";

class BaseApiServices {
  async test(path) {
    var array_def_projects;
    return array_def_projects;
  }

  async get(path, params) {
    console.log("path", API_VERSION + path);
    try {
      const response = await axios.get(API_BASEURL + API_VERSION + path, {
        method: "GET",
        params: params,
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      });
      console.log(response);
      return response.data;
    } catch (error) {
      console.error(error);
    }
  }

  async post(path, projectID, input, queryParams = {}) {
    var url_str = API_BASEURL + API_VERSION + path;
    console.log("url_str:" + url_str);

    var json_str = JSON.stringify(input);
    console.log("json_str:" + json_str);

    const params = { project_uuid: projectID, ...queryParams };

    return await axios
      .post(url_str, json_str, {
        params: params,
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
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
    console.log("url_str:" + url_str);

    var json_str = JSON.stringify(input);
    console.log("json_str:" + json_str);

    return await axios
      .post(url_str, json_str, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
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
    console.log("url_str:" + url_str);

    var json_str = JSON.stringify(input);
    console.log("json_str:" + json_str);

    return await axios
      .patch(url_str, json_str, {
        method: "PATCH",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
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
    console.log("url_str:" + url_str);

    var json_str = JSON.stringify(propsDict);
    console.log("json_str:" + json_str);

    return await axios
      .patch(url_str, json_str, {
        method: "PATCH",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
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
    console.log("url_str:" + url_str);

    try {
      const response = await axios.delete(url_str, {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
          "Access-Control-Allow-Origin": "*",
        },
        method: "DELETE",
      });
      console.log("Data ", response.data);
      console.log("Issue deleted");
    } catch (error) {
      console.log("Something went wrong!");
      console.error(error);
      console.log(error.response);
    }
  }

  async postEdge(path, uuid1, uuid2) {
    var url_str = API_BASEURL + API_VERSION + path;
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
