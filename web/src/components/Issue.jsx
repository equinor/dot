import React, { useState, useEffect } from "react";
import { Draggable } from "react-beautiful-dnd";
import {
  Button,
  Icon,
  Card,
  Typography,
  Chip,
  Tooltip,
} from "@equinor/eds-core-react";
import { delete_forever, swap_horizontal } from "@equinor/eds-icons";
import { removeIssue, unMergeIssue } from "../services/issue_api";
import "../styles/clusterTable.css";
import { readInEdges } from "../services/edge_api";
import { useProjectContext } from "../components/context";

export default function Issue({ issue, index, onEditIssue }) {
  const [isIssueMerged, setIsIssueMerged] = useState(false);
  const [project] = useProjectContext();
  /*Remove Issue*/
  const handleRemoveClick = async (event) => {
    const issueID = event.target.getAttribute("data-tag");

    try {
      await removeIssue(issueID);
      onEditIssue();
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  const checkIsIssueMerged = async () => {
    const list = await readInEdges(issue.uuid, "merged_into");
    setIsIssueMerged(list.length > 0);
  };

  const handleUnMergeClick = async (event) => {
    const issueID = event.target.getAttribute("data-tag");
    console.log("Unmerging the issue: ", issueID);
    try {
      await unMergeIssue(project, issueID);
      onEditIssue();
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  useEffect(() => {
    checkIsIssueMerged();
  }, [issue]);

  return (
    <Draggable
      draggableId={issue.uuid.toString()}
      key={issue.uuid}
      index={index}
    >
      {(provided, snapshot) => (
        <div
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          ref={provided.innerRef}
          isDragging={snapshot.isDragging}
        >
          <Card className="itemContainer">
            <Card.Header>
              <Card.HeaderTitle>
                <Typography variant="h5">{issue.shortname}</Typography>
              </Card.HeaderTitle>
            </Card.Header>
            <Card.Content>
              <div>{issue.description} </div>
            </Card.Content>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "0.5fr 2fr",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <Card.Actions
                style={{
                  display: "flex",
                  alignItems: "center",
                  paddingBottom: "16px",
                }}
              >
                <Button
                  variant="ghost"
                  data-tag={issue.uuid}
                  onClick={handleRemoveClick}
                  className="removeButton"
                >
                  <Icon data={delete_forever} />
                </Button>
                {isIssueMerged && (
                  <Tooltip title="Un-merging of issues">
                    <Button
                      variant="ghost"
                      data-tag={issue.uuid}
                      onClick={handleUnMergeClick}
                      className="unmergeButton"
                    >
                      <Icon data={swap_horizontal} />
                    </Button>
                  </Tooltip>
                )}
              </Card.Actions>
              <Card.Content style={{ display: "flex" }}>
                <div
                  style={{
                    display: "flex",
                    flexWrap: "wrap",
                    width: "100%",
                    marginLeft: "auto",
                    marginRight: "0",
                    justifyContent: "flex-end",
                  }}
                >
                  {issue.tag.map((tag, index) => (
                    <Chip
                      key={index}
                      style={{ marginBottom: "5px", marginRight: "5px" }}
                    >
                      {tag}
                    </Chip>
                  ))}
                </div>
              </Card.Content>
            </div>
          </Card>
          {provided.placeholder}
        </div>
      )}
    </Draggable>
  );
}
