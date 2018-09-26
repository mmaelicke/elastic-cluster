# Software setup

In this project we want to use the software cluster as a host for [Elasticsearch](https://www.elastic.co/products/elasticsearch). Some of the presented settings will be specific to Elasticsearch, while others are neccessary to connect the nodes. I will try to keep these two things as good apart as possible.

## OS

The first thing we need is, obviously, an OS. The selection of available OS will change in the future and be dependend on the actual board that you select to be your node. In case you'll also use the [Rock64 by pine64](https://www.pine64.org/?page_id=7147), you'll find a tool for flashing an OS onto the board on their website. It is basically an [Etcher.io](https://etcher.io) specific for pine64 products. It will automatically download the OS image for you. Of couse you could also use the regular Etcher.

Most boards will support some kind of Linux distribution. You can basically use any OS that is capable of running Java 8, as this is the only prerequisite of Elasticseach. As the cluster is (in my case) not connected to the internet, we should choose a very stable distribution. I would recommend an Debian Jessie or Linux Arch. This software instruction will focus on the **minimal Debian Jessie** version, distributed through pine64's etcher version. That's a lightweight Jessie version without a Desktop or any software preinstalled. Flash the OS to an micro SD. In case you have another Linux distro at hands, I would recommend to mount the SD to that Computer because you can just copy and paste all neccessary files onto the SD without ssh'ing into the node.

## Local network

The nodes make up their own network using the ethernet switch build into the cluster shelf. Once they are connected to the switch, we need to set up a hostname and assign a static IP to each node. In order to keep things simple, I will configure the nodes themselves. In case you decided to run some kind of router or managed ethernet switch in the cluster, you won't need this setup.

For my usecase, all hostnames and IP adresses will follow the same pattern:

* `rockX`, for hostname 
* `24.9.13.X` for the IP adress.

In both cases, the `X` will be substituted with an increasing number from 1 to the amount of nodes used.

The Raspberry Pi 3+, which is used as a controller to run the cluster application will also be connected to the Ethernet switch by cable and expose the application by the built in WLAN. It will be assigned the hostname `rockmaster` and use the static IP on `eth0` (in case of Debian Jessie) `24.9.13.111`. 

<div class="alert alert-info">
Of course you can choose any other IP space, but keep in mind, that you might connect your Laptop to the cluster switch for debugging and development or the Pi might connect to an existing network. Make sure, that your IP adress space does not interference with any other application like VirtualBox or Docker or stuff like that (happend...).
</div>
### Debian Jessie

I have written a small Python script to configure the nodes. It produces the needed files, which can then be uploaded to the nodes. This is easiest from a Linux os, as you can just mount the Jessie on the SD card and copy paste the created files. How to use the script is described below. First, we will walk through all adjustments.

On Debian jessie, there are three files that need to be adjusted for networking:

`/etc/hostname`

```
rocknode1
```

In `/etc/hosts` add two lines at the top:

```
127.0.0.1 localhost
127.0.1.1 rocknode1

#The following lines are desirable for IPv6 capable hosts

::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

```

In `/etc/dhcpcd.conf` add two lines to the end of the file:

```
interface eth0
static ip_address=24.9.13.1/24
```

Where you can replace your name pattern in `/etc/hostname` and `/etc/hosts`  and replace the IP address in `/etc/dhcpcd.conf` with your IP pattern.

## Elasticsearch

As layed out before, running Elasticsearch on the elastic cluster is just one option. You could also install a Mongodb daemon on all nodes and distribute the shards across the nodes. These instructions will explain the necessary steps to get Elasticsearch running. One downside of the Debian Jessie I chose was that no Java compiler or runtime environment is available. Therefore, the JDK for Java 8 is included in the `/home/rock64`folder along with elasticsearch (Version 6.2) itself. In principle, the jre (runtime environment) inside the jdk should be enough to run elasticsearch, but I haven't tried that so far. Both, elasticsearch and JDK can just be copied into the home directory of the cluster node. Additionally, there is the `/home/rock64/elasticsearch.yml` file, which has to be copied into the config folder of elasticsearch after modifying it. In case you use the Python script, it will handle this for you. The necessary config used in my cluster version with 5 nodes active looks like:

```
[...]
# ---------------------------------- Cluster -----------------------------------
#
# Use a descriptive name for your cluster:
#
cluster.name: emc2-iwg-1
#
# ------------------------------------ Node ------------------------------------
#
# Use a descriptive name for the node:
#
node.name: rocknode-4

[...]

# ---------------------------------- Network -----------------------------------
#
# Set the bind address to a specific IP (IPv4 or IPv6):
#
#network.host: 192.168.0.1
network.host: 0.0.0.0

[...]

# --------------------------------- Discovery ----------------------------------
#
# Pass an initial list of hosts to perform discovery when new node is started:
# The default list of hosts is ["127.0.0.1", "[::1]"]
#
discovery.zen.ping.unicast.hosts: ["24.9.13.1", "24.9.13.2", "24.9.13.3", "24.9.13.4", "24.9.13.5"]

[...]
```

Note, that is configuration will accept connections from every source. That's why it is important to not directly connect the nodes to an external network or the internet. This Elasticsearch instance does not have any Authentification enabled.

Note: This config still lacks the CORS settings needed allow a JS application to communicate with Elasticsearch. I will update the files soon.

#### Configuration

There is a lot that can be configured on an Elasticsearch instance. Keep in mind, that you need to configure the Elasticsearch applications on all nodes in exactly the same way in order to work properly. But there is one setting, that is mandatory. Elasticsearch uses `mmapfs` directory to store indices and the Debian Jessie OS does not allow enough virtual memory for one process. Therefore, the following line has to be appended to the `/etc/sysctl.conf`:

```
vm.max_map_count=262144
```

In cas you use the Python script to create the necessary files for each node, a modified `sysctl.conf` is already copied into the `etc` that needs to be shipped to the operation system on the SD card. Keep that in mind in case you decide to add additional modifications to the `sysctl.conf`.

#### Starting Elasticsearch

You can find a prepared service file in the home directory of the utils folder. I prefer to operate Elasticsearch as a service, because you can start/stop/restart/reload Elasticsearch easily. Additionally, a service can be enable or disabled. An enabled service will start up automatically on system startup. That's quite handy. Once installed, you can ask for the status like:

```bash
sudo systemctl status elasticsearch.service
```

which will output something like:

```
● elasticsearch.service - Elasticsearch
   Loaded: loaded (/usr/lib/systemd/system/elasticsearch.service; disabled; vend
   Active: inactive (dead)
     Docs: http://www.elastic.co
lines 1-4/4 (END)
```

(This is an Elasticsearch on my Laptop, therefore the path is different.)

Enabling the service permanentily can be done by `systemctl`:

```bash
sudo systemctl enable elasticsearch.service
```

Keep in mind, that this will just enable the service, in order to start it on next system startup. So you either reboot the node, or start the service manually:

```bash
sudo systemctl start elasticsearch.service
```



In case you use the Python script, it will automatically be copied into the prepared location. On Debian Jessie, services live in the `/etc/systemd/system`directory. The most important part of the service file is shown below `/etc/systemd/system/elasticsearch.service` :

```
[Unit]
Description=Elasticsearch
Documentation=http://www.elastic.co
Wants=network-online.target
After=network-online.target

[Service]
RuntimeDirectory=elasticsearch
Environment=ES_HOME=/home/rock64/elasticsearch-6.2.4
Environment=ES_PATH_CONF=/home/rock64/elasticsearch-6.2.4/config
Environment=PID_DIR=/home/rock64
Environment=JAVA_HOME=/home/rock64/jdk1.8.0_171/bin/java


WorkingDirectory=/home/rock64/elasticsearch-6.2.4

User=rock64
Group=rock64

ExecStart=/home/rock64/elasticsearch-6.2.4/bin/elasticsearch -p ${PID_DIR}/elasticsearch.pid --quiet

[...]
```

Two important lines that you might want to change, before deploying the service file to the nodes is the `Environment=JAVA_HOME [...]` and the `ExecStart= [...]`  lines. I haven't tried it yet, but it should absolutely be possible to replace the JDK in the home folder by a JRE and adapt the path here. Might be easier to handle in terms of Java licenes.

The `ExecStart` setting specifies how elasticsearch will be started. Here, it is started iwth the `-p`flag, which will save the PID into the specified file. This makes killing the process easy. Additionally, the `--quiet`flag is set in order to silence Elasticsearch, because nobody will be listening. If you want to, for debugging or whatever, you can just change this line and re-deploy the service file. The Elasticsearch references list more options that can be used on startup.

In case you download a more recent version of Elasticsearch or use other hardware than the Rock64, you will have to change the service file accordingly. 

