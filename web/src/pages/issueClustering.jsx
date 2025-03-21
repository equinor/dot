import React, { useState, useEffect } from "react";
import { readIssues } from "../services/issue_api";
import FramingTabs from "../components/framingTabs";
import AppHeader from "../components/NavBar";
import IssueClusterElement from "../components/issueClusterElement";
import AddIssue from "../components/addIssue";
import { useProjectContext } from "../components/context";

function IssueClustering() {
  const [project] = useProjectContext();
  const [, setFactList] = useState([]);
  const [, setUncertaintyList] = useState([]);
  const [, setDecisionList] = useState([]);
  const [, setUnassignedList] = useState([]);
  const [dataSet, setDataSet] = useState({});

  const createDataSet = (list) => {
    const columns = {
      Unassigned: {
        id: "Unassigned",
        title: "Unassigned",
        itemsOrder: [],
        items: {},
      },
      Fact: {
        id: "Fact",
        title: "Fact",
        itemsOrder: [],
        items: {},
      },
      Uncertainty: {
        id: "Uncertainty",
        title: "Uncertainty",
        itemsOrder: [],
        items: {},
      },
      Decision: {
        id: "Decision",
        title: "Decision",
        itemsOrder: [],
        items: {},
      },
    };

    // Iterate over the list and group items by column
    list.forEach((item) => {
      let columnId = "";
      if (item.category === "") {
        columnId = "Unassigned";
      } else {
        columnId = item.category;
      }

      if (!columns[columnId]) {
        // Create a new column if it doesn't exist
        columns[columnId] = {
          id: columnId,
          title: columnId,
          itemsOrder: [],
        };
      }
      // Add the item to the column's itemsOrder array
      columns[columnId].itemsOrder.push(item);
    });
    // Return the columns object
    return columns;
  };

  const fetchData = async () => {
    const updatedUncertaintyData = await readIssues(project, {
      category: "Uncertainty",
    });
    setUncertaintyList(
      updatedUncertaintyData.sort((a, b) => a.index - b.index)
    );
    const updatedFactData = await readIssues(project, { category: "Fact" });
    setFactList(updatedFactData.sort((a, b) => a.index - b.index));
    const updatedDecisionData = await readIssues(project, {
      category: "Decision",
    });
    setDecisionList(updatedDecisionData.sort((a, b) => a.index - b.index));
    const updatedUnassignedList = await readIssues(project, {
      category: "",
    });
    setUnassignedList(updatedUnassignedList);

    // Call createDataSet to create the new data set
    //TODO: Have this as an API call?
    const newDataSet = createDataSet([
      ...updatedUnassignedList,
      ...updatedFactData,
      ...updatedUncertaintyData,
      ...updatedDecisionData,
    ]);
    setDataSet(newDataSet);
  };
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <>
      <AppHeader />
      <FramingTabs />
      <AddIssue onSave={fetchData} />
      <div>
        <IssueClusterElement
          dataSet={dataSet}
          setDataSet={setDataSet}
          onEditIssue={fetchData}
        />
      </div>
    </>
  );
}

export default IssueClustering;
