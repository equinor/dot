// home.test.jsx
import React from "react";
import { act, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, test, vi, afterEach, beforeEach } from "vitest";
import Home from "../../src/pages/home";
import { MockProjectProvider } from "../__mocks__/mockProjectContext";
import { BrowserRouter as Router } from "react-router-dom";
import { allProjects } from "../../src/services/project_api";

const projects_mock = [
  {
    tag: ["000000000000000000001"],
    name: "The Used Car Buyer Problem",
    shortname: "Project shortname",
    description: "Literature Problem",
    index: "0",
    decision_maker: null,
    decision_date: null,
    uuid: "64d5594d-3e1e-4473-b393-7e0e4ec18420",
    timestamp: "1712647888.1065063",
    date: "2024-04-09 07:31:28.106508",
    ids: "test",
    id: "64d5594d-3e1e-4473-b393-7e0e4ec18420",
    sensitivity_label: "Open",
    label: "project",
  },
  {
    tag: ["subsurface"],
    name: "the little project example",
    shortname: "cute project",
    description: "This is a project example",
    category: "Uncertainty",
    index: "0",
    decision_maker: null,
    decision_date: null,
    uuid: "49712919-cb6a-49a3-948a-d9e82aa9a5de",
    timestamp: "1709319663.9792306",
    date: "2024-03-01 19:01:03.979234",
    ids: "test",
    sensitivity_label: "Restricted",
    id: "49712919-cb6a-49a3-948a-d9e82aa9a5de",
    label: "project",
  },
];

vi.mock("../../src/services/project_api", () => ({
  allProjects: vi.fn(() => Promise.resolve(projects_mock)),
}));

vi.mock("../../src/components/importDialog", () => ({
  __esModule: true,
  default: vi.fn(() => null),
}));
vi.mock("../../src/components/deleteCheck", () => ({
  __esModule: true,
  default: vi.fn(() => null),
}));

afterEach(() => {
  vi.clearAllMocks(); // Clear all mocks after each test
});

describe("Home page", () => {
  beforeEach(() => {
    //allProjects.mockResolvedValue(projects_mock);
  });

  test("render home component without projects", async () => {
    allProjects.mockResolvedValue([]);
    await act(async () => {
      render(
        <Router>
          <MockProjectProvider>
            <Home />
          </MockProjectProvider>
        </Router>
      );
    });
    const linkElements = screen.getAllByText(/Decision Optimization Tool/i);
    expect(linkElements.length).toBeGreaterThan(0);
    linkElements.forEach((element) => {
      expect(element).toBeInTheDocument();
    });

    //New Project Button
    expect(
      screen.getByRole("link", { name: "add action" })
    ).toBeInTheDocument();
  });

  test("renders Home component with two projects", async () => {
    allProjects.mockResolvedValue(projects_mock);
    await act(async () => {
      render(
        <Router>
          <MockProjectProvider>
            <Home />
          </MockProjectProvider>
        </Router>
      );
    });

    await waitFor(() => {
      expect(allProjects).toHaveBeenCalled();
      const usedCarBuyerText = screen.getByText(/The Used Car Buyer Problem/i);
      expect(usedCarBuyerText).toBeInTheDocument();
      expect(
        screen.getByText(/the little project example/i)
      ).toBeInTheDocument();
    });
  });
});
