import { Droppable } from "react-beautiful-dnd";
import Issue from "./Issue";
import { Button, Icon } from "@equinor/eds-core-react";
import { chevron_up, chevron_down } from "@equinor/eds-icons";
import useSortableData from "../services/tableSort";
import "../styles/clusterTable.css";
import "../styles/issueListStyle.css";

export default function ClusterColumn({ title, issues, id, onEditIssue }) {
  const { items, requestSort, sortConfig } = useSortableData(issues);
  const getClassNamesFor = (name) => {
    if (!sortConfig) {
      return;
    }
    return sortConfig.key === name ? sortConfig.direction : undefined;
  };

  return (
    <div className="catContainer">
      <div className="containerHead" style={{ position: "stick" }}>
        <div className="containerHeading"> {title}</div>
        <div className="sortingButton">
          <Button
            variant="ghost"
            onClick={() => requestSort("index", "ascending")}
            className={getClassNamesFor("index")}
            id="sortingActionButton"
          >
            <Icon data={chevron_up} />
          </Button>
          <Button
            variant="ghost"
            onClick={() => requestSort("index", "descending")}
            className={getClassNamesFor("index")}
            id="sortingActionButton"
          >
            <Icon data={chevron_down} />
          </Button>{" "}
        </div>
      </div>
      <div className="scrollContainer">
        <Droppable droppableId={id} isCombineEnabled>
          {(provided, snapshot) => (
            <div
              className="dropContainer"
              ref={provided.innerRef}
              {...provided.droppableProps}
              isDraggingOver={snapshot.isDraggingOver}
            >
              {items?.map((issue, index) => (
                <Issue
                  key={issue.uuid}
                  index={index}
                  issue={issue}
                  onEditIssue={onEditIssue}
                />
              ))}
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </div>
    </div>
  );
}
