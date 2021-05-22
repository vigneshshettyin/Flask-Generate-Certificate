import React from "react";
import { Overview } from "./components/Overview/index";
import { Motive } from "./components/Motive/index";

import styles from "./home.module.scss";

export const Home = (props) => {
  let dark = props.theme;
  console.log("Theme changed in the home page", dark);

  return (
    <div
      className={
        dark ? `${styles["home"]} ${styles["dark"]}` : `${styles["home"]}`
      }
    >
      <Overview theme={dark} />
      <Motive theme={dark} />
    </div>
  );
};
