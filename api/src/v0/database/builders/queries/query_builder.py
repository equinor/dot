import json

TRANSFORM_QUERY_STRING: str = ".valueMap(true)"


class GremlinStringQueryBuilder:
    """
    Base class for building Gremlin queries using string formatting.

    Args:
        graph_name (str): Name of the graph to query. Defaults to "g".
        transform_query (str): Gremlin step to transform results. Defaults to
                               ".valueMap(true)".
    """

    def __init__(
        self,
        graph_name: str = "g",
        transform_query: str = TRANSFORM_QUERY_STRING,
    ) -> None:
        """
        Initializes a GremlinStringQueryBuilder instance.

        Args:
            graph_name (str, optional): Name of the graph to query. Defaults to "g".
            transform_query (str, optional): Gremlin step to transform results.
                                             Defaults to ".valueMap(true)".
        """

        self.transform_query: str = transform_query
        self.graph_name: str = graph_name

    def filter_query(self, filter_dict: dict[str, str]) -> str:
        """
        Generates a Gremlin query string for property filtering using
            `.has('key', 'value')`.

        Args:
            filter_dict (dict[str, str]): Dictionary of key-value pairs for filtering.

        Returns:
            str: Gremlin query string with `.has('key', 'value')` filtering steps.
        """

        query = ""
        if filter_dict and any(v is not None for v in filter_dict.values()):
            for k, v in filter_dict.items():
                if v is not None:
                    query += f".has('{k}', '{v}')"
                # TODO: how to get a list into the model and then also as a query
                #       parameter? not possible in pydantic v2?
            # https://stackoverflow.com/questions/62468402/query-parameters-from-pydantic-model
        return query

    def filter_label_query(self, label: str) -> str:
        """
        Generates a Gremlin query string for filtering by label using
            `.hasLabel('label')`.

        Args:
            label (str): Label to filter by.

        Returns:
            str: Gremlin query string with `.hasLabel('label')` filtering step.
        """

        return f".hasLabel('{label}')"

    # TODO: what whenvalue is empty?
    def _parse_property_as_is(self, key, value):
        return f".property({key}, '{value}')"

    def _parse_property_as_empty(self, key, value):
        return f".property('{key}', '')"

    def _parse_property_as_simple_string(self, key, value):
        return f".property('{key}', '{value}')"

    def _parse_property_as_multiline_string(self, key, value):
        return f".property('{key}', '''{value}''')"

    def _parse_property_as_iterable(self, key, value):
        return f".property('{key}', '{json.dumps(value)}')"

    def property_query(self, key: str, value: str | list[str]) -> str:
        """
        Generates a Gremlin query string for setting a property using
            `.property('key', 'value')`.

        Args:
            key (str): Name of the property.
            value (str | list[str]): Value of the property (string or list of strings).

        Returns:
            str: Gremlin query string with `.property('key', 'value')` property setting
                 step.
        """
        if value is None:
            return self._parse_property_as_empty(
                key, value
            )  #  f".property('{key}', '')"
        if str(key) == "id":
            return self._parse_property_as_is(key, value)  #  f".property(id, '{value}')"
        elif str(key) == "label":
            return self._parse_property_as_is(
                key, value
            )  #  f".property(label, '{value}')"
        elif str(key) == "description":
            return self._parse_property_as_multiline_string(
                key, value
            )  #  f".property('{key}', '''{value}''')"
        elif str(key) == "alternatives":
            return self._parse_property_as_iterable(
                key, value
            )  #  f".property('{key}', '{json.dumps(value, ensure_ascii=False)}')"
        elif str(key) == "tag":
            return self._parse_property_as_iterable(
                key, value
            )  #  f".property('{key}', '{json.dumps(value, ensure_ascii=False)}')"
        elif str(key) == "probabilities":
            return self._parse_property_as_iterable(
                key, value
            )  #  f".property('{key}', '{json.dumps(value, ensure_ascii=False)}')"
        elif str(key) == "comments":
            return self._parse_property_as_iterable(
                key, value
            )  #  f".property('{key}', '{json.dumps(value, ensure_ascii=False)}')"
        elif isinstance(value, list):
            return f".property('{key}', '{json.dumps(value, ensure_ascii=False)}')"
        else:
            return self._parse_property_as_simple_string(
                key, value
            )  #  f".property('{key}', '{value}')"

    def property_dict_query(self, property_dict: dict[str, str]) -> str:
        """
        Generates a Gremlin query string for setting multiple properties by
            concatenating properties as
        `.property('key1', 'value1').property('key2', 'value2')`.

        Args:
            property_dict (dict[str, str]): Dictionary of property key-value pairs.

        Returns:
            str: Gremlin query string with multiple property setting steps.
        """

        return "".join([self.property_query(k, v) for k, v in property_dict.items()])
