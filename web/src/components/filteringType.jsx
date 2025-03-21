import { useState } from "react";

export const useFilteringType = () => {
  const [filteringType, setFilteringType] = useState("OR");
  return { filteringType, setFilteringType };
};
