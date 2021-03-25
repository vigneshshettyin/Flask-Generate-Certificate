# Getting started using Elastic Beanstalk<a name="GettingStarted"></a>

To help you understand how AWS Elastic Beanstalk works, this tutorial walks you through creating, exploring, updating, and deleting an Elastic Beanstalk application\. It takes less than an hour to complete\. 

There is no cost for using Elastic Beanstalk, but the AWS resources that it creates for this tutorial are live \(and don't run in a sandbox\)\. You incur the standard usage fees for these resources until you terminate them at the end of this tutorial\. The total charges are typically less than a dollar\. For information about how to minimize charges, see [AWS free tier](https://aws.amazon.com/free)\. 

## Setting up: Create an AWS account<a name="GettingStarted.Setup"></a>

If you're not already an AWS customer, you need to create an AWS account\. Signing up enables you to access Elastic Beanstalk and other AWS services that you need\.

**To sign up for an AWS account**

1. Open the [Elastic Beanstalk console](https://console.aws.amazon.com/elasticbeanstalk), and in the **Regions** list, select your AWS Region\.

1. Follow the instructions shown\.

# Step 1: Create an example application<a name="GettingStarted.CreateApp"></a>

In this step, you create a new application starting from a preexisting example application\. Elastic Beanstalk supports platforms for different programming languages, application servers, and Docker containers\. You choose a platform when you create the application\.

## Create an application and an environment<a name="GettingStarted.CreateApp.Create"></a>

To create your example application, you'll use the **Create a web app** console wizard\. It creates an Elastic Beanstalk application and launches an environment within it\. An environment is the collection of AWS resources required to run your application code\.

**To create an example application**

1. Open the Elastic Beanstalk console using this link: [https://console.aws.amazon.com/elasticbeanstalk/home#/gettingStarted?applicationName=getting-started-app](https://console.aws.amazon.com/elasticbeanstalk/home#/gettingStarted?applicationName=getting-started-app)

1. Optionally add [application tags](applications-tagging.md)\.

1. For **Platform**, choose a platform, and then choose **Create application**\.

To run the example application on AWS resources, Elastic Beanstalk takes the following actions\. They take about five minutes to complete\.

1. Creates an Elastic Beanstalk application named **getting\-started\-app**\.

1. Launches an environment named **GettingStartedApp\-env** with these AWS resources:
   + An Amazon Elastic Compute Cloud \(Amazon EC2\) instance \(virtual machine\)
   + An Amazon EC2 security group
   + An Amazon Simple Storage Service \(Amazon S3\) bucket 
   + Amazon CloudWatch alarms 
   + An AWS CloudFormation stack 
   + A domain name

   For details about these AWS resources, see [AWS resources created for the example application](#GettingStarted.CreateApp.AWSresources)\.

1. Creates a new application version named **Sample Application**\. This is the default Elastic Beanstalk example application file\.

1. Deploys the code for the example application to the **GettingStartedApp\-env** environment\.

During the environment creation process, the console tracks progress and displays events\.

![\[Elastic Beanstalk console showing the events that occur when it creates an environment\]](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/images/gettingstarted-events.png)

When all of the resources are launched and the EC2 instances running the application pass health checks, the environment's health changes to `Ok`\. You can now use your web application's website\.

## AWS resources created for the example application<a name="GettingStarted.CreateApp.AWSresources"></a>

When you create the example application, Elastic Beanstalk creates the following AWS resources:
+ **EC2 instance** – An Amazon EC2 virtual machine configured to run web apps on the platform you choose\.

  Each platform runs a different set of software, configuration files, and scripts to support a specific language version, framework, web container, or combination thereof\. Most platforms use either Apache or nginx as a reverse proxy that processes web traffic in front of your web app, forwards requests to it, serves static assets, and generates access and error logs\.
+ **Instance security group** – An Amazon EC2 security group configured to allow incoming traffic on port 80\. This resource lets HTTP traffic from the load balancer reach the EC2 instance running your web app\. By default, traffic is not allowed on other ports\.
+ **Amazon S3 bucket** – A storage location for your source code, logs, and other artifacts that are created when you use Elastic Beanstalk\.
+ **Amazon CloudWatch alarms** – Two CloudWatch alarms that monitor the load on the instances in your environment and are triggered if the load is too high or too low\. When an alarm is triggered, your Auto Scaling group scales up or down in response\.
+ **AWS CloudFormation stack** – Elastic Beanstalk uses AWS CloudFormation to launch the resources in your environment and propagate configuration changes\. The resources are defined in a template that you can view in the [AWS CloudFormation console](https://console.aws.amazon.com/cloudformation)\.
+ **Domain name** – A domain name that routes to your web app in the form **subdomain*\.*region*\.elasticbeanstalk\.com*\.

# Step 2: Explore your environment<a name="GettingStarted.Explore"></a>

To see an overview of your Elastic Beanstalk application's environment, use the environment page in the Elastic Beanstalk console\.

**To view the environment overview**

1. Open the [Elastic Beanstalk console](https://console.aws.amazon.com/elasticbeanstalk), and in the **Regions** list, select your AWS Region\.

1. In the navigation pane, choose **Environments**, and then choose the name of your environment from the list\.
**Note**  
If you have many environments, use the search bar to filter the environment list\.

The environment overview pane shows top level information about your environment\. This includes its name, its URL, its current health status, the name of the currently deployed application version, and the platform version that the application is running on\. Below the overview pane you can see the five most recent environment events\.

To learn more about environment tiers, platforms, application versions, and other Elastic Beanstalk concepts, see [Elastic Beanstalk concepts](concepts.md)\.

![\[Environment overview.\]](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/images/gettingstarted-dashboard.png)

While Elastic Beanstalk creates your AWS resources and launches your application, the environment is in a `Pending` state\. Status messages about launch events are continuously added to the overview\.

The environment's **URL** is located at the top of the overview, below the environment name\. This is the URL of the web application that the environment is running\. Choose this URL to get to the example application's *Congratulations* page\.

The navigation page on the left side of the console links to other pages that contain more detailed information about your environment and provide access to additional features:
+ **Configuration** – Shows the resources provisioned for this environment, such as the Amazon Elastic Compute Cloud \(Amazon EC2\) instances that host your application\. You can configure some of the provisioned resources on this page\.
+ **Health** – Shows the status of and detailed health information about the Amazon EC2 instances running your application\.
+ **Monitoring** – Shows statistics for the environment, such as average latency and CPU utilization\. You can use this page to create alarms for the metrics that you are monitoring\.
+ **Events** – Shows information or error messages from the Elastic Beanstalk service and from other services whose resources this environment uses\.
+ **Tags** – Shows environment tags and allows you to manage them\. Tags are key\-value pairs that are applied to your environment\.

# Step 3: Deploy a new version of your application<a name="GettingStarted.DeployApp"></a>

Periodically, you might need to deploy a new version of your application\. You can deploy a new version at any time, as long as no other update operations are in progress on your environment\.

The application version that you started this tutorial with is called **Sample Application**\.

**To update your application version**

1. Download the sample application that matches your environment's platform\. Use one of the following applications\.
   + **Docker** – [docker\-singlecontainer\-v1\.zip](samples/docker-singlecontainer-v1.zip)
   + **Multicontainer Docker** – [docker\-multicontainer\-v2\.zip](samples/docker-multicontainer-v2.zip)
   + **Preconfigured Docker \(Glassfish\)** – [docker\-glassfish\-v1\.zip](samples/docker-glassfish-v1.zip)
   + **Go** – [go\-v1\.zip](samples/go-v1.zip)
   + **Java SE** – [java\-se\-jetty\-gradle\-v3\.zip](samples/java-se-jetty-gradle-v3.zip)
   + **Tomcat \(default\)** – [java\-tomcat\-v3\.zip](samples/java-tomcat-v3.zip)
   + **Tomcat 7** – [java7\-tomcat7\.zip](samples/java7-tomcat7.zip)
   + **\.NET Core on Linux** – [dotnet\-core\-linux\-v1\.zip](samples/dotnet-core-linux-v1.zip)
   + **\.NET** – [dotnet\-asp\-v1\.zip](samples/dotnet-asp-v1.zip)
   + **Node\.js** – [nodejs\-v1\.zip](samples/nodejs-v1.zip) 
   + **PHP** – [php\-v1\.zip](samples/php-v1.zip)
   + **Python** – [python\-v1\.zip](samples/python-v1.zip)
   + **Ruby \(Passenger Standalone\)** – [ruby\-passenger\-v3\.zip](samples/ruby-passenger-v3.zip)
   + **Ruby \(Puma\)** – [ruby\-puma\-v3\.zip](samples/ruby-puma-v3.zip)

1. Open the [Elastic Beanstalk console](https://console.aws.amazon.com/elasticbeanstalk), and in the **Regions** list, select your AWS Region\.

1. In the navigation pane, choose **Environments**, and then choose the name of your environment from the list\.
**Note**  
If you have many environments, use the search bar to filter the environment list\.

1. On the environment overview page, choose **Upload and deploy**\.

1. Choose **Choose file**, and then upload the sample application source bundle that you downloaded\.  
![\[Upload and deploy dialog.\]](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/images/aeb-app-version-upload.png)

   The console automatically fills in the **Version label** with a new unique label\. If you type in your own version label, ensure that it's unique\.

1. Choose **Deploy**\.

 While Elastic Beanstalk deploys your file to your Amazon EC2 instances, you can view the deployment status on the environment's overview\. While the application version is updated, the **Environment Health** status is gray\. When the deployment is complete, Elastic Beanstalk performs an application health check\. When the application responds to the health check, it's considered healthy and the status returns to green\. The environment overview shows the new **Running Version**—the name you provided as the **Version label**\.

Elastic Beanstalk also uploads your new application version and adds it to the table of application versions\. To view the table, choose **Application versions** under **getting\-started\-app** on the navigation pane\.

# Step 4: Configure your environment<a name="GettingStarted.EditConfig"></a>

You can configure your environment to better suit your application\. For example, if you have a compute\-intensive application, you can change the type of Amazon Elastic Compute Cloud \(Amazon EC2\) instance that is running your application\. To apply configuration changes, Elastic Beanstalk performs an environment update\.

Some configuration changes are simple and happen quickly\. Some changes require deleting and recreating AWS resources, which can take several minutes\. When you change configuration settings, Elastic Beanstalk warns you about potential application downtime\. 

## Make a configuration change<a name="GettingStarted.EditConfig.Edit"></a>

In this example of a configuration change, you edit your environment's capacity settings\. You configure a load balanced, automatically scaling environment that has between two and four Amazon EC2 instances in its Auto Scaling group, and then you verify that the change occurred\. Elastic Beanstalk creates an additional Amazon EC2 instance, adding to the single instance that it created initially\. Then, Elastic Beanstalk associates both instances with the environment's load balancer\. As a result, your application's responsiveness is improved and its availability is increased\.

**To change your environment's capacity**

1. Open the [Elastic Beanstalk console](https://console.aws.amazon.com/elasticbeanstalk), and in the **Regions** list, select your AWS Region\.

1. In the navigation pane, choose **Environments**, and then choose the name of your environment from the list\.
**Note**  
If you have many environments, use the search bar to filter the environment list\.

1. In the navigation pane, choose **Configuration**\.

1. In the **Capacity** configuration category, choose **Edit**\.

1. In the **Auto Scaling group** section, change **Environment type** to **Load balanced**\.

1. In the **Instances** row, change **Max** to **4**, and then change **Min** to **2**\.

1. Choose **Apply**\.

1. A warning tells you that this update replaces all of your current instances\. Choose **Confirm**\.

1. In the navigation pane, choose **Events**\.

   The environment update can take a few minutes\. To find out that it's complete, look for the event **Successfully deployed new configuration to environment** in the event list\. This confirms that the Auto Scaling minimum instance count has been set to 2\. Elastic Beanstalk automatically launches the second instance\. 

## Verify the configuration change<a name="GettingStarted.EditConfig.Verify"></a>

When the environment update is complete and the environment is ready, verify your change\.

**To verify the increased capacity**

1. In the navigation pane, choose **Health**\.

1. Look at the **Enhanced health overview** page\.

   You can see that two Amazon EC2 instances are listed following the **Overall** line\. Your environment capacity has increased to two instances\.  
![\[Enhanced health overview page on the Elastic Beanstalk console showing two Amazon EC2 instances\]](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/images/gettingstarted-health.png)


# Step 5: Clean up<a name="GettingStarted.Cleanup"></a>

Congratulations\! You have successfully deployed a sample application to the AWS Cloud, uploaded a new version, and modified its configuration to add a second Auto Scaling instance\. To ensure that you're not charged for any services you aren't using, delete all application versions and terminate the environment\. This also deletes the AWS resources that the environment created for you\.

**To delete the application and all associated resources**

1. Delete all application versions\.

   1. Open the [Elastic Beanstalk console](https://console.aws.amazon.com/elasticbeanstalk), and in the **Regions** list, select your AWS Region\.

   1. In the navigation pane, choose **Applications**, and then choose **getting\-started\-app**\.

   1. In the navigation pane, find your application's name and choose **Application versions**\.

   1. On the **Application versions** page, select all application versions that you want to delete\.

   1. Choose **Actions**, and then choose **Delete**\.

   1. Turn on **Delete versions from Amazon S3**\.

   1. Choose **Delete**, and then choose **Done**\.

1. Terminate the environment\.

   1. In the navigation pane, choose **getting\-started\-app**, and then choose **GettingStartedApp\-env** in the environment list\.

   1. Choose **Environment actions**, and then choose **Terminate Environment**\.

   1. Confirm that you want to terminate **GettingStartedApp\-env** by typing the environment name, and then choose **Terminate**\.

1. Delete the getting\-started\-app application\.

   1. In the navigation pane, choose the **getting\-started\-app**\.

   1. Choose **Actions**, and then choose **Delete application**\.

   1. Confirm that you want to delete **getting\-started\-app** by typing the application name, and then choose **Delete**\.