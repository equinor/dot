import { Link, Outlet, useLocation } from "react-router-dom";
import React, { useEffect } from "react";
import { Tabs } from "@equinor/eds-core-react";

function TabsComponent({ tabs, activeTab, setActiveTab }) {
  const location = useLocation();

  const handleTabChange = (index) => {
    setActiveTab(index);
  };

  useEffect(() => {
    const activeIndex = tabs.findIndex((tab) =>
      location.pathname.startsWith(tab.path)
    );
    setActiveTab(activeIndex !== -1 ? activeIndex : 0);
  }, [location.pathname, tabs, setActiveTab]);

  return (
    <div className="tabsContainer">
      <Tabs activeTab={activeTab} onChange={handleTabChange}>
        <Tabs.List>
          {tabs.map((tab) => (
            <Tabs.Tab key={tab.id} id={tab.id} as={Link} to={tab.path}>
              {tab.label}
            </Tabs.Tab>
          ))}
        </Tabs.List>
        <Outlet />
      </Tabs>
    </div>
  );
}

export default TabsComponent;
