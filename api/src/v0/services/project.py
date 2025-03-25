from ..models.project import ProjectCreate, ProjectResponse, ProjectUpdate
from ..repositories.project import ProjectRepository


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def create(self, project_data: ProjectCreate) -> ProjectResponse:
        """Method to create a new project vertex

            Creates vertex with the label "project" and the properties of project_data

        Args:
            project_data (ProjectCreate): contains all properties for the project

        Returns
            ProjectResponse: Created Project with the project_data as ProjectCreate
        """
        return self.repository.create(project_data)

    def read_projects_all(self) -> list[ProjectResponse]:
        """Reads all project vertices

        Args:
            None

        Returns
            List[ProjectResponse]: List of Projects in the database
        """
        return self.repository.all()

    def read(self, project_uuid: str) -> ProjectResponse:
        """Method to read one project based on the id

        Args:
            project_uuid (str): id of the vertex with the label "project"'

        Returns
            ProjectResponse: Project with all properties
        """
        return self.repository.read(project_uuid)

    def export_project(self, project_uuid: str) -> dict:
        """Method to export one project based on the id in JSON format

        Args
            project_uuid (str): id of the vertex with the label "project"'

        Returns
            json_dict: JSON dictionary containing the project data
        """
        return self.repository.export_project(project_uuid)

    def import_project(self, project_json: dict) -> None:
        """Method to import a project in JSON format

        Args:
            project_json (dict): JSON dictionary with the project data

        Returns
            None
        """
        return self.repository.import_project(project_json)

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
        return self.repository.update(project_uuid, modified_fields)

    def delete(self, project_uuid: str) -> None:
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
        return self.repository.delete(project_uuid)
