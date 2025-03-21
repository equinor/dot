import React, { useState } from "react";
import {
  TextField,
  Button,
  Icon,
  Divider,
  Table,
} from "@equinor/eds-core-react";
import {
  arrow_drop_down,
  arrow_drop_up,
  delete_forever,
} from "@equinor/eds-icons";

function CommentList({
  comments,
  cellId,
  setEditingCell,
  handleDeleteComment,
}) {
  const [isExtended, setIsExtended] = useState(false);

  const handleToggle = (e) => {
    setIsExtended(!isExtended);
    e.stopPropagation();
  };

  const commentsArray = Array.isArray(comments)
    ? comments.slice().reverse()
    : []; // Reverse to show the latest comment first
  const commentsToShow = isExtended ? commentsArray : commentsArray.slice(0, 2);
  return (
    <div onClick={(e) => setEditingCell(cellId)}>
      {commentsArray.length > 0 ? (
        <>
          <Table
            className="commentTable"
            density="compact"
            style={{ width: "100%" }}
          >
            {commentsToShow.map((comment, index) => (
              <Table.Row key={index}>
                <Table.Cell style={{ width: "65%" }}>
                  {comment.comment}
                </Table.Cell>
                <Table.Cell style={{ width: "20px" }}>
                  {comment.author}
                </Table.Cell>
                <Table.Cell style={{ textAlign: "right" }}>
                  <Button
                    variant="ghost_icon"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteComment(cellId, index);
                    }}
                  >
                    <Icon data={delete_forever} />
                  </Button>
                </Table.Cell>
              </Table.Row>
            ))}
          </Table>
          {commentsArray.length > 2 && (
            <Button variant="ghost_icon" onClick={handleToggle}>
              {isExtended ? (
                <Icon data={arrow_drop_up} />
              ) : (
                <Icon data={arrow_drop_down} />
              )}
            </Button>
          )}
        </>
      ) : (
        <div style={{ display: "flex", alignItems: "center" }}>
          {" "}
          <p> </p>{" "}
        </div>
      )}
    </div>
  );
}

export function CommentCell({
  cellValue,
  handleCommentChange,
  handleBlur,
  editingCell,
  setEditingCell,
  setCellValue,
  handleDeleteComment,
  info,
}) {
  const cellId = `${info.row.original.uuid}_comments`;
  const objectValue = cellValue[cellId] || info.row.getValue("comments");
  const currentValue = objectValue; /* Array.isArray(objectValue)
    ? objectValue.map((commentObj) => commentObj.comment)
    : []; */
  const [comments, setComments] = useState(currentValue);

  //The currentValue is overwritten and thus will be empty if we start typing
  return (
    <>
      <CommentList
        comments={comments}
        cellId={cellId}
        setEditingCell={setEditingCell}
        handleDeleteComment={handleDeleteComment}
      />
      {editingCell === cellId ? (
        <TextField
          value={cellValue[cellId]}
          onChange={(e) => handleCommentChange(e, cellId)}
          onBlur={handleBlur}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleBlur();
            } else if (e.key === "Escape") {
              setEditingCell(null);
            }
          }}
          autoFocus
        />
      ) : (
        <> </>
      )}
    </>
  );
}
