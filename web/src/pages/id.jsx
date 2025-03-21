import React from "react";
import AppHeader from "../components/NavBar";
import CIDGraphFrame from "../features/visualization/cid/CIDGraphFrame";
import "../styles/id.css";
import StructuringTab from "../components/structuringTab";

function InfluenceDiagram() {
  return (
    <>
      <AppHeader />
      <StructuringTab />
      <div>
        {" "}
        <CIDGraphFrame />{" "}
      </div>
    </>
  );
}

export default InfluenceDiagram;
