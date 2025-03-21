export const getIssueRows = (issueList) => {
  return issueList.map((issue) => ({
    index: issue.index,
    description: issue.description,
    category: issue.category,
    boundary: issue.boundary,
    tag: issue.tag,
    shortname: issue.shortname,
    uuid: issue.uuid,
    date: issue.date,
    comments: issue.comments,
  }));
};
