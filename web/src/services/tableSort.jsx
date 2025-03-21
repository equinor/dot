import { useState, useMemo } from "react";

const useSortableData = (items, config = null) => {
  const [sortConfig, setSortConfig] = useState(config);

  const sortedItems = useMemo(() => {
    let sortableItems;
    if (items?.length === 0) {
      sortableItems = [];
    } else {
      sortableItems = items ? [...items] : [];
    }

    if (sortConfig !== null) {
      sortableItems?.sort((a, b) => {
        if (a[sortConfig.key] < b[sortConfig.key]) {
          return sortConfig.direction === "ascending" ? -1 : 1;
        }
        if (a[sortConfig.key] > b[sortConfig.key]) {
          return sortConfig.direction === "ascending" ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [items, sortConfig]);

  const requestSort = (key, order) => {
    let direction = "ascending";
    order === "ascending"
      ? (direction = "ascending")
      : (direction = "descending");
    setSortConfig({ key, direction });
  };

  return { items: sortedItems, requestSort, sortConfig };
};

export default useSortableData;
