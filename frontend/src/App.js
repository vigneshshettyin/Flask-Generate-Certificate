import { Fragment, useEffect, useState } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import logo from './logo.svg';
import './App.css';
import { Home } from "./pages/Home/index";
import { useSelector } from "react-redux";

function App() {
  const isSuperAdmin = useSelector((state) => state.isSuperAdmin);

  function getTheme() {
    return JSON.parse(localStorage.getItem("dark")) || false;
  }
  const [theme, setTheme] = useState(getTheme());

  function toggleTheme() {
    setTheme((prevTheme) => !prevTheme);
    setToast(true);

    setTimeout(() => {
      setToast(false);
    }, 3000);

    localStorage.setItem("dark", !theme);
  }

  useEffect(() => {
    console.log("Theme changed");
  }, [theme, toast]);

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
