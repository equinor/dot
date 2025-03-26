import ast
import json

from ....models.issue import CommentData, ProbabilityData
from ....models.vertex import VertexResponse


class FieldParserVertex:
    """Class for parsing the different types of fields existing in the vertices of
    the DataBase"""

    def id(self, data):
        # The id and labels from Gremlins are strings and not list
        if not isinstance(data, str):
            raise TypeError("The id should be a string")
        return data

    def label(self, data):
        # The id and labels from Gremlins are strings and not list
        if not isinstance(data, str):
            raise TypeError("The label should be a string")
        return data

    def string(self, data):
        return data[0]

    def list(self, data):
        if data:
            if data[0]:
                return ast.literal_eval(data[0])
        else:
            return None

    def probability(self, data):
        # default_probability by default. Cannot be empty, but legacy tests...
        if data is None:
            return None
        if data[0] is None or data[0] == "":
            return None
        if data[0] == "null":
            return None
        # if data[0] != "null" and data[0] != "":  # TODO: this depends on how we
        #       store the None data values
        #       in the DB
        try:
            return ProbabilityData.model_validate_json(data[0]).model_dump()
        except Exception:
            raise TypeError("Probability in DataBase is not in a ProbabilityData format")

    def comments(self, data):
        if data is None:
            return None
        if data[0] is None or data[0] == "":
            return None
        if data[0] == "null":
            return None
        validated_comments = []
        if not isinstance(data, list):
            raise TypeError("The data should be a list")
        for item in ast.literal_eval(data[0]):
            try:
                item_json = json.dumps(item)
                validated_comment = CommentData.model_validate_json(
                    item_json
                ).model_dump()
                validated_comments.append(validated_comment)
            except Exception:
                raise TypeError(
                    f"Comment in DataBase is not in a CommentData format: {item}"
                )

        return validated_comments


class GremlinResponseBuilderVertex:
    """
    Class for building vertex data model Responses from a Gremlin payload.
    """

    def _parse_field(self, data: dict) -> dict:
        """Parse fields of vertices existing in the DataBase

        Fields can be:
            - id
            - label
            - string
            - List
            - ProbabilityData
        """
        """T.id and T.label classes to strings"""  # TODO: add description of what is
        #       expected to be returned
        result_dict = {}
        field_parser = FieldParserVertex()

        # Mapping of keys to their corresponding parsing functions
        parse_map = {
            "T.id": field_parser.id,
            "T.label": field_parser.label,
            "alternatives": field_parser.list,
            "tag": field_parser.list,
            "probabilities": field_parser.probability,
            "comments": field_parser.comments,
        }

        for key, value in data.items():
            str_key = str(key)
            if str_key == 'id':
                result_dict[str_key] = parse_map['T.id'](value)
            elif str_key == 'label':
                result_dict[str_key] = parse_map['T.label'](value)
            elif str_key in parse_map:
                result_dict[str_key] = parse_map[str_key](value)
            elif isinstance(value, list) and len(value) == 1:
                result_dict[str_key] = field_parser.string(value)
            else:
                raise ValueError(f"Parser for field '{str_key}' is not defined")

        return result_dict

    def build_item(self, data: list) -> VertexResponse:
        """Build the VertexResponse from input data (scalar)

        Args:
            data (List): data retrieved from the DataBase


        Returns:
            VertexResponse: the response of the vertex
        """
        results_parsed = self._parse_field(data[0])
        return VertexResponse.model_validate(results_parsed)

    def build_list(self, data: list[list]) -> list[VertexResponse]:
        """Build the VertexResponse from input data (List)

        Args:
            data (List): data retrieved from the DataBase

        Returns:
            VertexResponse: the response of the vertex
        """
        results_parsed = [self._parse_field(item) for item in data]
        return [VertexResponse.model_validate(v) for v in results_parsed]

    def build_none(self, data=None) -> None:
        """Build the VertexResponse when it should only return None"""
        return None
