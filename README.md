# The 5GMETA Cloud Platform


## Introduction

This Repository contains the deployment files of the 5GMETA Cloud Platform. 

The deployment of the current version of the Cloud Platform can be done as follows:

1. Provisioning of a Kubernetes Cluster
2. Deploymnent of the Cloud Plaform
3. Post Installation configurations

## Prerequisities

The following requirements are needed to be able to deploy the platform:

-  A Kubernetes cluster with a configured PersistentVolume and Dynamic Provisionner e.g. Minikube.
-  When installing the cloud modules, it is necessary to configure the "storageClassName" to the class name of the Kubernetes Cluster. This must be done for MongoDB and PostgreSQL.
-  [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
-  [Helm v3](https://helm.sh/docs/intro/install/)
-  Optional [Docker](https://www.docker.com/get-started/) as provider for Minikube. Other providers can be selected e.g Podman, VirutualBox, etc.
-  Optional [Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform) used to deploy on Amazon EKS
-  Optional [Kubespray](https://github.com/kubernetes-sigs/kubespray) for creation a single node K8s test cluster.

### Prerequisities for a local development environment

-  [Virtualbox](https://www.virtualbox.org/wiki/Downloads) to provide a local virtualisation environment and as provider for Minikube
-  [Vagrant](https://developer.hashicorp.com/vagrant/install)

### Kubernetes Clusters

The deplopyment of the cloud platfrom requires a running Kubernetes cluster.
The Cloud Platform has been tested on:
- A Minikube cluster of (CPUs=6, Memory=16g, Disk-Size=200g) for local development and test

#### Development environments


##### Option 1: Cloud Platform on Minikube <a name="cloud-platform-minikube"></a>

In this documentation, Minikube is used to provide a Kubernetes cluster for local development environment.
- For Minikube this "storageClassName" should be standard for MongoDB and PostgreSQL.

```bash
minikube start --cpus=6  --memory=16g --disk-size=200g
```

After successfully sarting minikube, install the ingress-nginx addons as follow:

```bash
minikube addons enable ingress
```

When using Minikube, it is possible to configure a local DNS server. If such a server is used,
5gmeta-platform.eu can be used a the DNS name for the Minikube IP. It will be necessary to change the configuration of the Helm chart.


##### Options 2: Kubernetes cluster of MS Azure using Kubespay

A single node K8s cluster using [Kubespray](https://github.com/kubernetes-sigs/kubespray) on a [Microsoft Azure](https://azure.microsoft.com/en-us/) VM with  8vCPU and 32GB is used to provide a development and test environment.
Since the cluster has a single node, the type of the Nginx Ingress controller service was set to NodeType. However, a Loadbalancer can be used. 

#### Production environments

The deplopyment of the 5GMETA platform in prodction can be done using any:

- [Kubernetes production cluster](https://kubernetes.io/docs/setup/production-environment/)
- [Managed Kubernetes clusters](https://kubernetes.io/docs/setup/production-environment/turnkey-solutions/)

##### Pre-requisities

The following requirements must be met to deploy in production:
- A K8s cluster configured for production
- A DNS host name for the Cloud and MEC Platforms
- TLS certificates for MEC and CLOUD services
- A SMTP server
- A Nginx Ingress controller and Load Balancer. Services such Apache Kafka can be configure behind a Load Balancer. This step is dependant on each Cloud Provider and requires the adaptation of the Helm Charts.
- Configuration on the Cloud Service Provider of the Network Security Group to open the ports mentionned in the document.

##### Cloud Platform on EKS <a name="cloud-platform-eks"></a>

The [5GMETA](https://cordis.europa.eu/project/id/957360) Cloud Platform has been tested during the project on an [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/) cluster as  illustrated by the  the architecure diagram below. The figure also displays the diferent services exposed by the Cloud platform:

<p align="center">
<img src="./docs/images/Cloud%20Architecture.png">

Cloud Platform Architecture
</p>

For more details on using EKS refers at this document: [Deployment details on EKS](./docs/deployment-options/eks.md).


#### Deployment of the Cloud Platform

The deplopyment of the Cloud Platform is done using one Helm chart which will install the following:

0. Install Cert Manager's CRDs to ensure that Helm is able to create the TLS Certificates
1. Install Cert Manager and create the TLS certificates
2. Install the Prometheus Operator
3. Install MySQL Database and create the databases
4. Install Confluentic Apache Kafka
5. Install the 5GMETA Cloud Platform modules.
6. Install Apache Superset

To install the 5GMETA Cloud Platform follow the instructions below:

- Clone the Cloud Platform

```bash
git clone git@github.com:Akkodis/cloud-platform.git
```

- Edit the Cloud Platform chart's values to set a hostname, usernames and passwords. The values' file can be found in ./cloud-platform/deploy/helm/cloud-platform-chart.

- Then type the following commands:

```bash
cd cloud-platform

# Install other components
kubectl create namespace cert-manager
helm dependency build deploy/helm/cloud-platform-chart
helm install cloud-platform deploy/helm/cloud-platform-chart -n cloud-platform --create-namespace
```
#### Install Apache Superset

Apache Superset has been used as replacement of the Dashboard developped during the 5GMETA project. To install superset, type the following commands

```bash
cd deploy/helm/apache-superset
kubectl create namespace superset
helm repo add superset https://apache.github.io/superset
helm upgrade --install --values values.yaml superset superset/superset -n superset
```

#### Cloud Platform Post-install configuration

After a successful installation:

- The 5GMTA realm must be imported in Keycloak. This realm can be found in cloud-platform/security.
- The Grafana Dashboard must be imported in Grafana

# Knwon Issues

- After the deployment of the Cloud Platform, the Apisx container may crash because of the mismatch between the Oauth2.0 client secret and the client secret in the 5GMETA realm. Make sure to:

   - Import the 5GMETA realm in Keycloak
   - Change the apisix client secret if necessary
   - Update the apisix-routes configmap with the new client secret
   - Delete the crashing apisix pod

# Credits

- Djibrilla Amadou Kountche


# Conclusions and Perspectives

This document presented the 5GMETA Cloud Platfrom and its deployment approach.
