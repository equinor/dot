import React from "react";
import { ProjectContext, ProjectProvider } from "../../src/components/context";
import { vi } from "vitest";

const mockContextValue = [
  { id: "123", name: "Mock Project" }, // Mock project data
  vi.fn(), // Mock function
];

const MockProjectProvider = ({ children }) => {
  return <ProjectProvider value={mockContextValue}>{children}</ProjectProvider>;
};

export { MockProjectProvider };
