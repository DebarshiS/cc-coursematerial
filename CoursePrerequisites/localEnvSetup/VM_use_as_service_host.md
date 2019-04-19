# How to use Virtual Machine as Service Host

When you need to access PostgreSQL, RabbitMQ, Redis, or MongoDB from your local machine, you can start the virtual machine to get access to its services.

## Prerequisite
Install the virtual machine according to [this](https://github.wdf.sap.corp/agile-se/vagrant-development-box/blob/master/VMImage_GettingStarted.md) document.
You can skip the step "Set SSH Keys", as those are only needed when using the VM to access GitHub.

### VM configuration

Virtual Box is configured to redirect the local port 8080 to the VM. In order to be able to start a Tomcat server on your local machine, you need to disable this redirection:

- Start the VM
- In the VM window select `Devices` - `Network` - `Network Settings...` - `Port Forwarding`.
- Delete the entry for port `8080`.

Furthermore, the current VM configuration does not accept connections from the outside (which includes your local machine) to internal services like PostgreSQL running inside the VM.

To fix this, perform the following steps:

#### PostgreSQL
 - Inside the VM, start the terminal
 - Type `sudo bash` to become root
 - Edit the file `/etc/postgresql/9.3/main/postgresql.conf` (e.g. by running `gedit /etc/postgresql/9.3/main/postgresql.conf`)
 - Find the line starting with `#listen_addresses` and change it to `listen_addresses = '*'`
 - Save the file and close the editor
 - Edit the file `/etc/postgresql/9.3/main/pg_hba.conf` (e.g. by running `gedit /etc/postgresql/9.3/main/pg_hba.conf`)
 - Find the line `host all all 127.0.0.1/32 md5` and below it add a line `host all all 10.0.2.0/24 md5`
 - Save the file and close the editor
 - Run `/etc/init.d/postgresql restart`

#### RabbitMQ 
 - Inside the VM, start the terminal
 - Type `sudo bash` to become root
 - Enter `echo '[{rabbit, [{loopback_users, []}]}].' > /etc/rabbitmq/rabbitmq.config`
 - Enter `/etc/init.d/rabbitmq-server restart`

#### Redis
 - Inside the VM, start the terminal
 - Type `sudo bash` to become root
 - Edit the file `/etc/redis/redis.conf` (e.g. by running `gedit /etc/redis/redis.conf`)
 - Find the line containing `bind 127.0.0.1` and replace it by `bind 127.0.0.1 10.0.2.15`
 - Enter `/etc/init.d/redis-server restart`

### Headless Mode
For convenience you can also start the VM in headless mode, so that no window is created for it.
To do that, right-click on the VM in Virtual Box and select `Start` - `Headless Start`.

To shutdown the VM either show it and use the menu in the upper right, or connect to the virtual machine using SSH:
`ssh vagrant@localhost -p 2222 sudo poweroff` (the password is `vagrant`)
