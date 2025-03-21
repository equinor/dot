from src.v0.database.builders.queries.gremlin_queries_edge import (
    GremlinStringQueryBuilderEdge,
)


def test_create_edge():
    assert GremlinStringQueryBuilderEdge().create_edge(
        "junk", "id_out", "id_in", {"uuid": "id"}
    ) == (
        "g.V('id_out')"
        ".addE('junk')"
        ".to(__.V('id_in'))"
        ".property(id, 'id')"
        ".property('uuid', 'id')"
    )


def test_read_edge():
    assert GremlinStringQueryBuilderEdge().read_edge("junk") == "g.E('junk')"


def test_list_all_edges():
    assert (
        GremlinStringQueryBuilderEdge().list_all_edges("junk")
        == "g.E().hasLabel('junk').valueMap(true)"
    )
    assert (
        GremlinStringQueryBuilderEdge().list_all_edges("junk", {"a": "1"})
        == "g.E().hasLabel('junk').has('a', '1').valueMap(true)"
    )


def test_list_all_edges_from_project():
    assert (
        GremlinStringQueryBuilderEdge().list_all_edges_from_project("uuid", "junk")
        == "g.V('uuid').outE('contains')"
    )
    assert (
        GremlinStringQueryBuilderEdge().list_all_edges_from_project("uuid", "influences")
        == "g.V('uuid').outE('contains').inV().outE('influences')"
    )
    assert (
        GremlinStringQueryBuilderEdge().list_all_edges_from_project(
            "uuid", "merged_into"
        )
        == "g.V('uuid').outE('contains').inV().inE('merged_into')"
    )
    assert (
        GremlinStringQueryBuilderEdge().list_all_edges_from_project(
            "uuid", "has_value_metric"
        )
        == "g.V('uuid').outE('contains').inV().outE('has_value_metric')"
    )


def test_read_out_edge_from_vertex():
    assert (
        GremlinStringQueryBuilderEdge().read_out_edge_from_vertex("uuid", "junk")
        == "g.V('uuid').outE().hasLabel('junk')"
    )


def test_read_in_edge_to_vertex():
    assert (
        GremlinStringQueryBuilderEdge().read_in_edge_to_vertex("uuid", "junk")
        == "g.V('uuid').inE().hasLabel('junk')"
    )


def test_update_edge():
    assert (
        GremlinStringQueryBuilderEdge().update_edge("uuid", {"a": 1})
        == "[g.E('uuid').property('a', '1')]"
    )


def test_delete_edge():
    assert GremlinStringQueryBuilderEdge().delete_edge("uuid") == "g.E('uuid').drop()"


def test_delete_edge_from_vertex():
    assert (
        GremlinStringQueryBuilderEdge().delete_edge_from_vertex("uuid")
        == "g.V('uuid').bothE().drop()"
    )
