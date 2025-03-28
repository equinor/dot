from itertools import chain

from ..database.client import DatabaseClient
from ..models.issue import IssueCreate
from ..models.meta import VertexMetaData
from ..models.objective import ObjectiveCreate
from ..models.opportunity import OpportunityCreate
from ..models.project import ProjectCreate, ProjectResponse, ProjectUpdate
from ..repositories.edge import EdgeRepository
from ..repositories.issue import IssueRepository
from ..repositories.objective import ObjectiveRepository
from ..repositories.opportunity import OpportunityRepository
from ..repositories.vertex import VertexRepository


class ProjectRepository:
    def __init__(self, client: DatabaseClient):
        self._client = client
        self.builder = client.builder

    def create(self, project_data: ProjectCreate) -> ProjectResponse:
        """Method to create a new project vertex

            Creates vertex with the label "project" and the properties of project_data

        Args:
            project_data (ProjectCreate): contains all properties for the project

        Returns
            ProjectResponse: Created Project with the project_data as ProjectCreate
        """
        vertex = VertexRepository(self._client).create("project", project_data)
        return ProjectResponse.convert_api_payload_to_response(vertex)

    def all(self) -> list[ProjectResponse]:
        """Reads all project vertices

        Args:
            None

        Returns
            List[ProjectResponse]: List of Projects in the database
        """
        vertex_list = VertexRepository(self._client).all("project")
        return ProjectResponse.convert_list_api_payloads_to_responses(vertex_list)

    def read(self, project_uuid: str) -> ProjectResponse:
        """Method to read one project based on the id

        Args:
            project_uuid (str): id of the vertex with the label "project"'

        Returns
            ProjectResponse: Project with all properties
        """
        vertex = VertexRepository(self._client).read(project_uuid)
        return ProjectResponse.convert_api_payload_to_response(vertex)

    def _filter_non_empty_fields(
        self, data: list[dict] | dict, exclude_keys: None | list[str] = None
    ) -> list[dict] | dict:
        """Filter non empty data from dictionaries

            Remove items for which the value is either None or an empty string
            and is not specified as to be kept.

        Args:
            data (list[dict] | dict): data to filter
            exclude_keys (None | list[str], optional): list of keys to be kept
            even when empty. Defaults to None.

        Returns:
            list[dict] | dict: input data without filtered items.
        """
        if exclude_keys is None:
            exclude_keys = []
        if isinstance(data, dict):
            return {
                k: v
                for k, v in data.items()
                if v is not None and v != "" and k not in exclude_keys
            }
        elif isinstance(data, list):
            return [self._filter_non_empty_fields(item, exclude_keys) for item in data]
        else:
            return data

    def export_project(self, project_uuid: str) -> dict:
        """Method to export one project based on the id in JSON format

        Args
            project_uuid (str): id of the vertex with the label "project"'

        Returns
            json_dict: JSON dictionary containing the project data
        """
        project = VertexRepository(self._client).read(project_uuid)
        # all issues (through "contains" edge) of the project
        objectives_nodes = VertexRepository(self._client).read_out_vertex(
            project_uuid,
            original_vertex_label="objective",
            edge_label="contains",
        )
        opportunities_nodes = VertexRepository(self._client).read_out_vertex(
            project_uuid,
            original_vertex_label="opportunity",
            edge_label="contains",
        )
        issue_nodes = VertexRepository(self._client).read_out_vertex(
            project_uuid, original_vertex_label="issue", edge_label="contains"
        )
        # merged issues of the project, through "merged_into" edge into one of the nodes
        merged_issues = []
        for issue in issue_nodes:
            merged_issues.extend(
                VertexRepository(self._client).read_in_vertex(
                    issue.id, edge_label="merged_into"
                )
            )
        # all edges of the project, e.g. "contains", "merged_into", "influences"
        # basically all which are connected to some node which is connected to the
        # project
        contain_edges = EdgeRepository(self._client).read_all_edges_from_project(
            project_uuid, edge_label="contains"
        )  # contains edges
        influence_edges = EdgeRepository(self._client).read_all_edges_from_project(
            project_uuid, edge_label="influences"
        )
        merged_edges = EdgeRepository(self._client).read_all_edges_from_project(
            project_uuid, edge_label="merged_into"
        )
        has_vm_edges = EdgeRepository(self._client).read_all_edges_from_project(
            project_uuid, edge_label="has_value_metric"
        )

        # can we get these keys from somewhere else?
        metadata = VertexMetaData()
        metadata_keys = metadata.model_dump().keys()
        # ["version", "timestamp", "date", "ids"]

        # Create JSON dictionary
        json_dict = {
            "vertices": {
                "project": self._filter_non_empty_fields(
                    project.model_dump(),
                    exclude_keys=metadata_keys,
                ),
                "objectives": [
                    self._filter_non_empty_fields(
                        obj.model_dump(), exclude_keys=metadata_keys
                    )
                    for obj in objectives_nodes
                ],
                "opportunities": [
                    self._filter_non_empty_fields(
                        opp.model_dump(), exclude_keys=metadata_keys
                    )
                    for opp in opportunities_nodes
                ],
                "issues": [
                    self._filter_non_empty_fields(
                        issue.model_dump(), exclude_keys=metadata_keys
                    )
                    for issue in issue_nodes
                ],
                "merged_issues": [
                    self._filter_non_empty_fields(
                        merged.model_dump(), exclude_keys=metadata_keys
                    )
                    for merged in merged_issues
                ],
            },
            "edges": [
                edge.model_dump()
                for edge in chain(
                    contain_edges, influence_edges, merged_edges, has_vm_edges
                )
            ],
        }

        # Write JSON dictionary to file - Handled in frontend - saved to downloads folder
        # print(f"Exporting project {project.model_dump()['name']} to JSON")
        # file_name = project.model_dump()['name'].replace(" ", "_")
        # downloads_folder = ""
        # file_path = os.path.join(downloads_folder, f"{file_name}.json")
        # with open(file_path, "w") as file:
        #    json.dump(json_dict, file)

        return json_dict

    def _remove_contains_edge(self, uuid: str) -> None:
        """Remove incoming edges with labels "contains" to a vertex

        Args:
            uuid (str): UUID of the vertex

        Returns:
            None
        """
        contains_edge = EdgeRepository(self._client).read_in_edge_to_vertex(
            edge_label="contains", vertex_uuid=uuid
        )  # EdgeResponse
        contains_edge_id = contains_edge[0].model_dump()
        EdgeRepository(self._client).delete(contains_edge_id["id"])
        return None

    def _create_project_components_vertices(
        self, vertices: list | dict, label: str, project_uuid: str, project_json: dict
    ) -> None:
        """Create vertices contained in a project and update uuids of edges

        Args:
            vertices (list | dict): vertices to be created as json
            label (str): label of the vertice to create
            project_uuid (str): UUID of the project
            project_json (dict): The full project data as json

        Returns:
            None
        """
        for vertex in vertices:
            vertex.pop("label")
            id = vertex.pop("id")
            if label == "objectives":
                created_vertex = ObjectiveRepository(self._client).create(
                    project_uuid, ObjectiveCreate.model_validate(vertex)
                )
            elif label == "opportunities":
                created_vertex = OpportunityRepository(self._client).create(
                    project_uuid, OpportunityCreate.model_validate(vertex)
                )
            elif label == "issues":
                created_vertex = IssueRepository(self._client).create(
                    project_uuid, IssueCreate.model_validate(vertex)
                )
            elif label == "merged_issues":
                created_vertex = IssueRepository(self._client).create(
                    project_uuid, IssueCreate.model_validate(vertex)
                )
                self._remove_contains_edge(created_vertex.uuid)
            # Update the vertex id in the edges
            for edge in project_json["edges"]:
                if edge["outV"] == id:
                    edge["outV"] = created_vertex.uuid
                elif edge["inV"] == id:
                    edge["inV"] = created_vertex.uuid
        return None

    def import_project(self, project_json: dict):
        """Method to import a project in JSON format

        Args:
            project_json (dict): JSON dictionary with the project data

        Returns
            None
        """
        # TODO: check the JSON format
        project = project_json["vertices"]["project"]
        project.pop("label")
        id = project.pop("id")
        project = ProjectCreate.model_validate(project)
        # project_vertex = self._create_project_from_dict(project)
        project_vertex = self.create(project)
        # project_vertex = VertexRepository(self._client).create("project", project)
        # Update the project vertex id in the edges
        for edge in project_json["edges"]:
            if edge["outV"] == id:
                edge["outV"] = project_vertex.uuid
        # Create all other vertices
        for label, vertices in project_json["vertices"].items():
            if label == "project":
                continue
            self._create_project_components_vertices(
                vertices, label, project_vertex.uuid, project_json
            )
        # Create all edges
        for edge in project_json["edges"]:
            if edge["label"] == "contains":
                # already created
                continue
            else:
                EdgeRepository(self._client).create(
                    edge_label=edge["label"],
                    out_vertex_uuid=edge["outV"],
                    in_vertex_uuid=edge["inV"],
                )
        return

    def update(
        self, project_uuid: str, modified_fields: ProjectUpdate
    ) -> ProjectResponse:
        """Updates the specified project based on the id with the new project_data

        Args:
            project_uuid (str): id of the project vertex
            modified_fields (ProjectUpdate): contains properties of the project

        Returns
            ProjectResponse: Project with the project_data as ProjectUpdate
        """
        vertex = VertexRepository(self._client).update(project_uuid, modified_fields)
        return ProjectResponse.convert_api_payload_to_response(vertex)

    def delete(self, project_uuid: str):
        """Gets all vertices connected (via edge with label "contains") to the project
             vertex with the id = project_uuid

            Deletes all edges from these vertices and deletes afterwards all vertices
            connected to the project
            Deletes the project vertex based on the id

        Args
            project_uuid (str): id of the project vertex

        Returns
            None
        """
        vertex_list = VertexRepository(self._client).read_out_vertex(
            project_uuid, edge_label="contains"
        )

        # merged issues of the project, through "merged_into" edge into one of the nodes
        merged_issues = []
        for issue in vertex_list:
            merged_issues.extend(
                VertexRepository(self._client).read_in_vertex(
                    issue.id, edge_label="merged_into"
                )
            )
        vertex_list.extend(merged_issues)
        for v in vertex_list:
            EdgeRepository(self._client).delete_edge_from_vertex(v.id)
            VertexRepository(self._client).delete(v.id)
        VertexRepository(self._client).delete(project_uuid)
        return
