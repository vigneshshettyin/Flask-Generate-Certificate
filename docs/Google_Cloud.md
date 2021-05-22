## Steps for deploying the project on Google Cloud PLatform

1. Creating a Google Cloud Platform project

   - To use Google's tools for your own site or app, you need to create a new project on Google Cloud
     Platform. This requires having a Google account.
      - Go to the App Engine dashboard on the Google Cloud Platform Console and press the Create 
        button.
      - If you've not created a project before, you'll need to select whether you want to receive 
        email updates or not, agree to the Terms of Service, and then you should be able to continue.
      - Enter a name for the project, edit your project ID and note it down. For example-
        Project Name: ```GAE Sample Site```
        Project ID: ```gaesamplesite```
      - Click the Create button to create your project.

2. Creating an application    

   - We'll need a sample application to publish. If you've not got one to use, download and unzip 
     this sample app.
   - Have a look at the sample application's structure — the website folder contains your website
     content and <app.yaml> is your application configuration file.
       - Your website content must go inside the website folder, and its landing page must be called 
         <index.html>, but apart from that it can take whatever form you like.
       - The <app.yaml> file is a configuration file that tells App Engine how to map URLs to 
         your static files. You don't need to edit it.

3. Publishing your application

   - Open Google Cloud Shell.
   - Drag and drop the <sample-app> folder into the left pane of the code editor.
   - Run the following in the command line to select your project:-
      ```gcloud config set project gaesamplesite```
   - Then run the following command to go to your app's directory:-
      ```cd sample-app```
   - You are now ready to deploy your application, i.e. upload your app to App Engine:-
      ```gcloud app deploy```
   - Enter a number to choose the region where you want your application located.
   - Enter Y to confirm.
   - Now navigate your browser to your-project-id.appspot.com to see your website online. For 
     example, for the project ID ```gaesamplesite```, go to ```gaesamplesite.appspot.com```
      
