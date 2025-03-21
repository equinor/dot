import React from "react";
import "../styles/error.css";
import { useNavigate, useParams } from "react-router-dom";
import { Button } from "@equinor/eds-core-react";
import beaver from "../components/beaver.png";

function ErrorPage() {
  //TODO: the button to go back one step should also rerender the page?
  const navigate = useNavigate();
  const { code } = useParams();
  return (
    <div className="errorPage">
      <div className="errorMessage">
        <img
          src={beaver}
          alt="Beaver"
          className="beaverImage"
          style={{ width: "60%" }}
        />
        <h3 className="errorHeading">Damn!</h3>
        <p className="errorContext">Something happened to your tree!</p>
        <p className="errorContextDetail">Error {code}</p>
        <p className="errorContextDetail">Page not implemented!</p>
        <Button
          className="backButton"
          onClick={() => {
            navigate(-2);
          }}
        >
          Go back
        </Button>
      </div>
    </div>
  );
}

export default ErrorPage;
