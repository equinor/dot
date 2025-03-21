import React, { useState, useEffect } from "react";
import { Radio, Autocomplete } from "@equinor/eds-core-react";
import { useFilterList } from "./gridFilterContext";

// State variable for filtering type
let filteringType = "OR";

// Custom filter function for "contains element in array"
export function arrIncludes(row, columnId, filterValue) {
  const cellValue = row.getValue(columnId);
  if (!filterValue || filterValue.length === 0) {
    return true;
  }
  if (filteringType === "OR") {
    return filterValue.some((filterVal) => cellValue.includes(filterVal));
  }
  if (filteringType === "AND") {
    return filterValue.every((filterVal) => cellValue.includes(filterVal));
  }
}

// Select from AutoComplete Filter component
export const SelectFilterComponent = ({ listNum = 0, onChange, value }) => {
  const { filterList } = useFilterList();
  const [checked, setChecked] = useState(filteringType);
  const [selectedValues, setSelectedValues] = useState(value || []);

  useEffect(() => {
    filteringType = checked;
  }, [checked]);

  useEffect(() => {
    setSelectedValues(value || []); // Update selectedValues when value prop changes
  }, [value]);

  const handleSelections = (e) => {
    setSelectedValues(e.selectedItems);
    onChange(e.selectedItems);
  };
  return (
    <>
      <Radio
        label="OR"
        name="group"
        value="OR"
        checked={checked === "OR"}
        onChange={(e) => setChecked(e.target.value)}
        defaultChecked
      />
      <Radio
        label="AND"
        name="group"
        value="AND"
        checked={checked === "AND"}
        onChange={(e) => setChecked(e.target.value)}
      />
      <Autocomplete
        label="Select multiple labels"
        options={filterList[listNum]}
        multiple
        initialSelectedOptions={selectedValues}
        value={selectedValues}
        onOptionsChange={handleSelections}
      />
    </>
  );
};
