import React from "react";
import { act, render, screen } from "@testing-library/react";
import { describe, expect, test, vi, beforeEach, afterEach } from "vitest";
import App from "../src/App";
import { MockProjectProvider } from "./__mocks__/mockProjectContext";
import { allProjects } from "../src/services/project_api";

vi.mock("../src/services/project_api", () => ({
  allProjects: vi.fn(() => Promise.resolve([])),
}));

afterEach(() => {
  vi.clearAllMocks(); // Clear all mocks after each test
});
describe("App tests", () => {
  beforeEach(() => {
    allProjects.mockResolvedValue([]);
  });
  test("shows home page", async () => {
    await act(async () => {
      render(
        <MockProjectProvider>
          <App />
        </MockProjectProvider>
      );
    });
    const linkElements = screen.getAllByText(/Decision Optimization Tool/i);
    expect(linkElements.length).toBeGreaterThan(0);
    linkElements.forEach((element) => {
      expect(element).toBeInTheDocument();
    });
  });
});
