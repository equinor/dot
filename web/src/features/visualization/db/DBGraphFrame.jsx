import React, { useEffect, createRef } from "react";
import { Network } from "vis-network/standalone";
import DBGraph from "./DBGraph";
import { useProjectContext } from "../../../components/context";

import { readGraphData } from "../../../services/issue_api";

const [project] = useProjectContext();
var idData = [];
console.log(idData);

idData = await readGraphData(project);
console.log(idData);

const graph = new DBGraph();
const data = graph.toVisData(idData);
console.log(data);
const options = graph.toVisOptions();

const Graph = () => {
  const container = createRef();

  useEffect(() => {
    const network =
      container.current && new Network(container.current, data, options);
  }, [container, data, options]);

  return <div ref={container} style={{ height: "1000px" }} />;
};

export default Graph;
