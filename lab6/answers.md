# CCS3308 – Lab 6: Kubernetes Fundamentals — Answers

## Task 1.2 — Control Plane / Worker Node Component Mapping

| Pod name pattern | Component | Control Plane or Worker |
|---|---|---|
| kube-apiserver-... | API Server | Control Plane |
| etcd-... | etcd | Control Plane |
| kube-scheduler-... | Scheduler | Control Plane |
| kube-controller-manager-... | Controller Manager | Control Plane |
| kube-proxy-... | kube-proxy | Worker Node |
| coredns-... | DNS add-on (extra, not in lecture's core list) | Control Plane |
| storage-provisioner | Minikube-specific add-on | N/A |

Note: kubelet does not appear as a pod — it is the agent on the worker node
that manages pods, so it is not itself scheduled as one.

## Checkpoint Q1
The control plane makes cluster-wide decisions and stores state (API Server,
etcd, Scheduler, Controller Manager). A worker node is where the actual
application containers run, managed locally by kubelet, kube-proxy, and the
container runtime, carrying out what the control plane decides.

## Checkpoint Q2
Yes, the IP changed after deleting and recreating the pod. Pods are
"ephemeral" — when a Pod is deleted and recreated, Kubernetes treats it as a
brand-new object and assigns a new IP from the network layer, rather than
preserving the old identity.

## Checkpoint Q3
Using the control-loop model:
1. Desired State = 3 replicas (stored via the Deployment spec in etcd)
2. The ReplicaSet controller continuously watches the actual state
3. Deleting a pod dropped Actual State to 2
4. Gap Detected: controller compares 3 desired vs 2 actual
5. Reconcile: the Scheduler places a new Pod, kubelet pulls the image and
   starts the container until actual state = desired state again

## Checkpoint Q4
Once each tier (frontend, API, cache, database) is its own independent
Deployment/StatefulSet with its own selector, scaling one tier only affects
that tier's Pods, since each has a separate desired-state spec — the frontend
can be scaled without touching the database at all.

## Checkpoint Q5
Port-forward tunnels to one specific Pod — if that Pod dies, the tunnel
breaks. A Service routes by label selector, not fixed IP, so as Pods are
replaced (getting new IPs), the Service automatically finds whichever Pods
currently match app: frontend. This gives a stable access point despite Pods
being ephemeral.

## Checkpoint Q6
Docker Compose has no built-in rolling update mechanism — restarting
containers typically causes downtime with no revision history to roll back
to. Kubernetes tracks rollout history and replaces Pods gradually (old ones
stay up until new ones are healthy), giving zero-downtime updates and a
one-command rollback that Compose cannot do natively.

## Checkpoint Q7
Frontend and API are stateless — any replica is interchangeable, Pods get
random names, no need to preserve identity or storage across restarts, so a
Deployment works fine. The database is stateful — it needs a stable name
(postgres-0), stable storage reattached to the same Pod identity after
restart (via volumeClaimTemplates), and ordered creation/deletion — which is
exactly what a StatefulSet guarantees and a Deployment does not.

## Checkpoint Q8
No. A plain Deployment has no PersistentVolumeClaim tying storage to a
stable identity — its Pods use ephemeral storage by default, so deleting and
recreating the Pod would wipe the database data. The PVC in the StatefulSet
is what makes the data survive Pod deletion.

## Checkpoint Q9

The broken pod showed status `ErrImagePull`, which quickly transitioned to
`ImagePullBackOff` after Kubernetes retried and failed again. This status
is not one of the four explicitly listed in the lecture's Pod Status table
(Running / Pending / CrashLoopBackOff / OOMKilled) — it's a related but
distinct status.

The key difference is where in the pod lifecycle the failure happens:
- CrashLoopBackOff means the container image was pulled successfully and
  the container did start, but it kept crashing after starting, so
  Kubernetes keeps restarting it with an increasing back-off delay.
- ImagePullBackOff means Kubernetes never even got that far — it couldn't
  pull the image from the registry at all (because the tag
  nginx:definitely-not-a-real-tag doesn't exist), so no container ever
  started. The "BackOff" part follows the same retry pattern, but the
  failure point is earlier in the pipeline: image retrieval, not
  container execution.

So it's a sibling status to CrashLoopBackOff, following the same
back-off/retry pattern, but representing a different class of problem —
an image-availability issue rather than an application-runtime issue.
