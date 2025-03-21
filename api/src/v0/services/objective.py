from ..models.filter import Filter
from ..models.objective import ObjectiveCreate, ObjectiveUpdate
from ..repositories.objective import ObjectiveRepository


class ObjectiveService:
    def __init__(self, repository: ObjectiveRepository):
        self.repository = repository

    def create(self, project_uuid: str, objective_data: ObjectiveCreate):
        return self.repository.create(
            project_uuid=project_uuid, objective_data=objective_data
        )

    def read_objectives_all(
        self,
        project_uuid: str,
        filter_model: Filter,
    ):
        return self.repository.read_objectives_all(
            project_uuid=project_uuid,
            vertex_label="objective",
            edge_label="contains",
            filter_model=filter_model,
        )

    def read(self, objective_uuid: str):
        return self.repository.read(objective_uuid)

    def update(self, objective_uuid: str, modified_fields: ObjectiveUpdate):
        return self.repository.update(objective_uuid, modified_fields)

    def delete(self, objective_uuid: str):
        return self.repository.delete(objective_uuid)
