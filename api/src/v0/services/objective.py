from ..models.filter import Filter
from ..models.objective import ObjectiveCreate, ObjectiveResponse, ObjectiveUpdate
from ..repositories.objective import ObjectiveRepository


class ObjectiveService:
    def __init__(self, repository: ObjectiveRepository):
        self.repository = repository

    def create(
        self, project_uuid: str, objective_data: ObjectiveCreate
    ) -> ObjectiveResponse:
        """Method to create a new objective connected to a project vertex

            Creates vertex with the label "objective" and the properties of
            objective_data
            Creates an edge between the project vertex specified by project_uuid
            and the newly create objective vertex

        Args:
            project_uuid (str): id of the project vertex the new objective will be
                                connected to
            objective_data (ObjectiveCreate): contains all properties for the objective

        Returns:
            ObjectiveResponse: Created Objective with the objective_data as
                               ObjectiveData
        """
        return self.repository.create(
            project_uuid=project_uuid, objective_data=objective_data
        )

    def read_objectives_all(
        self,
        project_uuid: str,
        filter_model: Filter,
    ) -> list[ObjectiveResponse]:
        """Read all objectives connected to one project with filter possibilities

        Args:
            project_uuid (str): id of the project vertex
            vertex_label (str): label of the vertices of interest
            edge_label (str): edge_label to clarify the connection between the project
                              node and objective node, should always be "contains" in
                              this method (default "contains")
            filter_model (Filter (BaseModel))
                contains a dict with different properties for filtering, like hierarchy,
                tag, and description

        Returns
            List[ObjectiveResponse]: List of Objectives which satisfy the condition to
                                     be connected to the Project vertex with a
                                     "contains" edge and have the label "objective" and
                                     satisfy the filters when the filter_model is given
        """
        return self.repository.read_objectives_all(
            project_uuid=project_uuid,
            vertex_label="objective",
            edge_label="contains",
            filter_model=filter_model,
        )

    def read(self, objective_uuid: str) -> ObjectiveResponse:
        """Method to read one objective based on the id

        Args:
           objective_uuid (str): id of the vertex with the label "objective"

        Returns
            ObjectiveResponse: Objective with all properties
        """
        return self.repository.read(objective_uuid)

    def update(
        self, objective_uuid: str, modified_fields: ObjectiveUpdate
    ) -> ObjectiveResponse:
        """Updates the specified objective based on the id with the new objective_data

        Args:
            objective_uuid (str): id of the objective vertex
            modified_fields (ObjectiveUpdate): contains properties of the objective

        Returns:
            ObjectiveResponse: Objective with the objective_data as ObjectiveData
        """
        return self.repository.update(objective_uuid, modified_fields)

    def delete(self, objective_uuid: str) -> None:
        """Deletes the objective vertex based on the id and also all in and outgoing
            edges from this vertex

        Args:
            objective_uuid (str): id of the objective vertex

        Returns:
            None
        """
        return self.repository.delete(objective_uuid)
