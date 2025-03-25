from ..models.filter import Filter
from ..models.opportunity import (
    OpportunityCreate,
    OpportunityResponse,
    OpportunityUpdate,
)
from ..repositories.opportunity import OpportunityRepository


class OpportunityService:
    def __init__(self, repository: OpportunityRepository):
        self.repository = repository

    def create(
        self, project_uuid: str, opportunity_data: OpportunityCreate
    ) -> OpportunityResponse:
        """Method to create a new opportunity connected to a project vertex

            Creates vertex with the label "opportunity" and the properties of
            opportunity_data
            Creates an edge between the project vertex specified by project_uuid and the
            newly create opportunity vertex

        Args:
            project_uuid (str): id of the project vertex the new opportunity will be
                                connected to
            opportunity_data (OpportunityCreate): contains all properties for the
                                                opportunity

        Returns:
            OpportunityResponse: Created Opportunity with the opportunity_data as
            OpportunityCreate
        """
        return self.repository.create(project_uuid, opportunity_data)

    def read_opportunities_all(
        self,
        project_uuid: str,
        filter_model: Filter,
    ) -> list[OpportunityResponse]:
        """Read all opportunitys connected to one project with filter possibilities

        Args:
            project_uuid (str): id of the project vertex
            vertex_label (str): label of the vertices of interest
            edge_label (str):  edge_label to clarify the connection between the project
                               node and opportunity node, should always be "contains"
                               in this method (default "contains")
            filter_model (Filter(BaseModel)): contains a dict with different properties
                                              for filtering, like tag and description

        Returns
            List[OpportunityResponse]: List of Opportunitys which satisfy the condition
                                       to be connected to the Project vertex with a
                                       "contains" edge and have the label "opportunity"
                                       and satisfy the filters when the filter_model is
                                       given
        """
        return self.repository.read_opportunities_all(
            project_uuid=project_uuid,
            vertex_label="opportunity",
            edge_label="contains",
            filter_model=filter_model,
        )

    def read(self, opportunity_uuid: str) -> OpportunityResponse:
        """Read all opportunitys connected to one project with filter possibilities

        Args:
            project_uuid (str): id of the project vertex
            vertex_label (str): label of the vertices of interest
            edge_label (str):  edge_label to clarify the connection between the project
                               node and opportunity node, should always be "contains"
                               in this method (default "contains")
            filter_model (Filter(BaseModel)): contains a dict with different properties
                                              for filtering, like tag and description

        Returns
            List[OpportunityResponse]: List of Opportunitys which satisfy the condition
                                       to be connected to the Project vertex with a
                                       "contains" edge and have the label "opportunity"
                                       and satisfy the filters when the filter_model is
                                       given
        """
        return self.repository.read(opportunity_uuid)

    def update(
        self, opportunity_uuid: str, modified_fields: OpportunityUpdate
    ) -> OpportunityResponse:
        """Updates the specified opportunity based on the id with the new
            opportunity_data

        Args:
            opportunity_uuid (str): id of the opportunity vertex
            modified_fields (OpportunityUpdate): contains properties of the opportunity

        Returns
            OpportunityResponse: Opportunity with the opportunity_data as
                                 OpportunityData
        """
        return self.repository.update(opportunity_uuid, modified_fields)

    def delete(self, opportunity_uuid: str) -> None:
        """Deletes the opportunity vertex based on the id and also all in and outgoing
            edges from this vertex

        Args:
            opportunity_uuid (str): id of the opportunity vertex

        Returns
            None
        """
        return self.repository.delete(opportunity_uuid)
