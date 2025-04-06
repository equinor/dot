import { PublicClientApplication } from "@azure/msal-browser";
import { useMsal } from '@azure/msal-react';

const msalConfig = {
  auth: {
    clientId: process.env.CLIENT_APP_ID,
    authority:
      "https://login.microsoftonline.com/3aa4a235-b6e2-48d5-9195-7fcf05b459b0", // This is a URL (e.g. https://login.microsoftonline.com/{your tenant ID})
    redirectUri: process.env.REDIRECT_URL,
  },
  cache: {
    cacheLocation: "localStorage", // This configures where your cache will be stored
    storeAuthStateInCookie: false, // Set this to "true" if you are having issues on IE11 or Edge
  },
};

export const msalInstance = new PublicClientApplication(msalConfig);


export const getAccessToken = async () => {
  const loginRequest = {
    scopes: [process.env.CLIENT_APP_SCOPE],
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