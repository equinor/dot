import React, { useState, useEffect, useRef } from "react";
import * as d3 from "d3";
import AppHeader from "../components/NavBar";
import { Button } from "@equinor/eds-core-react";
import { id2dt } from "../services/structures_api";
import StructuringTab from "../components/structuringTab";
import { useProjectContext } from "../components/context";

function DecisionTree() {
  const svgRef = useRef(null);
  const [state, setState] = useState({});
  const [project] = useProjectContext();
  const [treeData, setTreeData] = useState(null);
  const fetchData = async () => {
    const updatedData = await id2dt(project);
    setTreeData(updatedData);
    console.log(updatedData);
  };

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (treeData) {
      const margin = { top: 200, right: 70, bottom: 100, left: 70 };
      const width = window.innerWidth - margin.left - margin.right;
      const height = window.innerHeight - margin.top - margin.bottom;
      const dx = 50;
      const dy = width / 7;
      const tree = d3.tree().nodeSize([dx, dy]);
      const diagonal = d3
        .linkHorizontal()
        .x((d) => d.y)
        .y((d) => d.x);
      const root = d3.hierarchy(treeData);
      root.x0 = dy / 2;
      root.y0 = 0;
      root.descendants().forEach((d, i) => {
        d.id = i;
        d._children = d.children;
        if (d.depth && d.data.id.shortname.length !== 7) {
          d.children = null;
        }
      });

      /* eslint-disable */
      function zoomed(event) {
        const { transform } = event;
        const { k } = transform;
        const maxZoom = 10;
        const minZoom = 0.5;
        const limitedScale = Math.max(minZoom, Math.min(maxZoom, k));
        const limitedTransform = transform.scale(limitedScale);
        gNode.attr("transform", limitedTransform);
        gLink.attr("transform", limitedTransform);
      }
      /* eslint-enable  */

      const svg = d3
        .select(svgRef.current)
        .attr("viewBox", [
          -margin.left,
          -margin.top,
          width + margin.left + margin.right,
          height + margin.top + margin.bottom,
        ])
        .style("font", "14px sans-serif")
        .style("user-select", "none")
        .call(d3.zoom().on("zoom", zoomed).scaleExtent([0.5, 10]));

      const gLink = svg //LINKS
        .append("g")
        .attr("fill", "none")
        .attr("stroke", "black")
        .attr("stroke-opacity", 0.99)
        .attr("stroke-width", 1.5);

      const gNode = svg
        .append("g")
        .attr("cursor", "pointer")
        .attr("pointer-events", "all");

      const update = (source) => {
        const duration = 5;
        const nodes = root.descendants().reverse();
        const links = root.links();

        // Compute the new tree layout.
        tree(root);

        let left = root;
        let right = root;
        root.eachBefore((node) => {
          if (node.x < left.x) left = node;
          if (node.x > right.x) right = node;
        });

        let top = root;
        let bottom = root;
        root.eachBefore((node) => {
          if (node.y > top.y) top = node;
          if (node.y < bottom.y) bottom = node;
        });
        console.log("top", top, "bottom", bottom);

        //transition for links
        const linkTransition = d3
          .transition()
          .duration(duration)
          .ease(d3.easeCubicInOut);

        //transition for Nodes
        const nodeTransition = svg
          .transition()
          .duration(duration)
          .attr("viewBox", [-margin.left, left.x - margin.top, width, height])
          .tween(
            "resize",
            window.ResizeObserver ? null : () => () => svg.dispatch("toggle")
          );

        // Update the nodes…
        const node = gNode.selectAll("g").data(nodes, (d) => d.id);

        // Enter any new nodes at the parent's previous position.
        const nodeEnter = node
          .enter()
          .append("g")
          .attr("transform", (d) => `translate(${source.y0},${source.x0})`)
          .attr("fill-opacity", 0)
          .attr("stroke-opacity", 0)
          .on("click", (event, d) => {
            console.log("Node clicked");
            d.children = d.children ? null : d._children;
            update(d);
          });

        nodeEnter
          .filter(function (d) {
            console.log(d.data.id);
            return d.data.id.node_type.match(/Uncertainty/);
          })
          .append("circle")
          .attr("class", "Node")
          .attr("r", 5)
          .attr("fill", "green")
          .attr("stroke-width", 10);
        nodeEnter
          .filter(function (d) {
            return d.data.id.node_type.match(/Decision/);
          })
          .append("rect")
          .attr("width", 20)
          .attr("height", 20)
          .attr("fill", "yellow")
          .attr("stroke-width", 10);

        nodeEnter
          .filter(function (d) {
            return d.data.id.node_type.match(/Utility/);
          })
          .append("rect")
          .attr("width", 20)
          .attr("height", 20)
          .attr("fill", "lightblue")
          .attr("stroke-width", 10);

        //special node format (uncertainty, decision)

        nodeEnter
          .append("text")
          .attr("dy", "1.5em") //location of text 0.9em -> below the line
          .attr("text-anchor", "middle")
          .attr("font-size", 14)
          .text((d) => d.data.id.shortname)
          .clone(true)
          .lower()
          .attr("stroke-linejoin", "round")
          .attr("stroke-width", 2) //line around text?
          .attr("stroke", "white"); //colour around text

        // Transition nodes to their new position.
        const nodeUpdate = node
          .merge(nodeEnter)
          .transition(nodeTransition)
          .attr("transform", (d) => `translate(${d.y},${d.x})`)
          .attr("fill-opacity", 1)
          .attr("stroke-opacity", 1);

        nodeUpdate.select("circle").attr("r", 10).attr("cx", 0).attr("cy", 0);

        nodeUpdate
          .select("rect")
          .attr("x", -10)
          .attr("y", -10)
          .attr("width", 20)
          .attr("height", 20);

        // Transition exiting nodes to the parent's new position.
        const nodeExit = node
          .exit()
          .transition(nodeTransition)
          .attr("transform", (d) => `translate(${source.y},${source.x})`)
          .attr("fill-opacity", 0)
          .attr("stroke-opacity", 0)
          .remove();

        // Update the links…
        const link = gLink.selectAll("path").data(links, (d) => d.target.id);

        // Enter any new links at the parent's previous position.
        const linkEnter = link
          .enter()
          .append("path")
          .attr("d", (d) => {
            const sourceX = d.source.y;
            const sourceY = d.source.x;
            const targetX = d.target.y;
            const targetY = d.target.x;
            const midpointX = (sourceX + targetX) / 2;
            const midpointY = targetY;
            return `M${sourceX},${sourceY} L${midpointX},${midpointY} L${targetX},${targetY}`;
          });

        // Transition links to their new position.
        link
          .merge(linkEnter)
          .transition(linkTransition)
          .attr("d", (d) => {
            const sourceX = d.source.y;
            const sourceY = d.source.x;
            const targetX = d.target.y;
            const targetY = d.target.x;
            const midpointX = (sourceX + targetX) / 2;
            const midpointY = targetY;
            return `M${sourceX},${sourceY} L${midpointX},${midpointY} L${targetX},${targetY}`;
          })
          .attr("x1", function (d) {
            return d.target.y;
          })
          .attr("y1", function (d) {
            return d.target.x;
          })
          .attr("x2", function (d) {
            return d.source.y;
          })
          .attr("y2", function (d) {
            return d.source.x;
          });

        // Transition exiting links to the parent's new position.
        link.exit().remove();

        // Transition exiting nodes to the parent's new position.
        link
          .exit()
          .attr("d", (d) => {
            const sourceX = d.source.y;
            const sourceY = d.source.x;
            const targetX = d.source.y;
            const targetY = d.source.x;
            return `M${sourceX},${sourceY} L${targetX},${targetY}`;
          })
          .remove();

        const linkText = gLink.selectAll("g").data(links, (d) => d.target.id);

        const linkTextEnter = linkText
          .enter()
          .append("g")
          .attr("fill", "black")
          .attr("stroke", "white")
          .attr("stroke-width", 0)
          .attr("font-size", 14)
          .attr(
            "transform",
            (d) =>
              `translate(${(d.source.y + d.target.y) / 2},${d.target.x - 5})`
          );

        linkTextEnter.append("text").text((d) => d.target.data.id.branch_name);

        linkText
          .merge(linkTextEnter)
          .transition(linkTransition)
          .attr(
            "transform",
            (d) =>
              `translate(${(d.source.y + d.target.y) / 2},${d.target.x - 5})`
          )
          // Smooth transition from 0 to 1 and back to 0 when expanding/collapsing
          .attr("fill-opacity", 1)
          .attr("stroke-opacity", 1);

        linkText.exit().remove();

        // Stash the old positions for transition.
        root.eachBefore((d) => {
          d.x0 = d.x;
          d.y0 = d.y;
        });
      };

      update(root);

      // expand the next level nodes
      const expandAll = () => {
        root.descendants().forEach((d) => {
          if (d._children) {
            d.children = d._children;
            d._children = null;
          }
        });
        update(root);
      };

      // collapse all nodes
      const collapseAll = () => {
        root.descendants().forEach((d) => {
          if (d.children) {
            d._children = d.children;
            d.children = null;
          }
        });
        root.x0 = dy / 2;
        root.y0 = 0;
        update(root);
      };
      setState({ expandAll, collapseAll });
      // Clean up the effect
      return () => {
        setState(null);
      };
    }
  }, [treeData]);

  const handleExpandAll = () => {
    state.expandAll();
  };
  const handleCollapseAll = () => {
    state.collapseAll();
  };

  return (
    <>
      <AppHeader />
      <StructuringTab />
      <div>
        <Button onClick={handleExpandAll}>Expand All</Button>
        <Button onClick={handleCollapseAll}>Collapse All</Button>
        <svg ref={svgRef} style={{ font: "10px sans-serif" }}></svg>
      </div>
    </>
  );
}

export default DecisionTree;
