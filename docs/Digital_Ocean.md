## Steps for deploying the project in Digital Ocean Platform
   
   ## Prerequisites
   - An email address to register for a free GitHub account.
   - A credit card or Paypal account for signing up with DigitalOcean’s cloud service. You will not
     be charged for your first three sites

1. Create a GitHub Account
2. Download and Install the GitHub Desktop App
3. Create a GitHub Repository for your Website Project
4. Copy Website Files to GitHub Repository
   -  Open your website project’s working folder, or the folder that is currently storing all of your
      website project’s files and folders
   - Find and open the newly created repository folder that you named    
   - Copy the files from your working folder to your repository folder
   - Paste copies of your files into the repository folder
   - After pasting the files into your repository folder, the GitHub Desktop app should display the
     files in the “Changes” panel on the left side of the app window
   - Once your folders are in your local repository folder, you are ready to save your changes to the
     repository  
   - Click the blue button <Commit to master> located below the text fields 
   - Once you have committed your changes to the main branch, your files in the left hand panel will
     disappear as this panel only displays files that contain uncommitted changes 

5. Pushing Committed Files to GitHub
   - Add your website files to your GitHub repository
   - To publish your local repository to your GitHub repository, click on the blue ```Publish repository``` button   
   - Once you click the button, a modal will appear asking you to fill out the name and description
     of your repository
   - After filling out your details, click the blue ```Publish repository``` button  
   - Once your files finish uploading, your repository should be available on your account on GitHub
       ```https://github.com/your_github_account_name/your_repository_name```

6. Create Your DigitalOcean Account
   -  visit the sign up page and 
      - Entering an email address and password
      - Using Google Single Sign On
      - Using GitHub Single Sign On 

7. Deploy Your Website with DigitalOcean App Platform
  - Visit the DigitalOcean App Platform portal and click on the blue ```Launch Your App```button 
  - On the next page, you will be prompted to select your GitHub repository
  - Since you have not yet connected your App Platform account to your GitHub account, you’ll need to
    click on the ```Link Your GitHub Account```button      
  - You will then be prompted to sign into your GitHub account (if you aren’t already signed in) and
    select the account that you want to connect to App Platform   
  - Once selected, you will be directed to a page where you can select which repositories to permit
    App Platform to access  
  - Click the ```Only select repositories``` button and select the repository that you pushed to your
    GitHub account 
  - When you are done, click the ```Save```button at the bottom of the webpage     
  - You will now be directed back to App Platform, where you should now be able to select your
    repository in the dropdown menu    
  - After selecting your repository, click ```Next``` You will then be prompted to choose the name,
    branch, and options for Autodeploy 
  - Next, you will be taken to a page where you can configure your App. This page should
    automatically detect your component type as a ```Static Site```   
  - Scroll down and click the blue button “Next” at the bottom of the page
  - You will be directed to a new window where you can select the ```Starter``` plan if you’d like to
    deploy this site as one of your free three static sites  
  - Select your desired plan and click the ```Launch Your Starter App``` button 
  - When your app is finished deploying, you will see the ```Deployed Successfully``` 
  
  
  
  