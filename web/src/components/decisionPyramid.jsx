import React from "react";
import { useIssueList } from "./allIssueContext";

function DecisionPyramid() {
  const { issueList } = useIssueList();
  console.log("Decision List", issueList);
  //upper one
  const policyList = issueList.filter((item) => item.decisionType === "Policy");

  // lower one
  const tacticalList = issueList.filter(
    (item) => item.decisionType === "Tactical"
  );

  //in the middle
  const focusList = issueList.filter((item) => item.decisionType === "Focus");

  const focusLayerStyle = {
    width: "800px",
  };
  const tacticLayerStyle = {
    width: "800px",
  };
  const policyLayerStyle = {
    height: "{policyLayerHeight}px",
    width: "800px",
  };

  return (
    <div className="pyramid">
      <div className="policyLayer" style={policyLayerStyle}>
        <h4 style={{ textAlign: "center" }}>Policy</h4>
        {policyList.map((item) => (
          <p key={item.uuid} style={{ marginTop: "10px" }}>
            {item.name}
          </p>
        ))}
      </div>
      <div className="focusLayer" style={focusLayerStyle}>
        <h4 style={{ textAlign: "center" }}>Focus</h4>
        {focusList.map((item) => (
          <p key={item.uuid} style={{ marginTop: "10px" }}>
            {item.name}
          </p>
        ))}
      </div>
      <div className="tacticalLayer" style={tacticLayerStyle}>
        <h4 style={{ textAlign: "center" }}>Tactical</h4>
        {tacticalList.map((item) => (
          <p key={item.uuid} style={{ marginTop: "10px" }}>
            {item.name}
          </p>
        ))}
      </div>
    </div>
  );
}

export default DecisionPyramid;
