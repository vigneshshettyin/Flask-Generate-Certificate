 ## Steps for deploying the project on Azure App Services

1. Prepare your repository:-
   - To get automated builds from Azure App Service build server, make sure that your repository root
     has the correct files in your project.
   - To customize your deployment, include a ```.deployment file``` in the repository root.  

2. Configure deployment source:-
   - In the Azure portal, navigate to the management page for your App Service app
   - From the left menu, click ```Deployment Center > Settings```
   - In ```Source```, select one of the CI/CD options
   - GitHub Actions is the default build provider. To change it, click ```Change provider > App   Service Build Service (Kudu) > OK```
   - If you're deploying from GitHub for the first time, click ```Authorize``` and follow the
     authorization prompts. If you want to deploy from a different user's repository, click ```Change Account```
   - Once you authorize your Azure account with GitHub, select the <Organization, Repository, and Branch> to configure CI/CD for
   - When GitHub Actions is the chosen build provider, you can select the ```workflow file``` you
     want with the Runtime stack and Version dropdowns. Azure commits this workflow file into your selected GitHub repository to handle build and deploy tasks
   - To see the file before saving your changes, click ```Preview file```
   - Click Save
     - New commits in the selected repository and branch now deploy continuously into your App
       Service app which can track the commits and deployments in the <Logs tab>

3. Disable continuous deployment
   - In the Azure portal, navigate to the <management page> for your App Service app
   - From the left menu, click ```Deployment Center > Settings > Disconnect``` 
   - By default, the GitHub Actions workflow file is preserved in your repository, but it will
    continue to trigger deployment to your app. To delete it from your repository, select 
     ```Delete workflow file```   
     
     