import React from "react";
import { Routes, Route } from "react-router-dom";

import Home from "../pages/Home";
import Signup from "../pages/Signup";

const Main = () => {
  return (
    <Routes>
      <Route path="/" element={Home}></Route>
      <Route path="/signup" element={Signup}></Route>
    </Routes>
  );
};

export default Main;
