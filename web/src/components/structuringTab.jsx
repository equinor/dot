import React, { useState } from "react";
import TabsComponent from "./tabsComponent";
import { tabsConfig } from "./tabsConfig";

function StructuringTab() {
  const [activeTab, setActiveTab] = useState(0);
  const structuringTabs = tabsConfig.filter(
    (tab) => tab.parent === "structuring"
  );

  return (
    <div className="framingTab">
      <TabsComponent
        tabs={structuringTabs}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />
    </div>
  );
}

export default StructuringTab;
