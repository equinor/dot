import React, { useEffect } from "react";
import AppHeader from "../components/NavBar";
import FramingTabs from "../components/framingTabs";
import { readIssues } from "../services/issue_api";
import AddIssue from "../components/addIssue";
import "../styles/issueListStyle.css";
import { useProjectContext } from "../components/context";
import UncertaintyGrid from "../components/data_grid/uncertainty_grid/UncertaintyGrid";
import { useIssueList } from "../components/allIssueContext";
import { useFilterList } from "../components/data_grid/gridFilterContext";

function Uncertainties() {
  const [project] = useProjectContext();
  const { issueList, setIssueList } = useIssueList();
  const { filterList, setFilterList } = useFilterList();

  const fetchData = async () => {
    const inData = await readIssues(project, {
      category: "Uncertainty",
      boundary: "in",
    });
    const onData = await readIssues(project, {
      category: "Uncertainty",
      boundary: "on",
    });
    const updatedData = inData.concat(onData);
    setIssueList(updatedData);

    const outcomes = [
      ...new Set(
        updatedData.flatMap((issue) => {
          if (!issue.probabilities) {
            return null;
          } else {
            const firstVariableKey = Object.keys(
              issue.probabilities.variables
            )[0];
            return issue.probabilities.variables[firstVariableKey];
          }
        })
      ),
    ].sort();

    const tags = [...new Set(updatedData.flatMap((issue) => issue.tag))].sort();

    setFilterList([outcomes, tags]);
  };
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      <AppHeader />
      <FramingTabs />
      <AddIssue onSave={fetchData} />
      <UncertaintyGrid />
    </>
  );
}

export default Uncertainties;
