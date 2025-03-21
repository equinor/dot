from src.v0.database.builders.queries.query_builder import GremlinStringQueryBuilder


def test_GremlinStringQueryBuilder():
    gqb = GremlinStringQueryBuilder()
    assert gqb.transform_query == ".valueMap(true)"
    assert gqb.graph_name == "g"


def test_filter_query():
    gqb = GremlinStringQueryBuilder()
    assert gqb.filter_query({}) == ""
    assert gqb.filter_query({"a": None}) == ""
    assert (
        gqb.filter_query({"a": "1", "b": "2", "c": None, "d": "4"})
        == ".has('a', '1').has('b', '2').has('d', '4')"
    )


def test_filter_label_query():
    gqb = GremlinStringQueryBuilder()
    assert gqb.filter_label_query("junk") == ".hasLabel('junk')"


def test__parse_property_as_is():
    gqb = GremlinStringQueryBuilder()
    assert gqb._parse_property_as_is("a", 1) == ".property(a, '1')"


def test__parse_property_as_empty():
    gqb = GremlinStringQueryBuilder()
    assert gqb._parse_property_as_empty("a", 1) == ".property('a', '')"


def test__parse_property_as_simple_string():
    gqb = GremlinStringQueryBuilder()
    assert gqb._parse_property_as_simple_string("a", 1) == ".property('a', '1')"


def test__parse_property_as_multiline_string():
    gqb = GremlinStringQueryBuilder()
    assert gqb._parse_property_as_multiline_string("a", 1) == ".property('a', '''1''')"


def test__parse_property_as_iterable():
    gqb = GremlinStringQueryBuilder()
    assert gqb._parse_property_as_iterable("a", [1, 2]) == ".property('a', '[1, 2]')"
    assert (
        gqb._parse_property_as_iterable("a", ["1", "2"])
        == ".property('a', '[\"1\", \"2\"]')"
    )


def test_property_query():
    gqb = GremlinStringQueryBuilder()
    assert gqb.property_query("a", None) == ".property('a', '')"
    assert gqb.property_query("id", "1") == ".property(id, '1')"
    assert gqb.property_query("label", "1") == ".property(label, '1')"
    assert gqb.property_query("description", "1") == ".property('description', '''1''')"
    assert (
        gqb.property_query("alternatives", ["1", "2"])
        == ".property('alternatives', '[\"1\", \"2\"]')"
    )
    assert gqb.property_query("tag", ["1", "2"]) == ".property('tag', '[\"1\", \"2\"]')"
    assert (
        gqb.property_query("probabilities", {"x": ["1", "2"]})
        == '.property(\'probabilities\', \'{"x": ["1", "2"]}\')'
    )
    assert (
        gqb.property_query("comments", [{"comment": "test", "author": "user"}])
        == '.property(\'comments\', \'[{"comment": "test", "author": "user"}]\')'
    )
    assert (
        gqb.property_query("a_list", ["1", "2"])
        == ".property('a_list', '[\"1\", \"2\"]')"
    )
    assert gqb.property_query("a", "1") == ".property('a', '1')"


def test_property_dict_query():
    gqb = GremlinStringQueryBuilder()
    assert (
        gqb.property_dict_query({"a": "1", "b": "2", "c": None, "d": "4"})
        == ".property('a', '1').property('b', '2').property('c', '').property('d', '4')"
    )
