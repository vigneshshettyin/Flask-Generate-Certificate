import { Fragment, useEffect, useState } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import logo from './logo.svg';
import './App.css';
import { Home } from "./pages/Home/index";
import { useSelector } from "react-redux";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        
        <Route
          exact={true}
          path="/"
          render={() => <Home theme={theme} />}
        />
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Flask Generate Certificate
        </a>
      </header>
    </div>
  );
}

export default App;
