# CP-Kafka Helm Chart

This chart bootstraps a cluster of Confluent Kafka

## Prerequisites

* Kubernetes 1.9.2+
* Helm 2.8.2+


### Installed Components

You can use `helm status <release name>` to view all of the installed components.

For example:

```console
$ helm status garish-cat
NAMESPACE: default
STATUS: DEPLOYED
```

There are
1. A [Confluent Zookeeper Ensemble](https://github.com/confluentinc/cp-helm-charts/tree/master/charts/cp-zookeeper) created by cp-zookeeper chart.
1. A [StatefulSet](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) `boiling-heron-cp-kafka` which contains 3 Kafka [Pods](https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/): `boiling-heron-cp-kafka-<0|1|2>`. Each Pod has a container running a Kafka Broker and an optional sidecar JMX Exporter Container.
1. A [Service](https://kubernetes.io/docs/concepts/services-networking/service/) `boiling-heron-cp-kafka` for clients to connect to Kafka.
1. A [Headless Service](https://kubernetes.io/docs/concepts/services-networking/service/#headless-services) `boiling-heron-cp-kafka-headless` to control the network domain for the Kafka processes.
1. A group(N = number of brokers) of [NodePort Service](https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport) `boiling-heron-cp-kafka-${i}-external` to allow access to Kafka Cluster from outside.
1. A [ConfigMap](https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/) which contains configuration for Prometheus JMX Exporter.

## Configuration

You can specify each parameter using the `--set key=value[,key=value]` argument to `helm install`.

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

```console
helm install --name my-kafka -f my-values.yaml ./cp-kafka
```

> **Tip**: A default [values.yaml](values.yaml) is provided

### Kafka Cluster

The configuration parameters in this section control the resources requested and utilized by the cp-kafka chart.

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `brokers` | The number of Broker servers. | `3` |

### Image

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `image` | Docker Image of Confluent Kafka. | `confluentinc/cp-enterprise-kafka` |
| `imageTag` | Docker Image Tag of Confluent Kafka. | `6.1.0` |
| `imagePullPolicy` | Docker Image Tag of Confluent Kafka. | `IfNotPresent` |
| `imagePullSecrets` | Secrets to be used for private registries. | see [values.yaml](values.yaml) for details |

### StatefulSet Configurations

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `podManagementPolicy` | The Kafka StatefulSet Pod Management Policy: `Parallel` or `OrderedReady`. | `OrderedReady` |
| `updateStrategy` | The Kafka StatefulSet update strategy: `RollingUpdate` or `OnDelete`. | `RollingUpdate` |

### Confluent Kafka Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `configurationOverrides` | Kafka [configuration](https://kafka.apache.org/documentation/#brokerconfigs) overrides in the dictionary format | `{}` |
| `customEnv` | Custom environmental variables | `{}` |

### Persistence

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `persistence.enabled` | Whether to create a PVC. If `false`, an `emptyDir` on the host will be used. | `true` |
| `persistence.size` | Size for log dir, where Kafka will store log data. | `5Gi` |
| `persistence.storageClass` | Valid options: `nil`, `"-"`, or storage class name. | `nil` |
| `persistence.disksPerBroker` | The amount of disks that will be attached per instance of Kafka broker. | 1 |

### Kafka JVM Heap Options

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `heapOptions` | The JVM Heap Options for Kafka | `"-Xms512M -Xmx512M"` |

### Resources

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `resources.requests.cpu` | The amount of CPU to request. | see [values.yaml](values.yaml) for details |
| `resources.requests.memory` | The amount of memory to request. | see [values.yaml](values.yaml) for details |
| `resources.limits.cpu` | The upper limit CPU usage for a Kafka Pod. | see [values.yaml](values.yaml) for details |
| `resources.limits.memory` | The upper limit memory usage for a Kafka Pod. | see [values.yaml](values.yaml) for details |

### Annotations

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `podAnnotations` | Map of custom annotations to attach to the pod spec. | `{}` |

### JMX Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `jmx.port` | The jmx port which JMX style metrics are exposed. | `5555` |

### Prometheus JMX Exporter Configuration

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `prometheus.jmx.enabled` | Whether or not to install Prometheus JMX Exporter as a sidecar container and expose JMX metrics to Prometheus. | `true` |
| `prometheus.jmx.image` | Docker Image for Prometheus JMX Exporter container. | `solsson/kafka-prometheus-jmx-exporter@sha256` |
| `prometheus.jmx.imageTag` | Docker Image Tag for Prometheus JMX Exporter container. | `6f82e2b0464f50da8104acd7363fb9b995001ddff77d248379f8788e78946143` |
| `prometheus.jmx.imagePullPolicy` | Docker Image Pull Policy for Prometheus JMX Exporter container. | `IfNotPresent` |
| `prometheus.jmx.port` | JMX Exporter Port which exposes metrics in Prometheus format for scraping. | `5556` |
| `prometheus.jmx.resources` | JMX Exporter resources configuration. | see [values.yaml](values.yaml) for details |

### External Access

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `nodeport.enabled` | Whether or not to allow access to kafka cluster from outside k8s through NodePort. | `false` |
| `nodeport.servicePort` | The Port broker will advertise to external producers and consumers.  | `19092` |
| `nodeport.firstListenerPort` | The first NodePort that Kafka Broker will use for advertising to external producers and consumers. For each broker, advertise.listeners port for external will be set to `31090 + {index of broker pod}`. | `31090` |

### Deployment Topology

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `nodeSelector` | Dictionary containing key-value-pairs to match labels on nodes. When defined pods will only be scheduled on nodes, that have each of the indicated key-value pairs as labels. Further information can be found in the [Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/) | `{}`
| `tolerations`| Array containing taint references. When defined, pods can run on nodes, which would otherwise deny scheduling. Further information can be found in the [Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration/) | `{}`

## Dependencies

### Zookeeper

| Parameter | Description | Default |
| --------- | ----------- | ------- |
| `cp-zookeeper.enabled` | Whether or not to install cp-zookeeper chart alongside cp-kafka chart | `true` |
| `cp-zookeeper.persistence.enabled` | Whether to create a PVC. If `false`, an `emptyDir` on the host will be used. | `true` |
| `cp-zookeeper.persistence.dataDirSize` | Size for Data dir, where ZooKeeper will store the in-memory database snapshots. This will overwrite corresponding value in cp-zookeeper chart's value.yaml | `5Gi` |
| `cp-zookeeper.persistence.dataLogDirSize` | Size for data log dir, which is a dedicated log device to be used, and helps avoid competition between logging and snapshots. This will overwrite corresponding value in cp-zookeeper chart's value.yaml. | `5Gi` |
| `cp-zookeeper.url` | Service name of Zookeeper cluster (Not needed if zookeeper.enabled is set to true). | `""` |
| `cp-zookeeper.clientPort` | Port of Zookeeper Cluster | `2181` |
