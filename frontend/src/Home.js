import React, { Component } from "react";
 
class Home extends Component {
  render() {
    return (
      <div>
        <h2>FLASK-GENERATE-CERTIFICATE WEBSITE</h2>
        <p>Certificate Generation and Verification System project aims
        in developing a computerized system to maintain and generate
        the certificate. It has an admin login through which the
        admin can monitor the whole system. It also has a facility
        where users after logging in to their account can monitor
        and generate a certificate for their particular use.</p>
 
        <p>Admin will manage user logins, will have the option to
        deactivate any user. Every time any changes are done an
        automated email will be sent depending on the update.
        Overall this project is being developed to help the
        users in the best way possible and also to reduce human efforts.
        </p>
      </div>
    );
  }
}
 
export default Home;
