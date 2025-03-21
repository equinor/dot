import React, { useState } from "react";
import TabsComponent from "./tabsComponent";
import { tabsConfig } from "./tabsConfig";

function FramingTabs() {
  const [activeTab, setActiveTab] = useState(0);
  const framingTabs = tabsConfig.filter((tab) => tab.parent === "framing");

  return (
    <div className="framingTab">
      <TabsComponent
        tabs={framingTabs}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />
    </div>
  );
}

export default FramingTabs;
