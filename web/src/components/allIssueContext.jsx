import React, { createContext, useState, useContext } from "react";

// Create a context for issueList
const IssueListContext = createContext();

// Create a provider component
export const IssueListProvider = ({ children }) => {
  const [issueList, setIssueList] = useState([]);

  return (
    <IssueListContext.Provider value={{ issueList, setIssueList }}>
      {children}
    </IssueListContext.Provider>
  );
};

// Create a custom hook to use the IssueListContext
export const useIssueList = () => {
  return useContext(IssueListContext);
};
