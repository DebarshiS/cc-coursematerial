# Using Course-VM Services from Host

The course VM contains PostgreSQL and RabbitMQ servers which are used for local tests (inside the VM).
Currently it is not possible to also use these services from the host (running, for example, Eclipse in Windows)
without the following re-configuration.

## PostgreSQL
In the VM, start the terminal and run the following commands:
- `sudo bash`
- `gedit /etc/postgresql/9.3/main/postgresql.conf`
- in the editor window, change `#listen_addresses = 'localhost'` to `listen_addresses = '*'` (Line 59), then save and quit
- `gedit /etc/postgresql/9.3/main/pg_hba.conf`
- in the editor window, change `host all all 127.0.0.1/32 md5`  to `host all all 0.0.0.0/0 md5` (Line 92), then save and quit
- `/etc/init.d/postgresql restart`
- `exit`

## RabbitMQ
In the VM, start the terminal and run the following commands:
- `sudo bash`
- `gedit /etc/rabbitmq/rabbitmq.config`
- in the editor window, add a new line containing `[{rabbit, [{loopback_users, []}]}].`, then save and quit
- `/etc/init.d/rabbitmq-server restart`
- `exit`
