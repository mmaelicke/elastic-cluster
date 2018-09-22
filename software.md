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

*more will follow soon*