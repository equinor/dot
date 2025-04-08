import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

afterEach(() => {
  cleanup();
});
globalThis.window.injectEnv = {
  CLIENT_APP_ID: 'b44b7866-c7b3-40d2-b3aa-aa0398cb99de',
  CLIENT_APP_SCOPE: "api://4251833c-b9c3-4013-afda-cbfd2cc50f3f/Read",
  REACT_APP_API_BASE_URL: 'http://localhost:8000',
  REDIRECT_URL: 'http://localhost:3000',
}