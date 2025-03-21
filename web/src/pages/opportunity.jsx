// react
import React, { useState, useEffect } from "react";

// dot
import AppHeader from "../components/NavBar";
import FramingTabs from "../components/framingTabs";
import AddOpportunity from "../components/addOpportunity";
import DisplayOpportunities from "../components/oppoTable";
import { allOpportunities } from "../services/opportunity_api";
import "../styles/opportunityStyle.css";
import { useProjectContext } from "../components/context";

function Opportunity() {
  const [project] = useProjectContext();

  const [opportunities, setOppList] = useState([]);

  const fetchData = async () => {
    const updateData = await allOpportunities(project);
    setOppList(updateData);
  };
  useEffect(() => {
    fetchData();
  }, []);
  console.log("Chosen project", project);

  return (
    <>
      <AppHeader />
      <FramingTabs />
      <AddOpportunity onSave={fetchData} />
      <DisplayOpportunities opp={opportunities} onEditIssue={fetchData} />
    </>
  );
}

export default Opportunity;
