import { useState, useEffect } from "react";
import AppHeader from "../components/NavBar";
import FramingTabs from "../components/framingTabs";
import AddObjective from "../components/addObjective";
import ObjectivesTable from "../components/objectiveTable";
import { allObjectives } from "../services/objective_api";
import { useProjectContext } from "../components/context";

function Objectives() {
  const [project] = useProjectContext();
  const [objectiveList, setObjectiveList] = useState([]);
  console.log("Project", project);

  const fetchData = async () => {
    const updatedData = await allObjectives(project);
    setObjectiveList(updatedData);
    //setProj(project);
  };
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      <AppHeader />
      <FramingTabs />
      <AddObjective onSave={fetchData} />
      <ObjectivesTable objectives={objectiveList} onEditIssue={fetchData} />
    </>
  );
}

export default Objectives;
