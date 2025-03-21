import React, { useState } from "react";
import {
  Button,
  Icon,
  Table,
  Typography,
  Search,
  Chip,
} from "@equinor/eds-core-react";
import {
  clear,
  delete_forever,
  edit,
  chevron_up,
  chevron_down,
  done,
} from "@equinor/eds-icons";
import useSortableData from "../services/tableSort";
import { readOutEdges } from "../services/edge_api";
import {
  readObjectives,
  removeObjective,
  updateObjective,
} from "../services/objective_api";
import ValueMetricDialog from "./valueMetricDialog";

function ObjectivesTable({ objectives, onEditIssue }) {
  /* -------------
      Search
      ----------------*/
  const [search, setSearch] = useState("");
  const handleSearch = (event) => {
    setSearch(event.target.value);
  };
  const data = objectives?.filter(
    (item) =>
      String(item.description).includes(search) ||
      String(item.tag).includes(search) ||
      String(item.hierarchy).includes(search)
  );
  const { items, requestSort, sortConfig } = useSortableData(data);
  const getClassNamesFor = (name) => {
    if (!sortConfig) {
      return;
    }
    return sortConfig.key === name ? sortConfig.direction : undefined;
  };

  /*----------------
  Get associated value metrics
  ------------------*/
  const getValueMetric = async (objectiveID) => {
    const outEdges = await readOutEdges(objectiveID, "has_value_metric");
  };

  /*----------------
  add value metric when button clicked
  ------------------*/

  /*--------------
    Remove Row
    ----------------*/
  const handleRemoveClick = async (event) => {
    const objectiveID = event.target.getAttribute("data-tag");

    try {
      await removeObjective(objectiveID);
      onEditIssue();
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  /*--------------
    Edit Rows
    ---------------*/

  const [inEditMode, setInEditMode] = useState({
    status: false,
    key: null, //row ID
  });

  const [objDescription, setObjDescription] = useState(null);
  const [objLabelText, setObjLabelText] = useState(null);
  const [objCategoryText, setObjCategoryText] = useState("Fact");

  const onEdit = ({
    objectiveID,
    currentDescription,
    currentLabelText,
    currentCategoryText,
  }) => {
    setInEditMode({
      status: true,
      key: objectiveID,
    });

    setObjDescription(currentDescription);
    setObjLabelText(currentLabelText);
    setObjCategoryText(currentCategoryText);
  };

  const updateData = async ({
    objectiveID,
    newDescription,
    newLabelText,
    newCategoryText,
  }) => {
    console.log("obj ID", objectiveID);
    const updatedObjective = {
      description: newDescription.toString(),
      hierarchy: newCategoryText.toString(),
      tag:
        typeof newLabelText === "string"
          ? newLabelText.split(/\r?\n/).flatMap((line) => line.split(","))
          : newLabelText,
    };
    await updateObjective(objectiveID, updatedObjective)
      .then(onCancel())
      .then(onEditIssue);
    console.log(
      "Update: ObjName to: ",
      newDescription,
      " Tag to ",
      newLabelText,
      " and Category to ",
      newCategoryText
    );
  };

  const onCancel = () => {
    setInEditMode({
      status: false,
      key: null,
    });
    setObjDescription(null);
    setObjCategoryText("Fact");
    setObjLabelText(null);
  };

  return (
    <div className="displayTable">
      <div id="issueListSearch">
        <form>
          <Search aria-label="Search for objectives" onChange={handleSearch} />
        </form>
      </div>
      <Table className="issueListTable">
        <Table.Caption>
          <Typography variant="h2">Objectives</Typography>
        </Table.Caption>
        <Table.Head sticky>
          <Table.Row>
            <Table.Cell>
              Objective
              <div className="sortingButton">
                <Button
                  variant="ghost"
                  onClick={() => requestSort("description", "ascending")}
                  className={getClassNamesFor("description")}
                  id="sortingActionButton"
                >
                  <Icon data={chevron_up} />
                </Button>
                <Button
                  variant="ghost"
                  onClick={() => requestSort("description", "descending")}
                  className={getClassNamesFor("description")}
                  id="sortingActionButton"
                >
                  <Icon data={chevron_down} />
                </Button>{" "}
              </div>
            </Table.Cell>
            <Table.Cell>
              Category
              <div className="sortingButton">
                <Button
                  variant="ghost"
                  onClick={() => requestSort("hierarchy", "ascending")}
                  className={getClassNamesFor("hierarchy")}
                  id="sortingActionButton"
                >
                  <Icon data={chevron_up} />
                </Button>
                <Button
                  variant="ghost"
                  onClick={() => requestSort("hierarchy", "descending")}
                  className={getClassNamesFor("hierarchy")}
                  id="sortingActionButton"
                >
                  <Icon data={chevron_down} />
                </Button>
              </div>
            </Table.Cell>
            <Table.Cell>
              Label
              <div className="sortingButton">
                <Button
                  variant="ghost"
                  onClick={() => requestSort("tag", "ascending")}
                  className={getClassNamesFor("tag")}
                  id="sortingActionButton"
                >
                  <Icon data={chevron_up} />
                </Button>
                <Button
                  variant="ghost"
                  onClick={() => requestSort("tag", "descending")}
                  className={getClassNamesFor("tag")}
                  id="sortingActionButton"
                >
                  <Icon data={chevron_down} />
                </Button>
              </div>
            </Table.Cell>
            <Table.Cell>
              Value Metric
              <div className="sortingButton">
                <Button
                  variant="ghost"
                  onClick={() => requestSort("tag", "ascending")}
                  className={getClassNamesFor("tag")}
                  id="sortingActionButton"
                >
                  <Icon data={chevron_up} />
                </Button>
                <Button
                  variant="ghost"
                  onClick={() => requestSort("tag", "descending")}
                  className={getClassNamesFor("tag")}
                  id="sortingActionButton"
                >
                  <Icon data={chevron_down} />
                </Button>
              </div>
            </Table.Cell>
            <Table.Cell>Action</Table.Cell>
          </Table.Row>
        </Table.Head>
        <Table.Body>
          {items?.map((objective) => (
            <Table.Row key={objective.uuid}>
              <Table.Cell className="issueTableCell">
                {inEditMode.status && inEditMode.key === objective.uuid ? (
                  <input
                    value={objDescription}
                    id="tableTextInput"
                    onChange={(event) => setObjDescription(event.target.value)}
                  />
                ) : (
                  objective.description
                )}
              </Table.Cell>
              <Table.Cell className="issueTableCell">
                {inEditMode.status && inEditMode.key === objective.uuid ? (
                  <select
                    id="tableTextInput"
                    onChange={(event) => setObjCategoryText(event.target.value)}
                  >
                    <option value="Strategic">Strategic</option>
                    <option value="Fundamental">Fundamental</option>
                    <option value="Mean">Mean</option>
                  </select>
                ) : (
                  objective.hierarchy
                )}
              </Table.Cell>
              <Table.Cell className="issueTableCell">
                {inEditMode.status && inEditMode.key === objective.uuid ? (
                  <input
                    value={objLabelText}
                    id="tableTextInput"
                    onChange={(event) => setObjLabelText(event.target.value)}
                  />
                ) : (
                  <div style={{ display: "flex", flexWrap: "wrap" }}>
                    {objective.tag.map((tag, index) => (
                      <Chip key={index}>{tag}</Chip>
                    ))}
                  </div>
                )}
              </Table.Cell>
              <Table.Cell>
                <ValueMetricDialog
                  objective={objective}
                  onEditIssue={onEditIssue}
                />
              </Table.Cell>
              <Table.Cell>
                <Button
                  variant="ghost"
                  onClick={handleRemoveClick}
                  data-tag={objective.uuid}
                  id="actionButton"
                >
                  <Icon data={delete_forever} title="delete" />
                </Button>
                {inEditMode.status && inEditMode.key === objective.uuid ? (
                  <React.Fragment>
                    <Button
                      variant="ghost"
                      id="actionButton"
                      onClick={() =>
                        updateData({
                          objectiveID: objective.uuid,
                          newDescription: objDescription,
                          newCategoryText: objCategoryText,
                          newLabelText: objLabelText,
                        })
                      }
                    >
                      <Icon data={done} title="save" />
                    </Button>
                    <Button
                      variant="ghost"
                      id="actionButton"
                      onClick={() => onCancel()}
                    >
                      <Icon data={clear} title="clear" />
                    </Button>
                  </React.Fragment>
                ) : (
                  <Button
                    variant="ghost"
                    data-tag={objective.uuid}
                    id="actionButton"
                    onClick={() =>
                      onEdit({
                        objectiveID: objective.uuid,
                        currentDescription: objective.description,
                        currentCategoryText: objective.hierarchy,
                        currentLabelText: objective.tag,
                      })
                    }
                  >
                    <Icon data={edit} title="edit" />
                  </Button>
                )}
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    </div>
  );
}

export default ObjectivesTable;
