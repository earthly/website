---
title: "How To Deploy a Kubernetes Cluster Using the CRI-O Container Runtime"
toc: true
author: Mercy Bassey
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Kubernetes
 - Container
 - CRI-O
 - Automation
excerpt: |
    Learn how to deploy a Kubernetes cluster using the CRI-O container runtime. This tutorial provides step-by-step instructions for setting up the necessary components, configuring the cluster, and deploying your first application.
last_modified_at: 2023-07-19
categories:
  - Cloud
---
**This article explains how to deploy Kubernetes CRI-O. Earthly streamlines the build process for Kubernetes applications. [Learn more about Earthly](https://cloud.earthly.dev/login).**

Are you tired of managing your containerized applications manually? Do you want a more efficient and automated way to deploy and manage your applications? Look no further than Kubernetes!

Kubernetes is a powerful platform for managing containerized applications, providing a unified API for managing containers and their associated resources, such as networking, storage, and security. And with the ability to work with different container runtimes like [Docker](https://docs.docker.com/), [Containerd](https://containerd.io/docs/getting-started/), [CRI-O](https://docs.openshift.com/container-platform/3.11/crio/crio_runtime.html) etc. you can choose the runtime that's best for your needs.

[CRI-O](https://cri-o.io/) is an optimized container engine specifically designed for Kubernetes. With CRI-O, you can enjoy all the benefits of Kubernetes while using a container runtime that is tailored to your needs.

In this article, you will learn how to deploy a Kubernetes cluster using the CRI-O container runtime. You'll learn everything you need to know, from setting up the necessary components to configuring your cluster and deploying your first application.

## Prerequisite

To follow along in this tutorial, you'll need the following:

- Understanding of Kubernetes and Linux commands.
- This tutorial uses a Linux machine with an Ubuntu 22.04 LTS (recommended) distribution. Any other version will work fine too.
- Virtual machines (VMs) as master and worker with at least the minimum specifications below:

| Nodes  | Specifications | IP Address |
| --- | --- | --- |
| Master | 2GB RAM and 2CPUs | 170.187.169.145 |
| Worker | 1GB RAM and 1CPU | 170.187.169.226 |

## What Is CRI-O?

**[CRI-O](https://cri-o.io/)** pronounced as (*cry-oh)* stands for Container Runtime Interface (CRI) for OpenShift (O); It is an open-source project for running Kubernetes containers on Linux operating systems and is designed specifically for Kubernetes, providing a lightweight and optimized runtime for running containers in a Kubernetes cluster. It implements the Kubernetes [Container Runtime Interface (CRI)](https://kubernetes.io/blog/2016/12/container-runtime-interface-cri-in-kubernetes/), which is a standard interface between Kubernetes and container runtimes.

It is fully compatible with the Kubernetes Container Runtime Interface (CRI) and is designed to provide a secure, stable, and reliable platform for running containerized applications.

Deploying a Kubernetes cluster using the CRI-O container runtime can help you streamline your container management processes, improve the security of your applications, and simplify the overall management of your infrastructure.

## Configuring Kernel Modules, Sysctl Settings, and Swap

Prior to setting up a cluster with CRI-O, the [Kubernetes official documentation](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#before-you-begin) instructs that you have the following requirements setup on all your servers (both master and worker nodes) before you can begin to setup Kubernetes; these requirements include enabling kernel modules, configuring some [sysctl](https://linuxize.com/post/sysctl-command-in-linux/) settings, and disabling [swap](https://linuxhint.com/swap_memory_linux/).

<div class="notice--info">

Swap is a space on a hard disk that is used as a temporary storage area for data that cannot be stored in RAM at that time. When the system runs out of physical memory (RAM), inactive pages from memory are moved to the swap space, freeing up RAM for other tasks. The swap space is used by the operating system as an extension of the RAM, allowing the system to run more programs or larger programs than it could otherwise handle. Swap is commonly used in modern operating systems like Linux and Windows.
</div>
Execute the following command on both of your servers (master and worker node) to [disable swap](https://discuss.kubernetes.io/t/swap-off-why-is-it-necessary/6879/4). This step is crucial as leaving `swap` enabled can interfere with the performance and stability of the Kubernetes cluster:

~~~{.bash caption=">_"}
swapoff -a
~~~

<div class="notice--info">

In the context of Kubernetes, it is recommended to disable swap space because it can interfere with the performance and stability of the Kubernetes cluster. This is because the Kubernetes scheduler may not be aware of the memory usage on the host system if swap space is enabled, which can lead to issues with pod scheduling and resource allocation.

So, the `swapoff -a` command disables all swap devices or files on a Linux system, ensuring that Kubernetes can manage the host system's memory resources accurately.
</div>

Remove any reference to swap space from the **`/etc/fstab`** file on both servers using the command below:

~~~{.bash caption=">_"}
sed -i '/swap/d' /etc/fstab
~~~

This ensures that your servers will not attempt to activate swap at boot time.

- The **`/etc/fstab`** file is used to define file systems that are mounted at boot time, including the swap partition or file.
- The [**`sed`**](https://www.ibm.com/docs/en/ssw_aix_72/s_commands/sed.html) command is a powerful utility used to manipulate text in files or streams. In this case, the command uses **`sed`** to edit the **`/etc/fstab`** file and remove any line containing the string "swap".

Now display the status of swap devices or files on your servers using the following command:

~~~{.bash caption=">_"}
swapon -s
~~~

Since you have turned off swap, you should have no output:

<div class="wide">
![Disabling swap]({{site.images}}{{page.slug}}/gGzREHt.png)
</div>

Append the `**overlay**` and `**br_netfilter`**kernel modules to the**`/etc/modulesload.d/crio.conf`** file which is necessary for the proper functioning of the CRI-O container runtime when your servers reboot.

<div class="notice--info">
The [**`overlay`** module](https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html) is used to support overlay filesystems, which is a requirement for many container runtimes including CRI-O. Overlay filesystems allow the efficient use of storage space by creating layers on top of each other. This means that multiple containers can share a base image while having their own writable top layer.

The[**`br_netfilter`** module](https://www.netfilter.org/documentation/) is required for the [iptables rules](https://www.digitalocean.com/community/tutorials/how-to-list-and-delete-iptables-firewall-rules) that are used for network address translation (NAT) with bridge networking. Bridge networking is a way to connect multiple containers together into a single network. By using a bridge network, all containers in the network can communicate with each other and with the outside world.

By adding the **`overlay`** and **`br_netfilter`** modules to the **`/etc/modules-load.d/crio.conf`** file, the modules will be loaded automatically at boot time. This ensures that the necessary kernel modules are available for the CRI-O container runtime to function properly. Without these modules, the CRI-O runtime would not be able to properly create and manage containers on the system.

</div>

~~~{.bash caption=">_"}
cat >>/etc/modules-load.d/crio.conf<<EOF
overlay
br_netfilter
EOF
~~~

Enable the kernel modules for the current session manually using the following commands:

~~~{.bash caption=">_"}
modprobe overlay
modprobe br_netfilter
~~~

By running the commands **`modprobe overlay`** and **`modprobe br_netfilter`**, the necessary kernel modules are loaded into the kernel's memory. This ensures that the modules are available for use by the CRI-O container runtime for this current session.

<div class="wide">
![Enabling kernel modules]({{site.images}}{{page.slug}}/Ad9XQuw.png)
</div>

Confirm that the kernel modules required by CRI-O are loaded and available on both servers using the following commands:

~~~{.bash caption=">_"}
lsmod | grep overlay
lsmod | grep br_netfilter
~~~

<div class="wide">
![Verifying kernel modules]({{site.images}}{{page.slug}}/zeyH1s5.png)
</div>

Provide networking capabilities to containers by executing the following command:

~~~{.bash caption=">_"}
cat >>/etc/sysctl.d/kubernetes.conf<<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables  = 1
net.ipv4.ip_forward                 = 1
EOF
~~~

This command will append the following lines  `net.bridge.bridge-nf-call-ip6tables = 1`, `net.bridge.bridge-nf-call-iptables  = 1`, and `net.ipv4.ip_forward             = 1` to the **`/etc/sysctl.d/kubernetes.conf`** file.

These lines set some important kernel parameters that are required for Kubernetes and CRI-O to function properly:

- **`net.bridge.bridge-nf-call-ip6tables = 1`** and **`net.bridge.bridge-nf-call-iptables = 1`** enable the kernel to forward network traffic between containers using bridge networking. This is important because Kubernetes and CRI-O use bridge networking to create a single network interface for all containers on a given host.
- **`net.ipv4.ip_forward = 1`** enables IP forwarding, which allows packets to be forwarded from one network interface to another. This is important for Kubernetes because it needs to route traffic between different pods in a cluster.

By appending these lines to **`/etc/sysctl.d/kubernetes.conf`**, the settings will be applied every time the system boots up. This ensures that the kernel parameters required for Kubernetes and CRI-O are always set correctly.

Be sure to run the command below so the *sysctl* settings above take effect for the current session:

~~~{.bash caption=">_"}
sysctl --system
~~~

If the settings are applied, you should have an output similar to the one below:

<div class="wide">
![Enabling kernel modules to take effect in current session]({{site.images}}{{page.slug}}/cSfQrMn.png)
</div>

## Setting Up Firewall

Setting up a firewall when deploying a Kubernetes cluster is important because it helps secure the cluster and prevent unauthorized access to the Kubernetes cluster by blocking incoming traffic from external sources that are not explicitly allowed. It also limits the scope of potential attacks, making it harder for attackers to gain unauthorized access to the cluster.

Therefore, you will follow the steps in this section to set up a firewall on your servers.

Firstly, execute the following command on both servers to enable the [Uncomplicated Firewall (UFW](https://en.wikipedia.org/wiki/Uncomplicated_Firewall)) on the system. Once enabled, UFW will start automatically at boot and enforce the firewall rules you configure:

~~~{.bash caption=">_"}
ufw enable
~~~

<div class="wide">
![Enabling ufw on all servers]({{site.images}}{{page.slug}}/2GobvWy.png)
</div>

According to the [Kubernetes official documentation](https://kubernetes.io/docs/reference/networking/ports-and-protocols/), the required ports needed for your Kubernetes cluster are as follows. These ports are only to be open on the server you'd like to use as the control plane:

- Port `6443` for the Kubernetes API server.
- Port `2379:2380` for the ETCD server client API.
- Port `10250` for the Kubelet API.
- Port `10259`  for the kube scheduler.
- Port `10257`  for the Kube controller manager.

~~~{.bash caption=">_"}
# Opening ports for Control Plane
sudo ufw allow 6443/tcp
sudo ufw allow 2379:2380/tcp
sudo ufw allow 10250/tcp
sudo ufw allow 10259/tcp
sudo ufw allow 10257/tcp
~~~

<div class="wide">
![Opening ports for control plane on master node]({{site.images}}{{page.slug}}/XVuI6Rf.png)
</div>

Then execute the following commands on the same server to open ports for the [Calico CNI](https://docs.tigera.io/calico/3.25/getting-started/kubernetes/requirements#network-requirements) as this is the Kubernetes network plugin we will be using:

~~~{.bash caption=">_"}
# Opening ports for Calico CNI
sudo ufw allow 179/tcp #allows incoming TCP traffic on port 179, 
#which is used by the Kubernetes API server for communication 
# with the etcd datastore
sudo ufw allow 4789/udp #allows incoming UDP traffic on port 4789, 
#which is used by the Kubernetes networking plugin (e.g. Calico) 
# for overlay networking.
sudo ufw allow 4789/tcp #allows incoming TCP traffic on port 4789, 
#which is also used by the Kubernetes networking plugin for 
# overlay networking.
sudo ufw allow 2379/tcp #allows incoming TCP traffic on port 2379, 
#which is used by the etcd datastore for communication 
# between cluster nodes.
~~~

<div class="wide">
![Opening ports for calico CNI on master node]({{site.images}}{{page.slug}}/WTVWEMe.png)
</div>

Now display the current status of the Uncomplicated Firewall (UFW) on the supposed control plane using the following command:

~~~{.bash caption=">_"}
sudo ufw status
~~~

You should see a list of the active firewall rules, including which ports are allowed:

<div class="wide">
![Verifying ufw status]({{site.images}}{{page.slug}}/V70491c.png)
</div>

Next, run the following commands on the server that will be used as a worker node. If you have multiple worker nodes, execute these commands on all of them:

~~~{.bash caption=">_"}
# Opening ports for Worker Nodes
sudo ufw allow 10250/tcp #Kubelet API
sudo ufw allow 30000:32767/tcp #NodePort Services

# Opening ports for Calico CNI
sudo ufw allow 179/tcp
sudo ufw allow 4789/udp
sudo ufw allow 4789/tcp
sudo ufw allow 2379/tcp
~~~

<div class="wide">
![Opening ports for both Kubernetes and Calico on worker node(s)]({{site.images}}{{page.slug}}/OrCF8zF.png)
</div>

Display the current status of the Uncomplicated Firewall (UFW) on the supposed worker node(s) using the following command:

~~~{.bash caption=">_"}
sudo ufw status
~~~

<div class="wide">
![Verifying ufw status on worker node]({{site.images}}{{page.slug}}/5PZBU9w.png)
</div>

<div class="notice--info">
Be sure to also allow connections to your server(s) by adding the following firewall rule **`sudo ufw allow 22/tcp`**. That way, you will also have access to the server anytime.

</div>

## Installing the CRI-O Container Runtime

In Kubernetes, a container runtime is responsible for managing the lifecycle of containers. It is the component that actually runs the container images and provides an interface between Kubernetes and the container. Since the container runtime we will be using is CRI-O, we'll go ahead to install it on our two servers (master and worker nodes).

Create two environment variables **OS*** and **CRIO-VERSION** on all your servers and set them to the following values **22.04** and **1.26** using the commands below:

~~~{.bash caption=">_"}
OS=xUbuntu_22.04
CRIO_VERSION=1.26
~~~

This ensures that the correct version of CRI-O is installed on the specific version of the operating system. The **`OS`** variable ensures that the package repository used to install the software is the one that corresponds to the operating system version, while the **`CRIO_VERSION`** variable ensures that the correct version of the software is installed.

Execute the following commands to add the cri-o repository via `apt`, so that the package manager can find and install the required packages:

~~~{.bash caption=">_"}

echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /"|sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable.list
echo "deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$CRIO_VERSION/$OS/ /"|sudo tee /etc/apt/sources.list.d/devel:kubic:libcontainers:stable:cri-o:$CRIO_VERSION.list
~~~

<div class="wide">
![Exporting variables and adding CRI-O repository via apt]({{site.images}}{{page.slug}}/Yljz6R5.png)
</div>

Download the GPG key of the CRI-O repository via curl:

<div class="notice--info">
[GPG](https://medium.com/@azerella/gpg-for-dummies-5bdde94fa36d) (GNU Privacy Guard) is a tool used for secure communication and data encryption. A GPG key is a unique code used to verify the authenticity and integrity of a software package or repository.

In the context of the CRI-O repository, downloading the GPG key helps to ensure that the packages we are downloading are genuine and have not been tampered with. This is important for security reasons, as it helps to prevent the installation of malicious software on our system.
</div>

~~~{.bash caption=">_"}

curl -L https://download.opensuse.org/repositories/devel:kubic:libcontainers:stable:cri-o:$CRI_VERSION/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | sudo apt-key --keyring /etc/apt/trusted.gpg.d/libcontainers.gpg add -
~~~

<div class="wide">
![Downloading GPG keys of the CRI-O repository]({{site.images}}{{page.slug}}/OavHZpW.png)
</div>

Update the package repository and install the CRI-O container runtime along with its dependencies using the following commands:

~~~{.bash caption=">_"}
sudo apt-get update 
sudo apt-get install -qq -y cri-o cri-o-runc cri-tools
~~~

<div class="wide">
![Updating servers and installing CRI and its components]({{site.images}}{{page.slug}}/TJSGQto.png)
</div>

Run the following commands to reload the systemd configuration and then enable and start the CRI-O service:

~~~{.bash caption=">_"}
systemctl daemon-reload
systemctl enable --now crio
~~~

<div class="wide">
![Reloading systemd and enabling cri-o]({{site.images}}{{page.slug}}/srz9k5g.png)
</div>

Verify the status and configuration of the CRI-O container runtime after installation with the following command:

~~~{.bash caption=">_"}
crictl info
~~~

You should see the following output which implies that the CRI-O container runtime is ready for use:

<div class="wide">
![Verifying crictl info]({{site.images}}{{page.slug}}/l3xThHg.png)
</div>

You can further check the CRI-O version with the following command:

~~~{.bash caption=">_"}
crictl version
~~~

<div class="wide">
![Checking CRI-O version]({{site.images}}{{page.slug}}/4PWzqBT.png)
</div>

## Installing Kubernetes Components

Since you have now installed the CRI-O container runtime, the next step is to install the components for Kubernetes. These components are *kubeadm*, *kubelet* and *kubectl*

Add the GPG key for the Kubernetes repository, download the Kubernetes repository, and install the Kubernetes components with the following commands:

~~~{.bash caption=">_"}
# Add GPG key for Kubernetes repository
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg \
| apt-key add -

# Add the Kubernetes apt repository to the local apt repository 
# configuration
apt-add-repository "deb http://apt.kubernetes.io/ kubernetes-xenial main"

# installs the Kubernetes components/packages
apt install -qq -y kubeadm=1.26.0-00 kubelet=1.26.0-00 kubectl=1.26.0-00 
~~~

<div class="wide">
![Adding GPG key and repository for kubernetes components]({{site.images}}{{page.slug}}/evYbqfz.png)
</div>

<div class="wide">
![Installing kubernetes components]({{site.images}}{{page.slug}}/oBvzffI.png)
</div>

<div class="notice--info">
Be sure to always install the same version as the CRI-O container runtime for your Kubernetes components else you might come across some errors.

</div>

## Initializing Kubernetes Cluster on Control Plane

Initializing a Kubernetes cluster on the control plane involves setting up the master node of the cluster. The master node (The server with the highest number of resources like storage, cpu etc) is responsible for managing the state of the cluster, scheduling workloads, and monitoring the overall health of the cluster.

First, run the following commands to enable the *kubelet* service and initialize the master node as the machine to run the control plane components (the API server, etcd, controller manager, and scheduler) :

~~~{.bash caption=">_"}
# Enable the Kubelet service
systemctl enable kubelet
# Lists and pulls all images that Kubeadm requires \
#specified in the configuration file
kubeadm config images pull
~~~

<div class="wide">
![Enabling kubelet service and pulling kubeadm images]({{site.images}}{{page.slug}}/nW1OfkH.png)
</div>

To initialize a Kubernetes cluster on the control plane, execute the following command:

~~~{.bash caption=">_"}
kubeadm init --pod-network-cidr=192.168.0.0/16 \
--cri-socket unix:///var/run/crio/crio.sock
~~~

This initializes a Kubernetes control plane with CRI-O as the container runtime and specifies the [Pod network CIDR range](https://sookocheff.com/post/kubernetes/understanding-kubernetes-networking-model/) as well as the CRI socket for communication with the container runtime.

The **`kubeadm init`** command creates a new Kubernetes cluster with a control plane node and generates a set of certificates and keys for secure communication within the cluster. It also writes out a **`kubeconfig`** file that provides the necessary credentials for **`kubectl`** to communicate with the cluster.

- The **`-pod-network-cidr`** flag: Specifies the Pod network CIDR range that will be used by the cluster. The Pod network is a [flat network](https://kodekloud.com/blog/kubernetes-networking-explained/#pod-to-pod-communication) that connects all the Pods in the cluster, and this CIDR range specifies the IP address range for this network.
- The **`-cri-socket`** flag:  Specifies the CRI socket that Kubernetes should use to communicate with the container runtime. In this case, it specifies the Unix socket for CRI-O located at **`/var/run/crio/crio.sock`**.

Once the Kubernetes cluster has been initialized successfully, you should have the below output:

<div class="wide">
![Initializing Kubernetes cluster on control plane node]({{site.images}}{{page.slug}}/Q9tNrtr.png)
</div>

You can see in the image above the command to be used to connect and interact with the Kubernetes cluster and a token to join worker nodes to the master node which can also be regenerated.

### Deploying the Calico Network for Kubernetes

Deploying [Calico Network in Kubernetes](https://docs.tigera.io/calico/3.25/getting-started/kubernetes/quickstart) means integrating the Calico network policy engine with a Kubernetes cluster to enforce network policies and provide network connectivity between containers. Calico helps in securing network communication within the cluster.

First, execute the following command, so you can use and interact with the Kubernetes cluster:

~~~{.bash caption=">_"}
export KUBECONFIG=/etc/kubernetes/admin.conf
~~~

Run the command on the master node to deploy the Calico Network:

~~~{.bash caption=">_"}

kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/calico.yaml
~~~

<div class="wide">
![Deploying calico network]({{site.images}}{{page.slug}}/GLaOYrh.png)
</div>

### Joining Worker Nodes

Joining the worker node(s) with the master node is very important as the worker nodes run the workloads or containers in the cluster and are controlled by the master node. The master node manages the worker nodes, maintains the cluster state, and communicates with the API server. This adds more capacity to the cluster, allowing it to manage and run more containers.

Execute the below command on the control plane node to generate a join command that can be used by worker nodes to join the Kubernetes cluster:

~~~{.bash caption=">_"}
kubeadm token create --print-join-command
~~~

This command generates a token and prints a command that can be used by worker nodes to join the cluster. The command also includes a token and the IP address of the control plane node:

Now execute the generated token on the worker node(s) to join them to the cluster:

<div class="wide">
![Generating join token for worker node(s)]({{site.images}}{{page.slug}}/WmrJRx4.png)
</div>

If the joining successful, you should have the below output:

<div class="wide">
![Joining worker node to Kubernetes cluster]({{site.images}}{{page.slug}}/8SzjwRv.png)
</div>

To verify, run the command on the control plane node (master node) to get the nodes available in the cluster:

~~~{.bash caption=">_"}
kubectl get nodes
~~~

If you have the following output, then you have successfully deployed a Kubernetes cluster with the CRI-O container runtime:

<div class="wide">
![Getting nodes]({{site.images}}{{page.slug}}/iq2a9KJ.png)
</div>

## Creating a Deployment for Testing

Now that you have your Kubernetes cluster up and running, it's time to test this cluster.

First, download the Kubeconfig file of your cluster to your local machine with the following commands:

~~~{.bash caption=">_"}
scp root@CONTROL_PLANE_IP_ADDRESS:/etc/kubernetes/admin.conf \
~/.kube/config
~~~

If you don't do this, you won't be able to use and interact with your cluster.

<div class="wide">
![Copying Kubeconfig file from control plane node to local machine]({{site.images}}{{page.slug}}/fdH7c8y.png)
</div>

Verify the status of the cluster and its components using the following command:

~~~{.bash caption=">_"}
kubectl cluster-info
~~~

When executed, it displays the URLs for the Kubernetes API server as well as the cluster DNS service IP:

<div class="wide">
![Verifying cluster info]({{site.images}}{{page.slug}}/gmzKlDF.png)
</div>

Retrieve the information about the nodes in the Kubernetes cluster, including their name, status, and IP addresses, and the information about all the pods running in the cluster, including the namespace, name, status, and IP address of each pod with the following commands:

~~~{.bash caption=">_"}
kubectl get nodes
kubectl get pods -A
~~~

<div class="wide">
![Getting nodes and pods ]({{site.images}}{{page.slug}}/4JcUS1d.png)
</div>

Lastly, create an Nginx deployment with the following command to test the Kubernetes cluster:

~~~{.bash caption=">_"}
kubectl create deploy nginx-web-server --image nginx
~~~

<div class="wide">
![Creating and verifying nginx web server deployment]({{site.images}}{{page.slug}}/DbSVmMz.png)
</div>

Create a NodePort service with the following command to expose the **`nginx-web-server`** deployment on a static port (port 80) on each node in the cluster, which allows external traffic to access the service:

~~~{.bash caption=">_"}
kubectl expose deploy nginx-web-server --port 80 --type NodePort
~~~

<div class="wide">
![Exposing nginx web server ]({{site.images}}{{page.slug}}/f9SdQit.png)
</div>

To view the nginx web server, execute the following over your preferred web browser:

~~~{.bash caption=">_"}
# MASTER_IP:NODEPORT_SERVICE_PORT
http://170.187.169.145:32141/

OR

# WORKER_IP:NODEPORT_SERVICE_PORT
http://170.187.169.226:32141/
~~~

<div class="wide">
![Accessing nginx web server over a web browser]({{site.images}}{{page.slug}}/jUsmM9L.png)
</div>

## Verifying Communication Between Nodes

After deploying a Kubernetes cluster, it is important to verify the communication between nodes to ensure that the nodes are able to communicate with each other properly. The reason is most times there might be network issues that may be present, such as misconfigured firewalls or incorrect network settings.

For illustration purposes, we will verify by deploying a [**`busybox`**](https://hub.docker.com/_/busybox) pod on the worker node and ping other nodes to see if they'd respond.

Create a new pod running a busybox container with the name **`busybox`** and attach a terminal session to it with the following command:

~~~{.bash caption=">_"}
kubectl run -it --rm busybox --image busybox
~~~

<div class="wide">
![Creating busybox pod]({{site.images}}{{page.slug}}/KPGT8m2.png)
</div>

If you open another terminal and run the following command, you will see that the **`busy-box`** pod has been created and is running :

~~~{.bash caption=">_"}
kubectl get pods -o wide -A
~~~

<div class="wide">
![Getting pods from all namespaces]({{site.images}}{{page.slug}}/CXiZwfN.png)
</div>

You can see in the image above, that the **`busybox`** container is running on the worker node with network IP **`192.168.171.66`**

<div class="notice--info">
Take note of the other network IP addresses, as we will be using them to demonstrate the network connection between them.

</div>

You can also execute the following command in the **`busybox`** shell to confirm:

~~~{.bash caption=">_"}
hostname -i
~~~

Execute the following command to check the network connectivity between the worker node running the **`busybox`** container and one of the master node network IP addresses - `10.85.0.4` for instance:

~~~{.bash caption=">_"}
ping ANY_OF_THE_MASTER_NODE_NETWORK_IP
ping 10.85.0.4
~~~

<div class="wide">
![Pinging master node network IP]({{site.images}}{{page.slug}}/0vZOhXU.png)
</div>

From the image above you can see that you have outputted an error message **permission denied (are you root)?**.

Even if you try pinging another network IP, you should still have the same error, as shown below:

~~~{.bash caption=">_"}
ping 170.187.169.145
~~~

<div class="wide">
![Pinging master node with IP(170.187.169.145)]({{site.images}}{{page.slug}}/kgYQ3n7.png)
</div>

Pinging master node with IP(170.187.169.145)

This error is CRI-O-specific, in the sense that some capabilities were removed to make CRI-O more secure.

Since the release of **[CRI-O v1.18.0](https://cri-o.github.io/cri-o/v1.18.0.html)**, The **CRI-O** container runtime now runs containers without the `NET_RAW` capability by default. This change was made for security reasons to reduce the attack surface of containerized applications.

The `NET_RAW` capability is used to create and manipulate raw network packets, which could potentially be used to launch a variety of network-based attacks.

So to correct the **permission denied (are you root)?** error, we need to configure CRI-O to run containers with this capability enabled by default.

Firstly, delete the **`busybox`**  container by simply typing the command `exit` and you should have the below output:

<div class="wide">
![Deleting busybox container]({{site.images}}{{page.slug}}/kD5mlZ1.png)
</div>

SSH into the worker node using the following command:

~~~{.bash caption=">_"}
ssh root@WORKER_NODE_IP
ssh root@170.187.169.226
~~~

Run the following command to open up the **`/etc/crio/crio.conf`** file using the nano text editor, you can use any text editor of your choice too:

~~~{.bash caption=">_"}
nano /etc/crio/crio.conf
~~~

Scroll through the file, stop where you see the lists of capabilities and add the **`NET_RAW`** capability in the list as shown below, be sure to also uncomment the capabilities by simply deleting the `#` character before each capability:

<div class="wide">
![Adding net_raw capability]({{site.images}}{{page.slug}}/zyiTs1c.png)
</div>

Save the file and run the **`systemctl restart crio`** command to restart CRI-O.

Now from your local machine execute the `kubectl run -it --rm busybox --image busybox` command again and try running the `ping MASTER_NODE_IP` command:

<div class="wide">
![Pinging master node with IP(170.187.169.145)]({{site.images}}{{page.slug}}/aFiWUhV.png)
</div>

You can see from the image above that both commands **`ping 10.85.0.4`** and **`ping 170.187.169.145`** becomes a success.

## Conclusion

In this tutorial, you've learned to set up and pair CRI-O with Kubernetes on an Ubuntu 22.04LTS server, initiate a Kubernetes cluster, and test an Nginx server deployment. CRI-O's focus on performance, security, and Kubernetes compatibility make it an excellent choice for large-scale containerized application deployment.

As you continue to explore and optimize your containerized applications, you might want to streamline your build processes. For that, we recommend checking out [Earthly](https://cloud.earthly.dev/login).

Enjoyed learning about CRI-O and Kubernetes? Then you'll definitely appreciate what Earthly has to offer.

{% include_html cta/bottom-cta.html %}
