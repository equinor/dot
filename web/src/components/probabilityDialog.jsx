import React, { useState, useEffect } from "react";
import {
  Button,
  Icon,
  Table,
  Typography,
  Dialog,
  TextField,
  Switch,
  Autocomplete,
} from "@equinor/eds-core-react";
import { add, delete_forever, edit } from "@equinor/eds-icons";
import { readIssues, readIssue, updateIssue } from "../services/issue_api";
import { addEdge } from "../services/edge_api";
import { useProjectContext } from "./context";
import "../styles/issueListStyle.css";

export default function ProbabilityDialog({ issue, onEditIssue }) {
  const [project] = useProjectContext();
  const Epsilon = 1e-6;

  const [issueList, setIssueList] = useState([]);
  const [isConditional, setIsConditional] = useState(false);
  const [isOpen, setIsOpen] = useState(false);
  const [outcomes, setOutcomes] = useState(null);
  const [outcomeName, setOutcomeName] = useState([]);
  const [outcomeProbability, setOutcomeProbability] = useState([[]]);
  const [influenceNode, setInfluenceNode] = useState(null);
  const [influenceNodeShortname, setInfluenceNodeShortname] = useState("");
  const [influenceNodeUUID, setInfluenceNodeUUID] = useState("");
  const [, setUpdatedInfluenceNode] = useState(false);

  const fetchData = async () => {
    const updatedData = await readIssues(project);
    setIssueList(updatedData);
  };

  const handleOpen = async () => {
    await fetchData();
    if (issue.probabilities === null) {
      var probability = {
        dtype: "DiscreteUnconditionalProbability",
        probability_function: [[1.0]],
        variables: { Node1: ["Outcome"] },
      };
      const firstOutcome = Object.keys(probability.variables)[0];
      setOutcomeName(probability.variables[firstOutcome]);
      console.log(probability.variables[firstOutcome]);
      setOutcomeProbability(probability.probability_function);
    } else {
      if (issue.probabilities.variables) {
        const firstOutcome = Object.keys(issue.probabilities.variables)[0];
        setOutcomeName(issue.probabilities.variables[firstOutcome]);
        console.log(issue.probabilities.variables[firstOutcome]);
        setOutcomeProbability(issue.probabilities.probability_function);
      }
    }

    if (issue.influenceNodeUUID !== "") {
      setUpdatedInfluenceNode(true);
      setIsConditional(true);
      setInfluenceNodeUUID(issue.influenceNodeUUID);
    }

    if (influenceNode) {
      setInfluenceNodeShortname(influenceNode.shortname);
    }

    setIsOpen(true);
    console.log(
      "open",
      issueList?.filter(
        (issue_in_list) =>
          ((String(issue_in_list.category).includes("Uncertainty") &&
            String(issue_in_list.keyUncertainty).includes("true")) ||
            (String(issue_in_list.category).includes("Decision") &&
              String(issue_in_list.decisionType).includes("Focus"))) &&
          issue_in_list.uuid !== issue.uuid
      )
    );
  };

  const handleClose = () => {
    setIsOpen(false);
    setOutcomeName([]);
    setOutcomeProbability([[]]);
  };

  const handleSave = async () => {
    //check if Probabilities sum to 1 for simple case
    function closeToOne(numbers) {
      for (let number of numbers) {
        if (Math.abs(number - 1) > Epsilon) {
          alert(
            "Sum of probabilities is not equal to 1. Please adjust probabilities."
          );
          return false;
        }
      }
      return true;
    }
    if (closeToOne(columnSums)) {
      console.log("sum is 1 always");
      const issueRead = await readIssue(issue.uuid);
      if (issueRead.probabilities === null) {
        issueRead.probabilities = {
          dtype: "DiscreteUnconditionalProbability",
          probability_function: [[1.0]],
          variables: { Node1: ["Outcome"] },
        };
      }
      if (influenceNodeUUID && influenceNodeUUID !== "") {
        console.log("Saving");
        issueRead.influenceNodeUUID = influenceNode.uuid;
        await addEdge(
          influenceNodeUUID.toString(),
          issue.uuid.toString(),
          "influences"
        );
      }
      console.log("Saving");
      issueRead.alternatives = outcomeName;
      if (isConditional) {
        issueRead.probabilities.dtype = "DiscreteConditionalProbability";
        if (influenceNode.category === "Decision") {
          issueRead.probabilities.variables = {
            [issueRead.shortname]: outcomeName,
            [influenceNodeShortname]: influenceNode.alternatives,
          };
        } else {
          issueRead.probabilities.variables = {
            [issueRead.shortname]: outcomeName,
            [influenceNodeShortname]:
              influenceNode.probabilities.variables[influenceNodeShortname],
          };
        }
      } else {
        issueRead.probabilities.dtype = "DiscreteUnconditionalProbability";
        issueRead.probabilities.variables = {
          [issueRead.shortname]: outcomeName,
        };
      }
      issueRead.probabilities.probability_function = outcomeProbability;
      await updateIssue(issueRead.uuid, issueRead) //TODO: remove issueRead and use dict instead
        .then(fetchData)
        .then(onEditIssue)
        .then(handleClose)
        .catch((error) => {
          console.error("Promise rejection:", error);
        });
    }
  };

  const handleNodeSelect = (selected) => {
    console.log("handle node select");
    setUpdatedInfluenceNode(false);
    console.log("Selected", selected.selectedItems[0]);
    setInfluenceNode(selected.selectedItems[0]);
    setInfluenceNodeUUID(selected.selectedItems[0].uuid);
    let rows = outcomeName.length;
    let cols = selected.selectedItems[0].alternatives.length;

    const nestedArray = [];

    for (let i = 0; i < rows; i++) {
      const row = [];
      for (let j = 0; j < cols; j++) {
        row.push(0);
      }
      nestedArray.push(row);
    }
    setOutcomeProbability(nestedArray);
  };

  useEffect(() => {
    setUpdatedInfluenceNode(true);
    const fetchInfluenceNode = async () => {
      if (influenceNodeUUID && influenceNodeUUID !== "") {
        const infNode = await readIssue(influenceNodeUUID.toString());
        console.log("Inf Node:", infNode);
        setInfluenceNode(infNode);
        setInfluenceNodeShortname(infNode.shorname);
      }
    };
    fetchInfluenceNode();
  }, [influenceNodeUUID]);

  useEffect(() => {
    if (influenceNode) {
      console.log("Inf Node selected.......");
      setInfluenceNodeShortname(influenceNode.shortname);
    } else {
      console.log("No Inf Node");
    }
  }, [influenceNode]);

  const addNewRow = () => {
    setOutcomeName([...outcomeName, ""]);
    setOutcomeProbability((outcomeProbability) => [
      ...outcomeProbability,
      Array(outcomeProbability[0].length).fill(0),
    ]);
  };

  const removeRow = (index) => {
    const updatedNames = [...outcomeName];
    updatedNames.splice(index, 1);

    const updatedProbabilities = [...outcomeProbability];
    updatedProbabilities.splice(index, 1);

    setOutcomeName(updatedNames);
    setOutcomeProbability(updatedProbabilities);
  };

  const handleOutcomeNameChange = (value, index) => {
    const updatedNames = [...outcomeName];
    updatedNames[index] = value;
    setOutcomeName(updatedNames);
  };

  const handleOutcomeProbabilityChange = (value, rowIndex, columnIndex = 0) => {
    const updatedProbabilities = [...outcomeProbability];
    updatedProbabilities[rowIndex][columnIndex] = parseFloat(value);
    setOutcomeProbability(updatedProbabilities);
  };

  const handleCheck = (e) => {
    setIsConditional(e.target.checked);
  };

  const transposedArray = outcomeProbability[0]?.map((col, i) =>
    outcomeProbability?.map((row) => row[i])
  );
  const columnSums = transposedArray?.map((col) => {
    return col.reduce((sum, value) => sum + value, 0);
  });

  return (
    <div>
      <Button
        aria-haspopup="dialog"
        className="uncertaintyEditButton"
        data-tag={issue.uuid}
        variant="ghost"
        onClick={handleOpen}
      >
        <Icon data={edit} title="edit" />
      </Button>
      <Dialog
        className="uncertaintyDialog"
        open={isOpen}
        isDismissable
        onClose={handleClose}
      >
        <Dialog.Header>
          <Dialog.Title>{"Probabilities - " + issue.shortname}</Dialog.Title>
        </Dialog.Header>
        <Dialog.CustomContent>
          <Typography variant="body_short">
            Please insert the probabilities for this uncertainty node.
          </Typography>
          <Switch
            label="Conditional Probabilities"
            onChange={(e) => handleCheck(e)}
            checked={isConditional}
          />

          {isConditional ? (
            <div>
              Choose a Node:
              <Autocomplete
                className="issueSelect"
                label="Issues"
                value={influenceNodeShortname}
                options={issueList?.filter(
                  (issue_in_list) =>
                    ((String(issue_in_list.category).includes("Uncertainty") &&
                      String(issue_in_list.keyUncertainty).includes("true")) ||
                      (String(issue_in_list.category).includes("Decision") &&
                        String(issue_in_list.decisionType).includes(
                          "Focus"
                        ))) &&
                    issue_in_list.uuid !== issue.uuid
                )}
                optionLabel={(issue) => issue.shortname.toString()}
                //selectedOptions={issue.name}
                onOptionsChange={(selected) => {
                  handleNodeSelect(selected);
                }}
                autoWidth="false"
              />{" "}
            </div>
          ) : (
            <Typography variant="body_short">
              <div>Insert Probabilities</div>
            </Typography>
          )}

          {isConditional && influenceNode ? (
            <div className="tableContainer">
              <Table className="probabilityTable">
                <Table.Head>
                  <Table.Row>
                    <Table.Cell>Outcome</Table.Cell>
                    {influenceNode.alternatives?.map((outcome, index) => (
                      <Table.Cell key={index}>{outcome}</Table.Cell>
                    ))}
                    <Table.Cell className="probTableCell">
                      {" "}
                      Additional Outcome
                    </Table.Cell>
                    <Table.Cell>Action</Table.Cell>
                  </Table.Row>
                </Table.Head>
                <Table.Body>
                  {outcomeName?.map((outcome, index) => (
                    <Table.Row key={index}>
                      <Table.Cell className="probTableCell">
                        <TextField
                          className="probTableCell"
                          defaultValue={outcome}
                          onChange={(e) =>
                            handleOutcomeNameChange(e.target.value, index)
                          }
                        />
                      </Table.Cell>
                      {influenceNode.alternatives?.map((alt, index2) => (
                        <Table.Cell key={index2} className="probTableCell">
                          <TextField
                            type="number"
                            className="probTableCell"
                            defaultValue={outcomeProbability[index][index2]}
                            onChange={(e) =>
                              handleOutcomeProbabilityChange(
                                e.target.value,
                                index,
                                index2
                              )
                            }
                          />
                        </Table.Cell>
                      ))}
                      <Table.Cell className="probTableCell"></Table.Cell>
                      <Table.Cell className="probTableCell">
                        <Button
                          variant="ghost"
                          onClick={() => removeRow(index)}
                          id="actionButton"
                        >
                          <Icon data={delete_forever} />
                        </Button>
                      </Table.Cell>
                    </Table.Row>
                  ))}
                  <Table.Row>
                    <Table.Cell>
                      <Button
                        variant="ghost"
                        onClick={addNewRow}
                        id="actionButton"
                      >
                        <Icon data={add} />
                      </Button>
                    </Table.Cell>
                    {influenceNode.alternatives?.map((alt, index3) => (
                      <Table.Cell
                        key={index3}
                        className={`totalSumCell ${
                          Math.abs(columnSums[index3] - 1) < Epsilon
                            ? "greenTotal"
                            : "redTotal"
                        }`}
                      >
                        &Sigma; = {columnSums[index3]}
                      </Table.Cell>
                    ))}
                    <Table.Cell></Table.Cell>
                    <Table.Cell></Table.Cell>
                  </Table.Row>
                </Table.Body>
              </Table>
            </div>
          ) : (
            <div className="tableContainer">
              <Table>
                <Table.Head>
                  <Table.Row>
                    <Table.Cell>Outcome</Table.Cell>
                    <Table.Cell>Probability</Table.Cell>
                    <Table.Cell>Action</Table.Cell>
                  </Table.Row>
                </Table.Head>
                <Table.Body>
                  {outcomeName.map((name, index) => (
                    <Table.Row key={index}>
                      <Table.Cell className="probTableCell">
                        <TextField
                          defaultValue={name}
                          onChange={(e) => {
                            handleOutcomeNameChange(e.target.value, index);
                          }}
                        />
                      </Table.Cell>
                      <Table.Cell className="probTableCell">
                        <TextField
                          type="number"
                          defaultValue={outcomeProbability[index][0]}
                          onChange={(e) =>
                            handleOutcomeProbabilityChange(
                              e.target.value,
                              index
                            )
                          }
                        />
                      </Table.Cell>
                      <Table.Cell>
                        <Button
                          variant="ghost"
                          onClick={() => removeRow(index)}
                          id="actionButton"
                        >
                          <Icon data={delete_forever} />
                        </Button>
                      </Table.Cell>
                    </Table.Row>
                  ))}
                  <Table.Row>
                    <Table.Cell>
                      <Button
                        variant="ghost"
                        onClick={addNewRow}
                        id="actionButton"
                      >
                        <Icon data={add} />
                      </Button>
                    </Table.Cell>
                    <Table.Cell
                      className={`totalSumCell ${
                        Math.abs(columnSums[0] - 1) < Epsilon
                          ? "greenTotal"
                          : "redTotal"
                      }`}
                    >
                      &Sigma; = {columnSums[0]}
                    </Table.Cell>
                    <Table.Cell></Table.Cell>
                  </Table.Row>
                </Table.Body>
              </Table>
            </div>
          )}
        </Dialog.CustomContent>
        <Dialog.Actions>
          <Button
            data-tag={issue.uuid}
            className="saveButton"
            onClick={handleSave}
          >
            Save
          </Button>
          <Button onClick={handleClose}>Close</Button>
        </Dialog.Actions>
      </Dialog>
    </div>
  );
}
