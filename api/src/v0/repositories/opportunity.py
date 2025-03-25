from ..database.client import DatabaseClient
from ..models.filter import Filter
from ..models.opportunity import (
    OpportunityCreate,
    OpportunityResponse,
    OpportunityUpdate,
)
from ..repositories.edge import EdgeRepository
from ..repositories.vertex import VertexRepository


class OpportunityRepository:
    def __init__(self, client: DatabaseClient):
        self._client = client
        self.builder = client.builder

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
        vertex = VertexRepository(self._client).create("opportunity", opportunity_data)
        EdgeRepository(self._client).create(project_uuid, vertex.uuid, "contains")
        return OpportunityResponse.convert_api_payload_to_response(vertex)

    def read_opportunities_all(
        self,
        project_uuid: str,
        vertex_label: str,
        edge_label: str,
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
        vertex_list = VertexRepository(self._client).read_out_vertex(
            vertex_uuid=project_uuid,
            original_vertex_label=vertex_label,
            edge_label=edge_label,
            filter_model=filter_model,
        )
        return OpportunityResponse.convert_list_api_payloads_to_responses(vertex_list)

    def read(self, opportunity_uuid: str) -> OpportunityResponse:
        """Method to read one opportunity based on the id

        Args:
            opportunity_uuid (str): id of the vertex with the label "opportunity"

        Returns
            OpportunityResponse: Opportunity with all properties
        """
        vertex = VertexRepository(self._client).read(opportunity_uuid)
        return OpportunityResponse.convert_api_payload_to_response(vertex)

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
        vertex = VertexRepository(self._client).update(opportunity_uuid, modified_fields)
        return OpportunityResponse.convert_api_payload_to_response(vertex)

    def delete(self, opportunity_uuid):
        """Deletes the opportunity vertex based on the id and also all in and outgoing
            edges from this vertex

        Args:
            opportunity_uuid (str): id of the opportunity vertex

        Returns
            None
        """
        EdgeRepository(self._client).delete_edge_from_vertex(opportunity_uuid)
        VertexRepository(self._client).delete(opportunity_uuid)
        return
