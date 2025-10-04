# The 5GMETA Cloud Platform

## Introduction

This repository contains the deployment files of the 5GMETA Cloud Platform. 

The deployment of the current version of the Cloud Platform can be done as follows:

1. Provisioning of a Kubernetes cluster
2. Deploymnent of the Cloud Plaform manually or by ArgoCD.
3. Post Installation configurations

## Prerequisities

The following requirements must be satisfied to deploy the platform:

-  A Kubernetes cluster with a configured PersistentVolume and Dynamic Provisionner e.g. Minikube.
-  When installing the cloud modules, it is necessary to configure a default storage class.
-  [Kubectl](https://kubernetes.io/docs/tasks/tools/#kubectl)
-  [Helm v3](https://helm.sh/docs/intro/install/)
-  Optional [Docker](https://www.docker.com/get-started/) as provider for Minikube. Other providers can be selected e.g Podman, VirutualBox, etc.
-  Optional [Terraform](https://developer.hashicorp.com/terraform/install?product_intent=terraform) used to deploy on Amazon EKS
-  Optional [Kubespray](https://github.com/kubernetes-sigs/kubespray) for creation a single node K8s test cluster.
-  Optional [Metallb] installed on the Kubernetes cluster. This was tested on a multi nodes cluster. BGP advertisement was used with Calico. 
-  Optional [ArgoCD] installed on the Kubernetes cluster. 

### Kubernetes Clusters

The deplopyment of the cloud platfrom requires a running Kubernetes cluster. The Cloud Platform has been tested on:
- A Minikube cluster of (CPUs=6, Memory=16g, Disk-Size=200g) for local development and test
- A multi node cluster deployed using Kubespray
- A single node cluster deployed on a Azure VM using Kubespay

#### Development environments

##### Option 1: Cloud Platform on Minikube <a name="cloud-platform-minikube"></a>

Minikube has been used to provide a Kubernetes cluster for local development environment.

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

A single node K8s cluster using [Kubespray](https://github.com/kubernetes-sigs/kubespray) on a [Microsoft Azure](https://azure.microsoft.com/en-us/) VM with  8 vCPU and 32GB is used to provide a development and test environment. Since the cluster has a single node, the type of the Nginx Ingress controller service was set to NodeType. However, a Loadbalancer can be used. 

#### Production environments

The deplopyment of the 5GMETA platform in production can be done using any:

- [Kubernetes production cluster](https://kubernetes.io/docs/setup/production-environment/)
- [Managed Kubernetes clusters](https://kubernetes.io/docs/setup/production-environment/turnkey-solutions/)

#### Pre-requisities

The following requirements must be met to deploy in production:
- A K8s cluster configured for production.
- A FQDN for the Cloud and MEC Platforms.
- TLS certificates for MEC and Cloud services. These can be obtained by using cert-manager.
- A SMTP server.
- A Nginx Ingress controller and Load Balancer. Services such Apache Kafka can be configure behind a Load Balancer. This step is dependant on each Cloud Provider and requires the adaptation of the Helm Charts.
- Configuration on the Cloud Service Provider of the Network Security Group to open the ports mentionned in the document.

#### GitOps using ArgoCD

The Cloud Platform can be installed using an ArgoCD application. The application's description can be found here: [cloud-platform](https://github.com/Akkodis/cloud-platform/tree/main/deploy/argocd)

For deploying in production, the Helm values must be changed using ArgoCD UI. 


#### Manual deployment of the Cloud Platform


##### Install Cert-manager 


Before installing the Cloud Platform, cert-manager must be installed as follows:

```bash
helm install \
  cert-manager oci://quay.io/jetstack/charts/cert-manager \
  --version v1.18.2 \
  --namespace cert-manager \
  --create-namespace \
  --set crds.enabled=true
```

##### Deploy the Cloud Platform

The deplopyment of the Cloud Platform is done using one Helm chart which will install the following:

1. the Prometheus Operator
2. MariaDB and create the databases
3. A modified version of the Confluentic Apache Kafka
4. Install the 5GMETA Cloud Platform modules.

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
helm dependency build deploy/helm/cloud-platform-chart
helm install cloud-platform deploy/helm/cloud-platform-chart -n cloud-platform --create-namespace
```

#### Cloud Platform Post-install configuration

After a successful installation:

-  The Apisix Pod will crash. Please edit the apisix deployment and change the command in the Pod form command: ["sh", "-c","ln -s /apisix-config/apisix.yaml /usr/local/apisix/conf/apisix.yaml && /docker-entrypoint.sh docker-start"] to command: ["sh", "-c","/docker-entrypoint.sh docker-start"]


## Cloud Platform on EKS <a name="cloud-platform-eks"></a>

The [5GMETA](https://cordis.europa.eu/project/id/957360) Cloud Platform has been tested during the project on an [Amazon Elastic Kubernetes Service (EKS)](https://aws.amazon.com/eks/) cluster as  illustrated by the  the architecure diagram below. The figure also displays the diferent services exposed by the Cloud platform:

<p align="center">
<img src="./docs/images/Cloud%20Architecture.png">

Cloud Platform Architecture
</p>

For more details on using EKS refers at this document: [Deployment details on EKS](./docs/deployment-options/eks.md).

# Credits

- Djibrilla Amadou Kountche

## TODO

1. Ensure that this README contains the relevant information from the follwoing project:
  - https://github.com/5gmeta/platform-config
2. Re-draw the diagrams

# Conclusions and Perspectives

This document presented the 5GMETA Cloud Platfrom and its deployment approach.
