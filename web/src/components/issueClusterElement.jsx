import React, { useMemo } from "react";
import { DragDropContext } from "react-beautiful-dnd";
import { readIssue, updateIssue, mergeIssue } from "../services/issue_api";
import "../styles/issueListStyle.css";
import "../styles/clusterTable.css";
import ClusterColumn from "./ClusterColumn";
import { useProjectContext } from "./context";

async function merge_issues(project, src, dst) {
  await mergeIssue(project, src, dst);
  return;
}

function IssueClusterElement({ dataSet, setDataSet, onEditIssue }) {
  const [project] = useProjectContext();

  const readIssueMemo = useMemo(() => readIssue, []);
  const updateIssueMemo = useMemo(() => updateIssue, []);

  const getItemListForColumn = (columnId) => {
    const column = dataSet[columnId];
    if (column) return column.itemsOrder;
    else {
      return [];
    }
  };
  const handleMergeIssues = async (draggableId, combine) => {
    const dstIssue = await readIssueMemo(draggableId);
    const srcIssue = await readIssueMemo(combine.draggableId);
    await merge_issues(project, dstIssue, srcIssue);
  };
  const handleDragEnd = async (result) => {
    const { destination, source, draggableId, combine } = result;
    if (!destination && !combine) {
      // rare case of dropping in between columns which is neither combining, nor moving
      console.log("Hit the jackpot!!!");
      return;
    }
    if (combine) {
      await handleMergeIssues(draggableId, combine);
      onEditIssue();
      return;
    }
    if (
      source.droppableId === destination.droppableId &&
      source.index === destination.index
    )
      return;
    //if element is dropped in the same column but different position
    if (
      source.droppableId === destination.droppableId &&
      source.index !== destination.index
    ) {
      const sourceColumnId = source.droppableId;
      const newItemOrder = [...dataSet[sourceColumnId].itemsOrder];
      const [movedItem] = newItemOrder.splice(source.index, 1);
      newItemOrder.splice(destination.index, 0, movedItem);
      const newData = { ...dataSet };
      newData[sourceColumnId].itemsOrder = newItemOrder;
      setDataSet(newData);
      try {
        await Promise.all(
          newItemOrder.map(async (item, index) => {
            const issue = item;
            issue.index = index.toString();
            const updatedData = { index: index.toString() };
            await updateIssueMemo(issue.uuid, updatedData);
          })
        );
      } catch (error) {
        console.error("Error: ", error);
      }
      return;
    } else {
      const sourceColumnId = source.droppableId,
        destinationColumnId = destination.droppableId;

      const sourceItems = [...dataSet[sourceColumnId].itemsOrder];
      const destinationItems = [...dataSet[destinationColumnId].itemsOrder];
      const [movedItem] = sourceItems.splice(source.index, 1);

      destinationItems.splice(destination.index, 0, movedItem);
      const newData = { ...dataSet };
      newData[sourceColumnId].itemsOrder = sourceItems;
      newData[destinationColumnId].itemsOrder = destinationItems;
      setDataSet(newData);

      //update index for destination column
      await Promise.all(
        destinationItems
          .filter((item) => item.index >= destination.index)
          .map(async (item) => {
            const issue = item;
            issue.index = (parseInt(issue.index) + 1).toString();
            const updatedData = {
              index: (parseInt(issue.index) + 1).toString(),
            };
            await updateIssueMemo(issue.uuid, updatedData);
          })
      );

      //update index for source column
      await Promise.all(
        sourceItems
          .filter((item) => item.index > source.index)
          .map(async (item) => {
            const issue = item;
            issue.index = (parseInt(issue.index) - 1).toString();
            const updatedData = {
              index: (parseInt(issue.index) - 1).toString(),
            };
            await updateIssueMemo(issue.uuid, updatedData);
          })
      );
    }
    if (source.droppableId === destination.droppableId) return;
    else console.log("hello");
    //update state
    try {
      const issue = await readIssueMemo(draggableId);
      console.log("reading issue", issue);
      const updatedData =
        destination.droppableId === "Unassigned"
          ? { category: "" }
          : { category: destination.droppableId };
      await updateIssueMemo(issue.uuid, updatedData);
    } catch (error) {
      console.error("Error: ", error);
    }
    onEditIssue();
    return;
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className="clusterContainer">
        {Object.values(dataSet).map((column) => (
          <ClusterColumn
            key={column.id}
            title={column.title}
            issues={getItemListForColumn(column.id)}
            id={column.id}
            onEditIssue={onEditIssue}
          />
        ))}
      </div>
    </DragDropContext>
  );
}

export default IssueClusterElement;
