import React from "react";
import { Outlet } from "react-router-dom";
import AppHeader from "./NavBar";

const Layout = () => {
  return (
    <>
      <AppHeader />
      <Outlet />
    </>
  );
};

export default Layout;
