import { saveAs } from "file-saver";
import { exportProject } from "../services/project_api";

export const handleExport = async (uuid) => {
  const project_export = await exportProject(uuid).then((response) => {
    console.log("Exporting project: ", JSON.stringify(response));
    const project_json = response;
    const project_name = response.vertices.project.name;
    console.log("Exporting project: ", project_name);

    const blob = new Blob([JSON.stringify(response, null, 4)], {
      type: "application/json",
    });
    saveAs(blob, `${project_name}.json`);
  });
};
