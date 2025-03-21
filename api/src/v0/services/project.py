from ..models.project import ProjectCreate, ProjectUpdate
from ..repositories.project import ProjectRepository


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def create(self, project_data: ProjectCreate):
        return self.repository.create(project_data)

    def read_projects_all(self):
        return self.repository.all()

    def read(self, project_uuid: str):
        return self.repository.read(project_uuid)

    def export_project(self, project_uuid: str):
        return self.repository.export_project(project_uuid)

    def import_project(self, project_json: dict):
        return self.repository.import_project(project_json)

    def delete(self, project_uuid: str):
        return self.repository.delete(project_uuid)

    def update(self, project_uuid: str, modified_fields: ProjectUpdate):
        return self.repository.update(project_uuid, modified_fields)
