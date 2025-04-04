"""Module defining the ProbabilisticGraphModel Abstract class"""

from __future__ import annotations

import importlib
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING

import networkx as nx

if TYPE_CHECKING:  # pragma: no cover
    from ..decision_diagrams.edge import Edge
    from ..decision_diagrams.node import NodeABC


logger = logging.getLogger(__name__)


class ProbabilisticGraphModelABC(ABC):
    NODES_MODULE_PATH = "src.v0.services.structure_utils.decision_diagrams.node"

    """Probabilistic Graph Model"""

    def __init__(self, *args, **kwargs):
        """
        Create an instance of a ProbabilisticGraphModel (ABSTRACT class!!!)
        It is a wrapper around networkx.Digraph

        Args:
            *args, **kwargs: arguments for networkx.DiGraph

        Attributes:
            nx: networkx object
        """
        self.nx = nx.DiGraph(*args, **kwargs)

    @classmethod
    def from_dict(cls, data: dict):
        """Create a probabilistic graph model from data in a dictionary

        Args:
            data (Dict): dictionary describing the graph model
                {"nodes": List[NodeABC], "edges": List[Edge]}

        Returns:
            ProbabilisticGraphModelABC: the decision diagram
        """
        diagram = cls.initialize_diagram(data)
        for node in data["nodes"]:
            diagram.add_node(node)
        for edge in data.get("edges", []):
            diagram.add_edge(edge)
        return diagram

    @classmethod
    @abstractmethod
    def initialize_diagram(cls, data):
        """Initialize a diagram with data"""
        raise NotImplementedError

    def add_node(self, node: NodeABC):
        """Add a node to the graph

        Args:
            node (NodeABC): node to be added
        """
        self.nx.add_node(node)

    def add_edge(self, edge: Edge):
        """Add an edge to the graph

        Args:
            edge (Edge): Edge to be added. If some of the end points do not exist, they
                         are added to the graph too.
        """
        nx_edge, nx_attributes = edge.to_nx()
        self.nx.add_edge(nx_edge[0], nx_edge[1], **nx_attributes)

    def copy(self):
        """copy the probabilistic graph model

        Returns
            ProbabilisticGraphModel: a copy of the graph. uuid's of the nodes are copied
                                     too.
        """
        new_id = type(self)()  # Need to instance from the concrete class
        new_id.nx = self.nx.copy()
        return new_id

    def get_parents(self, node: NodeABC) -> list[NodeABC]:
        """get parents of a given node

        Args:
            node (NodeABC): node to find the parents of

        Returns
            List[NodeABC]: the list of the parents of the given node
        """
        return list(self.nx.predecessors(node))

    def get_children(self, node: NodeABC) -> list[NodeABC]:
        """get children of a given node

        Args:
            node (NodeABC): node to find the children of

        Returns
            List[NodeABC]: the list of the children of the given node
        """
        return list(self.nx.successors(node))

    def get_node_type(self, node: NodeABC) -> str:
        """Return the type of a given node

        Args:
            node (NodeABC): node to examine

        Returns
            str: a string describing the type of the node (class name in lower font and
                 without the "Node" suffix)
        """
        return type(node).__name__.replace("Node", "").lower()

    def _get_nodes_from_type(self, node_type_string: str) -> list[NodeABC]:
        """find all the nodes of a given type

        Args:
            node_type_str (str): type of the nodes to find as a string

        Returns
            List[NodeABC]: the list of the nodes of given type
        """
        node_type = getattr(
            importlib.import_module(self.NODES_MODULE_PATH),
            node_type_string
        )
        node_list = []
        for node in list(self.nx.nodes(data=True)):
            if isinstance(node[0], node_type):
                node_list.append(node[0])
        return node_list

    def has_children(self, node: NodeABC) -> bool:
        """Check for existence of children

        Args:
            node (NodeABC): node to check for children

        Returns
            bool: existence (True) or not (False) of children to the given node
        """
        return len(self.get_children(node)) > 0

    def to_json(self, filepath: Path = None) -> str:
        """Convert the graph into a json object

        Args:
            filepath (Path, optional): Path where to copy the json file. None if no
                                       output file.

        Returns:
            str: json object as a string
        """
        json_object = self._to_json_stream()
        if filepath:
            with open(filepath, "w") as outfile:
                outfile.write(json_object)
        return json_object

    @abstractmethod
    def _to_json_stream(self):
        raise NotImplementedError

    def get_node_from_uuid(self, uuid: str) -> NodeABC:
        """get a node given its uuid

        Args:
            uuid (str): uuid of node to look for

        Returns:
            NodeABC: node object having the given uuid
        """
        return [node for node in self.nx if node.uuid == uuid][0]
