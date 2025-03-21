import React from "react";
import { Navigate } from "react-router-dom";

class NetworkError extends Error {
  constructor(message) {
    super(message);
    this.name = "NetworkError";
  }
}

class AuthorizationError extends Error {
  constructor(message) {
    super(message);
    this.name = "AuthorizationError";
  }
}
class ErrorBoundary extends React.Component {
  state = { error: null, code: null };

  componentDidCatch(error, errorInfo) {
    if (error instanceof NetworkError) {
      this.setState({ error, code: 503 });
    } else if (error instanceof AuthorizationError) {
      this.setState({ error, code: 401 });
    } else {
      this.setState({ error, code: 500 });
    }
  }

  render() {
    if (this.state.error) {
      // render the ErrorPage component with the error details
      return <Navigate to={`/error/${this.state.code}`} />;
    } else {
      // render the child components
      return this.props.children;
    }
  }
}
export default ErrorBoundary;
