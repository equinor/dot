import React, { useState, useEffect } from "react";
import { Button } from "@equinor/eds-core-react";
import AppHeader from "../components/NavBar";
import FramingTabs from "../components/framingTabs";
import { readIssues } from "../services/issue_api";
import DecisionPyramid from "../components/decisionPyramid";
import { useProjectContext } from "../components/context";
import DecisionGrid from "../components/data_grid/decision_grid/DecisionGrid";
import { useIssueList } from "../components/allIssueContext";
import { useFilterList } from "../components/data_grid/gridFilterContext";

function DecisionHierarchy() {
  const [project] = useProjectContext();
  const { issueList, setIssueList } = useIssueList();
  const { filterList, setFilterList } = useFilterList();

  const [showPyramid, setShowPyramid] = useState(false);
  const showHideFunc = () => {
    console.log(showPyramid);
    showPyramid ? setShowPyramid(false) : setShowPyramid(true);
  };

  const fetchData = async () => {
    const inData = await readIssues(project, {
      category: "Decision",
      boundary: "in",
    });
    const onData = await readIssues(project, {
      category: "Decision",
      boundary: "on",
    });
    const updatedData = inData.concat(onData);
    setIssueList(updatedData);

    const tags = [...new Set(updatedData.flatMap((issue) => issue.tag))].sort();

    const alternatives = [
      ...new Set(updatedData.flatMap((issue) => issue.alternatives)),
    ].sort();

    setFilterList([alternatives, tags]);
  };
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      <AppHeader />
      <FramingTabs />
      <div className="pyramidButton">
        <Button onClick={showHideFunc}>
          {showPyramid ? "Show List" : "Show Pyramid"}
        </Button>
      </div>
      {showPyramid ? <DecisionPyramid /> : <DecisionGrid />}
    </>
  );
}

export default DecisionHierarchy;
