import { PublicClientApplication } from "@azure/msal-browser";
import { useMsal } from '@azure/msal-react';

const msalConfig = {
  auth: {
    clientId: "637a2493-5510-40c3-86a6-9db8f3192966",
    authority:
      "https://login.microsoftonline.com/3aa4a235-b6e2-48d5-9195-7fcf05b459b0", // This is a URL (e.g. https://login.microsoftonline.com/{your tenant ID})
    redirectUri: "http://localhost:3000/",
  },
  cache: {
    cacheLocation: "localStorage", // This configures where your cache will be stored
    storeAuthStateInCookie: false, // Set this to "true" if you are having issues on IE11 or Edge
  },
};

export const msalInstance = new PublicClientApplication(msalConfig);


export const getAccessToken = async () => {
  const loginRequest = {
    scopes: ["api://4251833c-b9c3-4013-afda-cbfd2cc50f3f/Read"],
  };
  const accounts = msalInstance.getAllAccounts();
  if (accounts.length === 0) {
    return null;
  }
  const request = {
    ...loginRequest,
    account: accounts[0],
  };    
  const tokenResponse = await msalInstance.acquireTokenSilent(request);
  return  tokenResponse.accessToken;
}