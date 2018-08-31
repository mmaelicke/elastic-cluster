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



*more will follow soon*