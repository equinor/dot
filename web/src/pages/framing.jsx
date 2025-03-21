import React, { useState, useEffect } from "react";
import AppHeader from "../components/NavBar";
import FramingTabs from "../components/framingTabs";
import { readIssues } from "../services/issue_api";
import AddIssue from "../components/addIssue";
import "../styles/issueListStyle.css";
import { useProjectContext } from "../components/context";
import { useIssueList } from "../components/allIssueContext";
import IssueGrid from "../components/data_grid/issue_data_grid/IssueGrid";
import { useFilterList } from "../components/data_grid/gridFilterContext";
import { Switch } from "@equinor/eds-core-react";

function Framing() {
  const [project] = useProjectContext();
  const [, setProj] = useState(null);
  const { issueList, setIssueList } = useIssueList();
  const { filterList, setFilterList } = useFilterList();
  const [check, setCheck] = useState(false);

  const fetchData = async () => {
    const updatedData = await readIssues(project);
    setIssueList(updatedData);
    setProj(project);
    const tags = [...new Set(updatedData.flatMap((issue) => issue.tag))].sort();
    setFilterList([tags]);
  };
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      <AppHeader />
      <FramingTabs />
      <AddIssue onSave={fetchData} />
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          marginRight: "50px",
        }}
      >
        <div></div>
        <Switch
          onChange={(e) => {
            setCheck(e.target.checked);
          }}
          checked={check}
          disabled
          label={`${check ? "Activated" : "No"} AI Support`}
        />
      </div>

      <IssueGrid />
    </>
  );
}

export default Framing;
