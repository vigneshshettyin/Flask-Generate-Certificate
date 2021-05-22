import { Link } from "react-router-dom";
import style from "./motive.module.scss";

export const Motive = (props) => {
  let dark = props.theme;

  return (
    <div
      className={
        dark
          ? `${style["motive-div"]} ${style["dark"]}`
          : `${style["motive-div"]} ${style["light"]}`
      }
    >
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-lg-8">
            <div className="section-title text-center pb-20">
              <div
                className={
                  dark
                    ? `${style["motive"]} ${style["motive-dark"]}`
                    : `${style["motive"]} ${style["motive-light"]}`
                }
              >
                <h1>
                  <i className="fas fa-crosshairs"></i>ur Motive
                </h1>
                <div
                  className={
                    dark
                      ? `${style["dash"]} ${style["dash-dark"]}`
                      : `${style["dash"]} ${style["dash-light"]}`
                  }
                ></div>
              </div>
              <p className="text text-white my-3">
              This Certificate Generation and Verification System project aims in developing
              a computerized system to maintain and generate the certificate. 
              </p>
            </div>
          </div>
        </div>
        <div className="row justify-content-center">
          <div className="col-lg-4 col-md-6 col-sm-8 my-3">
            <div
              className={
                dark
                  ? `${style["single-features"]} ${style["single-features-dark"]} d-flex mt-30 wow fadeIn`
                  : `${style["single-features"]} ${style["single-features-light"]} d-flex mt-30 wow fadeIn`
              }
              data-wow-duration="1s"
              data-wow-delay="0s"
            >
              <div className={style["features-icon"]}>
                <i className="fas fa-bullhorn"></i>
              </div>
              <div className={`${style["features-content"]} text-left`}>
                <h4 className={style["features-title"]}>
                </h4>
                <p className={style["motive-content"]}>
                It has an admin login through which the admin can monitor the whole system.
                It also has a facility where users after logging in to their account can 
                monitor and generate a certificate for their particular use.
                </p>
              </div>
            </div>
          </div>
          <div className="col-lg-4 col-md-6 col-sm-8 my-3">
            <div
              className={
                dark
                  ? `${style["single-features"]} ${style["single-features-dark"]} d-flex mt-30 wow fadeIn`
                  : `${style["single-features"]} ${style["single-features-light"]} d-flex mt-30 wow fadeIn`
              }
              data-wow-duration="1s"
              data-wow-delay="0.5s"
            >
              <div className={style["features-icon"]}>
                <i className="fa fa-users"></i>
              </div>
              <div className={`${style["features-content"]} text-left`}>
                <h4 className={style["features-title"]}>
                
                </h4>
                <p className={style["motive-content"]}>
                Admin will manage user logins, will have the option to deactivate any user. 
                </p>
              </div>
            </div>
          </div>
          <div className="col-lg-4 col-md-6 col-sm-8 my-3">
            <div
              className={
                dark
                  ? `${style["single-features"]} ${style["single-features-dark"]} d-flex mt-30 wow fadeIn`
                  : `${style["single-features"]} ${style["single-features-light"]} d-flex mt-30 wow fadeIn`
              }
              data-wow-duration="1s"
              data-wow-delay="1s"
            >
              <div className={style["features-icon"]}>
                <i className="fas fa-user-graduate"></i>
              </div>
              <div className={`${style["features-content"]} text-left`}>
                <h4 className={style["features-title"]}>
                </h4>
                <p className={style["motive-content"]}>
                Every time any changes are done an automated email will
                be sent depending on the update. 
                </p>
              </div>
            </div>
          </div>
          <p className="text text-white my-3 text-center">
          Overall this project is being developed to help the users
          in the best way possible and also to reduce human efforts.

          </p>
        </div>
      </div>
    </div>
  );
};
