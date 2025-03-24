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

msalInstance.initialize().then(() => {
  root.render(
    <React.StrictMode>
      <MsalProvider instance={msalInstance}>
        <MsalAuthenticationTemplate interactionType={InteractionType.Redirect}>
          <ProjectProvider>
            <App />
          </ProjectProvider>
        </MsalAuthenticationTemplate>
      </MsalProvider>
    </React.StrictMode>
  );
});

// If you want to start measuring performance in your
// app, pass a function to log results (for example:
// reportWebVitals(console.log)) or send to an analytics
// endpoint.Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
