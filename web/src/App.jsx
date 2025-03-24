/*
start with code in cmd: npm start
*/
import React from "react";
import "./styles/App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Framing from "./pages/framing";
import InfluenceDiagram from "./pages/id";
import DecisionTree from "./pages/dt";
import Home from "./pages/home";
import Header from "./components/header";
import Objectives from "./pages/objectives";
import Opportunity from "./pages/opportunity";
import IssueClustering from "./pages/issueClustering";
import DecisionHierarchy from "./pages/decisionHierarchy";
import Uncertainties from "./pages/uncertainties";
import Synthesis from "./pages/synthesis";

import ProjectPage from "./pages/project";
import Analysis from "./pages/analysis";
import { useProjectContext } from "./components/context";
import ErrorBoundary from "./pages/errorBoundary";
import ErrorPage from "./pages/errorPage";
import { IssueListProvider } from "./components/allIssueContext";
import { FilterListProvider } from "./components/data_grid/gridFilterContext";

function App() {
  useProjectContext();
  return (
    <Router>
      <Header />
      <Routes>
        <Route
          path="/"
          element={
            <ErrorBoundary>
              <Home />
            </ErrorBoundary>
          }
        />
        <Route
          path="/project"
          element={
            <ErrorBoundary>
              <ProjectPage />
            </ErrorBoundary>
          }
        />
        <Route
          path="/framing"
          element={
            <ErrorBoundary>
              <Opportunity />
            </ErrorBoundary>
          }
        />
        <Route
          path="/framing/opportunity"
          element={
            <ErrorBoundary>
              <Opportunity />
            </ErrorBoundary>
          }
        />
        <Route
          path="/framing/objectives"
          element={
            <ErrorBoundary>
              <Objectives />
            </ErrorBoundary>
          }
        />
        <Route
          path="/framing/issuelist"
          element={
            <ErrorBoundary>
              <IssueListProvider>
                <FilterListProvider>
                  <Framing />
                </FilterListProvider>
              </IssueListProvider>
            </ErrorBoundary>
          }
        />
        <Route
          path="/framing/clustering"
          element={
            <ErrorBoundary>
              <IssueClustering />
            </ErrorBoundary>
          }
        />
        <Route
          path="/framing/decisionHierarchy"
          element={
            <ErrorBoundary>
              <IssueListProvider>
                <FilterListProvider>
                  <DecisionHierarchy />
                </FilterListProvider>
              </IssueListProvider>
            </ErrorBoundary>
          }
        />
        <Route
          path="/framing/uncertainties"
          element={
            <ErrorBoundary>
              <IssueListProvider>
                <FilterListProvider>
                  <Uncertainties />
                </FilterListProvider>
              </IssueListProvider>
            </ErrorBoundary>
          }
        />
        <Route
          path="/framing/synthesis"
          element={
            <ErrorBoundary>
              <Synthesis />
            </ErrorBoundary>
          }
        />
        <Route
          path="/structuring"
          element={
            <ErrorBoundary>
              <InfluenceDiagram />
            </ErrorBoundary>
          }
        />
        <Route
          path="/structuring/id"
          element={
            <ErrorBoundary>
              <InfluenceDiagram />
            </ErrorBoundary>
          }
        />
        <Route
          path="/structuring/dt"
          element={
            <ErrorBoundary>
              <DecisionTree />
            </ErrorBoundary>
          }
        />
        <Route
          path="/analysis"
          element={
            <ErrorBoundary>
              <Analysis />
            </ErrorBoundary>
          }
        />
        <Route path="/error/:code" element={<ErrorPage />}></Route>
        <Route path="*" element={<ErrorPage />}></Route>
      </Routes>
    </Router>
  );
}

export default App;
