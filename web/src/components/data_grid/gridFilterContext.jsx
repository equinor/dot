import React, { createContext, useState, useContext } from "react";

// Create a context for issueList
const FilterListContext = createContext();

// Create a provider component
export const FilterListProvider = ({ children }) => {
  const [filterList, setFilterList] = useState([]);

  return (
    <FilterListContext.Provider value={{ filterList, setFilterList }}>
      {children}
    </FilterListContext.Provider>
  );
};

// Create a custom hook to use the IssueListContext
export const useFilterList = () => {
  return useContext(FilterListContext);
};
