import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import TabsComponent from "./tabsComponent";

function AppHeader() {
  const location = useLocation();
  const [activeMainTab, setActiveMainTab] = useState(0);

  const mainTabs = [
    { id: "framingTab", label: "Framing", path: "/framing" },
    { id: "structuringTab", label: "Structuring", path: "/structuring" },
    { id: "analysisTab", label: "Analysis", path: "/analysis" },
  ];

  useEffect(() => {
    const activeIndex = mainTabs.findIndex((tab) =>
      location.pathname.startsWith(tab.path)
    );
    setActiveMainTab(activeIndex !== -1 ? activeIndex : 0);
  }, [location.pathname, mainTabs]);

  return (
    <div className="header">
      <TabsComponent
        tabs={mainTabs}
        activeTab={activeMainTab}
        setActiveTab={setActiveMainTab}
      />
    </div>
  );
}

export default AppHeader;
