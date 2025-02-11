# Overview
5GMETA metering tools are based on:
* Prometheus
* Grafana
* alert-manager
* Loki

## Prometheus
Prometheus is the default tool to aggregate numerical metrics from several services and instances both from MEC and cloud part from 5GMETA infrastructure. This software will monitor CPU and memory comsumption from all containers as well as input/output traffic from each one of them
## Loki
We are using Loki to monitor logs from containers deployed into MEC infrastructure. Loki gets output logs from all pods and pushes them to the monitoring infrastructure.

## Grafana
Grafana is the main entry point to show metrics infromation from Cloud and MEC infrastructure.
Grafana is the responsible software to show graphical representation and filtering capabilities from all logs that are captured by Prometheus and Loki. That representation and filtering task is made by using the default or customized panels from Grafana.
This way an infrastructure administrator can manage all information relative to performance and running services from 5GMETA infrastructure.
That means that an infrastructure administrator can select CPU, memory, bandwith or whatever numerical available metric from Prometheus and show it grouped by namespace, container or total from each container deployed both in each one of the MECs or from Cloud infrastructure and view it along the time.
In the same way, Grafana can show Loki metrics that correspond to output logs from containers and agrupate them in namespaces to show the amount of data logs produced by each group of deployments into the MEC.

## Alert-manager

Alert-manager is used to monitor alerts in both systems, Cloud and MECs from infrastructure.

# Prerequisites

Monitoring system can be deployed in both parts from 5GMETA infrastructure, Cloud and every MEC. Monitoring system deployment is based on Helm-charts, so helm client and kubectl are needed.

## MEC

Kubectl and helm are automatically installed on MEC deploying, so there is no task to be done.

## Cloud

On the other side, Cloud access is made from remote computer, so computers that are going to be used to deploy Cloud infrastructure need to install Helm and Kubectl (version 1.26.0) and be granted with kubernetes access to aws infrastructure by aws console or web interface.

## Helm installation
[https://helm.sh/docs/intro/install/](https://helm.sh/docs/intro/install/)

## Kubectl installation

[kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) version 1.26.0.
    * curl -LO https://dl.k8s.io/release/v1.26.0/bin/linux/amd64/kubectl
    * sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Deployment

## Installation and deployment monitoring infrastructure in a MEC

Default installation is based on standard deployment from MEC. That deployment uses ansible based on configuration from https://github.com/5gmeta/orchestrator/blob/main/deploy/EdgeDeployment.yaml and can be installed by executing:

```
ansible-playbook EdgeDeployment.yaml
```

If you want to make some modification about ports or versions from Prometheus, Grafana or Loki you can modify yaml descriptor and install step by step by executing:

```
ansible-playbook playbook.yml --step --start-at-task="Add prometheus-community helm repo"
ansible-playbook playbook.yml --step --start-at-task="Deploy kube-prometheus-stack"
ansible-playbook playbook.yml --step --start-at-task="Expose grafana's dashboard"
ansible-playbook playbook.yml --step --start-at-task="Expose prometheus's dashboard"
ansible-playbook playbook.yml --step --start-at-task="Expose alertmanager's dashboard"
ansible-playbook playbook.yml --step --start-at-task="Add grafana repo"
ansible-playbook playbook.yml --step --start-at-task="Deploy grafana/loki"
ansible-playbook playbook.yml --step --start-at-task="Expose grafana's with loki support dashboard"
ansible-playbook playbook.yml --step --start-at-task="Add kuberhealthy helm repo"
ansible-playbook playbook.yml --step --start-at-task="Deploy kuberhealthy"
```

These commands will deploy Prometheus, Grafana, Loki and alert-manager into MEC infrastructure to monitor both, the performance of the 5GMETA infrastructure deployed in the MEC, the performance of the kubernetes system deployed in the MEC and the performance of the anonymization containers deployed on-demand in the MEC infrastructure from 5GMETA.

### Access to monitoring tools
Prometheus, Grafana and Loki are available at:

* Grafana http://your_mec_ip:3000
* Prometheus http://your_mec_ip:9090
* Alert-manager http://your_mec_ip:9093

Access to all elements doesn't need any kind of authentication.

## Cloud monitoring installing process

### Installing the Kubernetes Metrics Server
````
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml
kubectl get deployment metrics-server -n kube-system
kubectl get --raw /metrics
````

### Deploying Kubernetes Dashboard
````
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.4.0/aio/deploy/recommended.yaml

cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
EOF
cat <<EOF | kubectl apply -f -
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
EOF

kubectl apply -f eks-admin-service-account.yaml
````

To connect to the Kubernetes dashboard, get the token and expose the service:
````
kubectl -n kubernetes-dashboard get secret $(kubectl -n kubernetes-dashboard get sa/admin-user -o jsonpath="{.secrets[0].name}") -o go-template="{{.data.token | base64decode}}"

kubectl proxy
````

To access the dashboard endpoint, open the following link with a web browser:  [http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#!/login](http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#!/login) and paste the token got in the first command.

The service type of the dashboard can be switched to NodePort so that the dashboard is exposed permanently.

### Deploying Kube-Prometheus stack
The following helm installs the  [kube-prometheus stack](https://github.com/prometheus-operator/kube-prometheus), a collection of Kubernetes manifests,  [Grafana](http://grafana.com/)  dashboards, and  [Prometheus rules](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules/)  combined with documentation and scripts to provide easy to operate end-to-end Kubernetes cluster monitoring with  [Prometheus](https://prometheus.io/)  using the  [Prometheus Operator](https://github.com/prometheus-operator/prometheus-operator).

````
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install -n monitoring --create-namespace -f values.yaml prometheus-stack prometheus-community/kube-prometheus-stack --version 46.0
````

The values file used in the helm can be found in the following 5GMETA repository: [values.yaml](https://github.com/5gmeta/platform-config/blob/main/src/kube-prometheus-stack/values.yaml)

````
prometheus:
  service:
    type: NodePort
  prometheusSpec:
    storageSpec:
      volumeClaimTemplate:
        spec:
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 20Gi
    retention: 30d
  enabled: true
  prometheusSpec:
    additionalScrapeConfigs: |
      - job_name: kafka
        static_configs:
          - targets:
            - kafkacluster-cp-kafka-connect.kafka.svc.cluster.local:5556
            - kafkacluster-cp-kafka-rest.kafka.svc.cluster.local:5556
            - kafkacluster-cp-ksql-server.kafka.svc.cluster.local:5556
            - kafkacluster-cp-schema-registry.kafka.svc.cluster.local:5556
            - kafkacluster-cp-zookeeper.kafka.svc.cluster.local:5556
            - kafkacluster-cp-kafka.kafka.svc.cluster.local:5556

alertmanager:
  service:
    type: NodePort
  alertmanagerSpec:
    storage:
      volumeClaimTemplate:
        spec:
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 5Gi

grafana:
  service:
    type: NodePort
  persistence:
    enabled: true

````

To expose temporally the ports of Prometheus and Grafana services:
````
PROMETHEUS=$(kubectl get pod -n monitoring -l app.kubernetes.io/name=prometheus -o jsonpath='{.items[0].metadata.name}')
GRAFANA=$(kubectl get pod -n monitoring -l app.kubernetes.io/name=grafana -o jsonpath='{.items[0].metadata.name}')
kubectl port-forward -n monitoring $PROMETHEUS 9090 &
kubectl port-forward -n monitoring $GRAFANA 3000 &
````
If you want to expose them constantly, change the service type to NodePort.

Installation and deployment
```
helm install -n monitoring --create-namespace -f values.yaml prometheus-stack prometheus-community/kube-prometheus-stack --version 46.0
```
### Access to monitoring tools
Prometheus, Grafana and Loki are available at:
* Grafana http://5gmeta_cloud_ip:31137
* Prometheus http://5gmeta_cloud_ip:30090
* Alert-manager http://5gmeta_cloud_ip:30903

Access to Prometheus and Alert-manger doesn't need any kind of authentication.
Grafana access credentials are: admin/prom-operator

# Monitoring and Metering Dashboards
We offer a collection of JSON files that can be imported into Grafana instances, whether in the Cloud or MEC environments. These dashboards comprise visualization panels designed to extract crucial insights into the status of resources across Cloud and MEC clusters. Additionally, an extra dashboard is included for Cloud environments, specifically tailored to extract data flow volumes between producers and consumers.

A full description of each dashboard can be found [here.](./dashboards/README.md)

To import a dashboard using the provided JSON file, navigate to the "Dashboard" panel in Grafana. Click on the "New" dropdown menu and select "Import". From there, you can upload the JSON file. If you encounter errors in the connection with Prometheus, please ensure that the dashboard is configured to use the correct data source, which should be the main Prometheus instance.

![Import Grafana](./dashboards/images/import_grafana.jpg)

# Authors

* Felipe Mogollón ([fmogollon@vicomtech.org](mailto:fmogollon@vicomtech.org))
* Juan Diego Ortega([jdortega@vicomtech.org](mailto:jdortega@vicomtech.org))


# License

Copyright : Copyright 2022 VICOMTECH

License : EUPL 1.2 ([https://eupl.eu/1.2/en/](https://eupl.eu/1.2/en/))

The European Union Public Licence (EUPL) is a copyleft free/open source software license created on the initiative of and approved by the European Commission in 23 official languages of the European Union.

Licensed under the EUPL License, Version 1.2 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at [https://eupl.eu/1.2/en/](https://eupl.eu/1.2/en/)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
