# Software setup

In this project we want to use the software cluster as a host for [Elasticsearch](https://www.elastic.co/products/elasticsearch). Some of the presented settings will be specific to Elasticsearch, while others are neccessary to connect the nodes. I will try to keep these two things as good apart as possible.

## OS

The first thing we need is, obviously, an OS. The selection of available OS will change in the future and be dependend on the actual board that you select to be your node. In case you'll also use the [Rock64 by pine64](https://www.pine64.org/?page_id=7147), you'll find a tool for flashing an OS onto the board on their website. It is basically an [Etcher.io](https://etcher.io) specific for pine64 products. It will automatically download the OS image for you. Of couse you could also use the regular Etcher.

Most boards will support some kind of Linux distributions. You can basically use any OS that is capable of running Java 8, as this is the only prerequisite of Elasticseach. As the cluster is (in my case) not connected to the internet, we should choose a very stable distribution. I would recommend an Debian Jessie or Linux Arch. This software instruction will focus on the **minimal Debian Jessie** version, distributed through pine64's etcher version. That's a lightweight Jessie version without a Desktop or any software preinstalled. Flash the OS to an micro SD. In case you have another Linux distro at hands, I would recommend to mount the SD to that Computer because you can just copy and paste all neccessary files onto the SD without ssh'ing into the node.



*more will follow soon*