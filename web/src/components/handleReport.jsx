import { saveAs } from "file-saver";
import { exportProject } from "../services/project_api";
import { reportProject } from "../services/project_api";

export const handleReport = async (uuid) => {
  const project_export = await exportProject(uuid).then((response) => {
    console.log("Reporting project: ", JSON.stringify(response));
    const project_json = response;
    const project_name = response.vertices.project.name;
    console.log("Reporting project: ", project_name);

    const blob = new Blob([JSON.stringify(response, null, 4)], {
      type: "application/json",
    });
    saveAs(blob, `${project_name}.json`);
  });
};
