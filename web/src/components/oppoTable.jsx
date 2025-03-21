import React, { useState } from "react";
import { Button, Icon, Table, Typography } from "@equinor/eds-core-react";
import { delete_forever, chevron_up, chevron_down } from "@equinor/eds-icons";
import { removeOpportunity } from "../services/opportunity_api";
import useSortableData from "../services/tableSort";

function DisplayOpportunities({ opp, onEditIssue }) {
  /*Remove Issue*/
  const handleRemoveClick = async (event) => {
    const opportunityID = event.target.getAttribute("data-tag");

    try {
      await removeOpportunity(opportunityID);
      onEditIssue();
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  const { items, requestSort, sortConfig } = useSortableData(opp);
  const getClassNamesFor = (name) => {
    if (!sortConfig) {
      return;
    }
    return sortConfig.key === name ? sortConfig.direction : undefined;
  };

  const [hoveredCell, setHoveredCell] = useState(null);
  const handleCellMouseEnter = (cellID) => {
    setHoveredCell(cellID);
  };
  const handleCellMouseLeave = () => {
    setHoveredCell(null);
  };

  return (
    <div className="displayTable">
      <Table className="oppTable">
        <Table.Caption>
          <Typography variant="h2">Opportunity Statement</Typography>
        </Table.Caption>
        <Table.Head>
          <Table.Row>
            <Table.Cell>
              Statement
              <div className="sortingButton">
                <Button
                  variant="ghost"
                  onClick={() => requestSort("statement", "ascending")}
                  className={getClassNamesFor("statement")}
                  id="sortingActionButton"
                >
                  <Icon data={chevron_up} />
                </Button>
                <Button
                  variant="ghost"
                  onClick={() => requestSort("statement", "descending")}
                  className={getClassNamesFor("statement")}
                  id="sortingActionButton"
                >
                  <Icon data={chevron_down} />
                </Button>{" "}
              </div>
            </Table.Cell>
          </Table.Row>
        </Table.Head>
        <Table.Body>
          {items?.map((opportunity) => (
            <Table.Row key={opportunity.uuid}>
              <Table.Cell
                className={
                  hoveredCell === opportunity.id ? "hoveredCell" : "oppCell"
                }
              >
                {opportunity.description}
                <Button
                  variant="ghost"
                  data-tag={opportunity.uuid}
                  onClick={handleRemoveClick}
                  className="removeButton"
                >
                  <Icon data={delete_forever} title="delete" />
                </Button>
              </Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table>
    </div>
  );
}

export default DisplayOpportunities;
