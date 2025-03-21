from src.v0.database.builders.queries.gremlin_queries_vertex import (
    GremlinStringQueryBuilderVertex,
)


def test_create_vertex():
    assert GremlinStringQueryBuilderVertex().create_vertex(
        "junk", {"uuid": "id", "a": 1}
    ) == (
        "g.addV('junk')"
        ".property(id, 'id')"
        ".property('uuid', 'id')"
        ".property('a', '1')"
        ".valueMap(true)"
    )


def test_read_vertex():
    assert (
        GremlinStringQueryBuilderVertex().read_vertex("uuid")
        == "g.V('uuid').valueMap(true)"
    )


def test_read_out_vertex():
    assert (
        GremlinStringQueryBuilderVertex().read_out_vertex("uuid", "junk")
        == "g.V('uuid').out('junk').valueMap(true)"
    )
    assert (
        GremlinStringQueryBuilderVertex().read_out_vertex(
            "uuid", "junk", original_vertex_label="junky"
        )
        == "g.V('uuid').out('junk').hasLabel('junky').valueMap(true)"
    )
    assert (
        GremlinStringQueryBuilderVertex().read_out_vertex(
            "uuid", "junk", filter_dict={"a": 1}
        )
        == "g.V('uuid').out('junk').has('a', '1').valueMap(true)"
    )
    assert (
        GremlinStringQueryBuilderVertex().read_out_vertex(
            "uuid", "junk", original_vertex_label="junky", filter_dict={"a": 1}
        )
        == "g.V('uuid').out('junk').hasLabel('junky').has('a', '1').valueMap(true)"
    )


def test_read_in_vertex():
    assert (
        GremlinStringQueryBuilderVertex().read_in_vertex("uuid", "junk")
        == "g.V('uuid').in('junk').valueMap(true)"
    )
    assert (
        GremlinStringQueryBuilderVertex().read_in_vertex(
            "uuid", "junk", original_vertex_label="junky"
        )
        == "g.V('uuid').in('junk').hasLabel('junky').valueMap(true)"
    )
    assert (
        GremlinStringQueryBuilderVertex().read_in_vertex(
            "uuid", "junk", filter_dict={"a": 1}
        )
        == "g.V('uuid').in('junk').has('a', '1').valueMap(true)"
    )
    assert (
        GremlinStringQueryBuilderVertex().read_in_vertex(
            "uuid", "junk", original_vertex_label="junky", filter_dict={"a": 1}
        )
        == "g.V('uuid').in('junk').hasLabel('junky').has('a', '1').valueMap(true)"
    )


def test_list_all_vertices():
    assert (
        GremlinStringQueryBuilderVertex().list_all_vertices("junk")
        == "g.V().hasLabel('junk').valueMap(true)"
    )


def test_update_vertex():
    assert (
        GremlinStringQueryBuilderVertex().update_vertex("uuid", {"a": 1})
        == "g.V('uuid').property('a', '1').valueMap(true)"
    )


def test_delete_vertex():
    assert (
        GremlinStringQueryBuilderVertex().delete_vertex("uuid") == "g.V('uuid').drop()"
    )
