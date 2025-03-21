import re

from ....models.edge import EdgeResponse


class GremlinResponseBuilderEdge:
    """
    Class for building edge data model Responses from a Gremlin payload.
    """

    def _parse_edge(self, edge_results: list) -> dict:
        """parse edge information returned from the DataBase

        The Edge information is a string structured as
            "e[id][outV.id-edge_label->inV.id]"

        Args:
            edge_results (List): the edge information as returned from the DataBase

        Returns:
            Dict: a dictionary containaing the different fields
                id
                label
                uuid
                outV
                inV
        """
        match = re.match(r"e\[(.+)\]\[(.+)-(.+)->(.+)\]", str(edge_results))
        return {
            "id": match.group(1),
            "label": match.group(3),
            "outV": match.group(2),
            "inV": match.group(4),
            "uuid": match.group(1),
        }

    def build_item(self, data: list) -> EdgeResponse:
        """Build the EdgeResponse from input data (scalar)

        Args:
            data (List): data retrieved from the DataBase

        Returns:
            EdgeResponse: the response of the Edge
        """
        results_parsed = self._parse_edge(data[0])  # data is always a list
        return EdgeResponse.model_validate(results_parsed)

    def build_list(self, data: list[list]) -> list[EdgeResponse]:
        """Build the EdgeResponse from input data (List)

        Args:
            data (List): data retrieved from the DataBase

        Returns:
            EdgeResponse: the response of the Edge
        """
        results_parsed = [self._parse_edge(d) for d in data]
        return [EdgeResponse.model_validate(e) for e in results_parsed]

    def build_none(self, data=None) -> None:
        """Build the EdgeResponse when it should only return None"""
        return None
