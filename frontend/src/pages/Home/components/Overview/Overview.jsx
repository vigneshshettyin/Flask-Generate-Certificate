import React from "react";
import styles from "./overview.module.scss";

export const Overview = (props) => {
  let dark = props.theme;

  return (
    <div className="content container">
      <div className="row justify-content-center">
        <div className="col-12">
          <div
            className={
              dark
                ? `${styles["overview"]} ${styles["overview-dark"]}`
                : `${styles["overview"]} ${styles["overview-light"]}`
            }
          >
            <div>
              <h1>Certificate Generation and Verification System </h1>
              <div
                className={
                  dark
                    ? `${styles["dash"]} ${styles["dash-dark"]}`
                    : `${styles["dash"]} ${styles["dash-light"]}`
                }
              ></div>
              <p>
              Certificate Generation and Verification System project aims in 
              developing a computerized system to maintain and generate the
              certificate. It has an admin login through which the admin can
              monitor the whole system. 
              </p>
            </div>
            <img
              src="./src/logo.svg"
              alt="Flask Generate Certificate Official Logo"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
