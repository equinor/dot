from ..models.filter import Filter
from ..models.opportunity import OpportunityCreate
from ..repositories.opportunity import OpportunityRepository


class OpportunityService:
    def __init__(self, repository: OpportunityRepository):
        self.repository = repository

    def create(self, project_uuid: str, opportunity_data: OpportunityCreate):
        return self.repository.create(project_uuid, opportunity_data)

    def read_opportunities_all(
        self,
        project_uuid: str,
        filter_model: Filter,
    ):
        return self.repository.read_opportunities_all(
            project_uuid=project_uuid,
            vertex_label="opportunity",
            edge_label="contains",
            filter_model=filter_model,
        )

    def read(self, opportunity_uuid: str):
        return self.repository.read(opportunity_uuid)

    def update(self, opportunity_uuid: str, modified_fields: dict):
        return self.repository.update(opportunity_uuid, modified_fields)

    def delete(self, opportunity_uuid: str):
        return self.repository.delete(opportunity_uuid)
