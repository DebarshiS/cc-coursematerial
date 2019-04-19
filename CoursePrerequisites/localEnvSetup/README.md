Local Environment Setup for Cloud Curriculum - Java
===================================================
> **Disclaimer (!):**   
> This document does not serve as alternative for the Virtual Machine for exercise execution:  we do not guarantee that this document is up to date and we cannot provide any support in case of problems with your local development environment up! 

To be able to install software on your computer, please make sure you have administrative rights.

Several services like a PostgreSQL database are used in the course. You can either install them manually or let the virtual machine provide these services to your machine. The manual steps that are required to use VM as service host are explained [here](/CoursePrerequisites/localEnvSetup/VM_use_as_service_host.md).

## Proxy Settings
- Windows: Download and run [proxyEnv.cmd](/CoursePrerequisites/localEnvSetup/proxyEnv.cmd) to permanently set the proxy settings in your environment.
- MacOSX: Add the lines inside [proxyEnv.bash_profile](/CoursePrerequisites/localEnvSetup/proxyEnv.bash_profile) to your .bash_profile to permanently set the proxy settings in your environment. After setting this, you need to re-login (or reboot).

## Eclipse IDE
In the course, we will develop Java software using Eclipse.
Please make sure you have the following software installed on your computer:

- Java 8 JDK
  - [Download JDK 8](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html) and install it
  - Windows:
    - Run the console `cmd` and enter `setx JAVA_HOME "C:\Program Files\Java\jdk1.8.X"` (replace the path with the path leading to your JDK installation)
    - To test your installation, open a new console and run both `"%JAVA_HOME%\bin\java" -version` and `java -version`. Both should return "java version 1.8.X".
  - MacOSX: nothing to do, env variables should be adjusted automatically. 
- Eclipse Mars (Spring Tool Suite)
  - [Download Eclipse](https://spring.io/tools/eclipse) (select Eclipse Mars - Eclipse IDE for Java EE Developers)
  - Unpack the ZIP file to a suitable location on your computer, e.g. C:/dev/eclipse
- Assign installed Java JRE to Eclipse: `Window` - `Preferences`, type `jre` in filter, in 'Installed JREs', select `Add...`->`Standard VM` and enter the path to your Java 8 version.
- Set proxies within Eclipse: `Window` - `Preferences`, type `network` in filter, in `network connections`, select `manual` and add these entries
  - For http and https: proxy.wdf.sap.corp, port 8080
  - bypass: `*.sap.corp`
- Install the `EclEmma` plugin via the Eclipse Marketplace. This is needed to show code coverage results in Eclipse using Jacoco.
- Install the `DBeaver` plugin via the Eclipse Marketplace. This is needed to manage your database such as PostgreSQL, HANA or H2.
When connecting to a database you are asked to download and install the respective database driver.

## SAP Github Account
- Create a Github account on the SAP internal GitHub if you don't already have one. Use your d-user as ID and an *own password* (not your SAP domain password). For help see: [Getting started with git and GitHub at SAP](https://github.wdf.sap.corp/pages/github/learn.html). (Note: Work on global SAP LDAP integration is in progress, with results expected not before October 2016)
- Then you must set up your SSH keys (if you have not already done this elsewhere). Open eclipse, go to `Window -  Preferences`, then type `ssh` in filter to get to the SSH2 dialog. Then do the following:
  - Make sure `SSH2 directory` is set to `~/.ssh` (where `~` is your your home directory).
  - Go to tab `Key Management` and choose `generate RSA Key...` 
  - Copy the generated public key text in the large text box. Then on GitHub select `Settings` - `Add SSH Keys`. Enter your GitHub password (*not* your SAP domain password) to confirm the new key.
  - Back in Eclipse: In the SSH2 dialog, click on `Save private key ...` and save the key into your `~/.ssh` directory. Click OK to not use a passphrase. Note: The default directory in the dialog may not be `~/.ssh`!
Now you can work with GitHub repositories from the git perspective in Eclipse. 

## Maven
The builds of the individual microservices are managed using Apache Maven.
Please make sure Maven is installed and configured on your computer:
 - [Download](https://maven.apache.org/download.cgi) and [install](https://maven.apache.org/install.html) the latest release (unpack into a local directory).
 - Create the directory `~/.m2/`, where `~` is your home directory, e.g. `C:\Users\D0123456`. (Note: Windows explorer doesn't let you create a directory ".name" - you have to add a dot at the end, i.e. ".name.", which will then be removed. Stupid Windows!)
 - Download the [settings.xml](settings.xml) configuration file and save it in the .m2 directory created in the last step
 
### Maven setup for Windows
 - Run the console `cmd` and enter `setx M2_HOME "C:\apache-maven-XXX"` (replace the path with the path leading to your maven installation)
 - In a new console, run `setx M2 "%M2_HOME%\bin"`
 - In a new console, run `setx PATH "%PATH%;%M2%"`. 
   - *Note on windows PATH length limitation*: Windows has a path length limitation of 1024 bytes! Check the PATH after the setx to make sure the M2 path element did fit at the end. There are also often duplicate entries in the PATH that you can delete if you need the space.
 - Test your installation by running `mvn -version` and `"%M2_HOME%\bin\mvn" -version` in a new console
 
### Maven setup for MacOSX 
 - You can either use homebrew or manually install maven + maintain the environment variables. Both is explained [here](http://stackoverflow.com/questions/26812770/how-to-install-maven-on-osx-10-10-yosemite)

## Cloud Foundry Client
The developed microservices will run on the Cloud Foundry platform.
Please install the Cloud Foundry Command Line Interface (CLI) and create an account using this tutorial: [CF @SAP CP](https://help.cf.sap.hana.ondemand.com/). Don't forget to request your own trial space as explained there.

## REST Client
In order to test the REST interfaces offered by the microservice, please install the [Chrome Plugin: Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop).

## Tomcat
In order to run/test the microservice locally, a Tomcat Web Server (version 8) needs to be installed. You can download it from [here](http://tomcat.apache.org/) and unzip and save it to a folder on your computer e.g. `C:\apache-tomcat-8` (Windows) or `~/apache-tomcat-8` (Mac).

### Eclipse: Setup and Configure Tomcat Server 
Define a Tomcat v8.0 server in the *Servers* view. In order to configure it double-click the server instance and select the  `Open launch configuration` link.

In the `Edit configuration` dialog ...
- switch to the `Environment` tab and add the following environment variables:
  - USER_ROUTE=https://bulletinboard-users-course.cfapps.sap.hana.ondemand.com
  - VCAP_APPLICATION={}
  - VCAP_SERVICES={"rabbitmq-lite":[{"credentials":{"hostname":"127.0.0.1","password":"guest","uri":"amqp://guest:guest@127.0.0.1:5672","username":"guest"},"name":"rabbitmq-lite","label":"rabbitmq-lite","tags":["rabbitmq33","rabbitmq","amqp"]}],"postgresql-9.3":[{"name":"postgresql-lite","label":"postgresql-9.3","credentials":{"dbname":"test","hostname":"127.0.0.1","password":"test123!","port":"5432","uri":"postgres://testuser:test123!@localhost:5432/test","username":"testuser"},"tags":["relational","postgresql"],"plan":"free"}]}


## Install PostgreSQL database 9.4.X
If you don't want to use the VM, you can also install PostgreSQL locally on your computer.
**Note:** If you still want to use the VM at the same time, you need to disable port forwarding for port 1234 (see above).

Download PostgreSQL installer from [here](http://www.postgresql.org/download/) and run through the installation wizard. Choose `5432` as port.

Note: The postgresql-9.4 service is automatically started.

### Prepare a `test` database using the `DBeaver` Eclipse Plugin
In Eclipse, switch to the `DBeaver` Perspective.

#### Connect to `postgres` Database 
In the `Database Navigator` view create a new connection with the following parameters:
 - Host: localhost
 - Database: postgres
 - User: postgres
 - Password: %your postgres password%

#### Create `testuser` Login Role
In the `Database Navigator` view ensure that the connection to the postgres database is active (means **bold**). Then right click on **PostgreSQL** database connection and select `SQL Editor`, enter there `CREATE USER testuser WITH PASSWORD 'test123!';` and execute it.

#### Create a `test` Database
In the `Database Navigator` view ensure that the connection to the postgres database is active (means **bold**). Then right click on **PostgreSQL - postgres** database and select `Create New Database` and enter in the popup:
- Database Name: test
- Owner: testuser

## Install RabbitMQ 3.6.X
If you don't want to use the VM, you can also install RabbitMQ locally on your computer.
**Note:** If you still want to use the VM at the same time, you need to disable port forwarding for port 5672 (see above).

Download Erlang installer from [here](http://www.erlang.org/download.html) and RabbitMQ installer from [here](https://www.rabbitmq.com/download.html) and run through the installation wizards using the default settings.

#### Starting RabbitMQ
##### Check if RabbitMQ was started automatically and operates fine
- Open a command prompt and list your active TCP listeners (e.g. `netstat -a | find "4369"` on Windows or `netstat -l` on Linux). Look for listening connections bound to port 4369 (Erlang's epmd.exe) and 5672 (RabbitMQ).
- Change directory to `<your_rabbitmq_installation_path>\sbin` or open the "RabbitMQ Command Prompt" (available using the start menu) and run `rabbitmqctl status`. The prompt should display `Status of node rabbit@...` followed by a series of configuration parameters.

If RabbitMQ doesn't operate properly (connection issues), you can either disable your firewall (not recommended) or apply the following steps:
- Go to RabbitMQ's configuration directory. Check the location for your operating system [here](https://www.rabbitmq.com/configure.html#configuration-file) (e.g. it's `%APPDATA%\RabbitMQ\` on Windows).
- Create a RabbitMQ environment configuration file: `rabbitmq-env.bat` (Windows) or `rabbitmq-env.conf` (Linux/Mac).
- Insert the following line into the file and save.
  - Windows: `set RABBITMQ_NODENAME=rabbit@localhost`
  - Linux/Mac: `export RABBITMQ_NODENAME=rabbit@localhost`
- Set a system environment variable called `RABBITMQ_CONF_ENV_FILE` that points to the RabbitMQ environment configuration file (e.g. run `setx RABBITMQ_CONF_ENV_FILE %APPDATA%\RabbitMQ\rabbitmq-env.bat`).

If RabbitMQ is not started automatically, choose one of two methods to start it manually.
- **as a service**: Open a command prompt with administrator privileges (!) and go to `<your_rabbitmq_installation_path>\sbin`. Remove the service `rabbitmq-service remove` and re-install `rabbitmq-service install`. Finally, start the service with `rabbitmq-service start`.
- **as a stand-alone job**: Open a command prompt and go to `<your_rabbitmq_installation_path>\sbin`. Run `rabbitmq-server.bat`. 

#### Enabling RabbitMQ Management Console
In order to use the RabbitMQ management console at its default location (`http://localhost:15672/`), enable the `rabbitmq_management` plugin. Open a command prompt and go to `<your_rabbitmq_installation_path>\sbin`. Run `rabbitmq-plugins enable rabbitmq_management`.

## Install Redis 3.x
Download the Redis MSI installer file from [here](https://github.com/MSOpenTech/redis/releases) using the default settings.
This installs a service which automatically starts Redis.

## Install Node.js and NPM
Install Node.js incl. NPM package manager. Download latest stable release [here](https://nodejs.org/en/).

## Further Reading
- [How to setup VM to use services](/CoursePrerequisites/localEnvSetup/VM_use_as_service_host.md)
