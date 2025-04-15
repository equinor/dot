import React from "react";
import ReactDOM from "react-dom/client";
import "./styles/index.css";
import "./styles/equinor-font.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { ProjectProvider } from "./components/context";
import { msalInstance } from "./auth";
import { MsalProvider } from "@azure/msal-react";
import { InteractionType } from "@azure/msal-browser";
import { MsalAuthenticationTemplate } from "@azure/msal-react";

const root = ReactDOM.createRoot(document.getElementById("root"));
const isLocalEnvironment =
  window.injectEnv.NODE_ENV === "local" || process.env.NODE_ENV === "local";
console.log(isLocalEnvironment);

if (!isLocalEnvironment) {
  msalInstance.initialize().then(() => {
    root.render(
      <React.StrictMode>
        <MsalProvider instance={msalInstance}>
          <MsalAuthenticationTemplate
            interactionType={InteractionType.Redirect}
          >
            <ProjectProvider>
              <App />
            </ProjectProvider>
          </MsalAuthenticationTemplate>
        </MsalProvider>
      </React.StrictMode>
    );
  });
} else {
  // Render the app directly without MSAL if in local environment
  root.render(
    <React.StrictMode>
      <ProjectProvider>
        <App />
      </ProjectProvider>
    </React.StrictMode>
  );
}

reportWebVitals();
