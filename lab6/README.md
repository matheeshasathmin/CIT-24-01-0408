# Lab 6 — Kubernetes Fundamentals with Minikube

## Overview
A multi-tier application (frontend, API, cache, database) deployed on a
local Minikube cluster, demonstrating Kubernetes core concepts: Pods,
Deployments, Services, StatefulSets, self-healing, scaling, rolling
updates/rollbacks, and persistent storage.

## Architecture
- Frontend: nginx:alpine — Deployment (3 replicas, scaled to 2) + NodePort Service
- API: kennethreitz/httpbin — Deployment (2 replicas) + ClusterIP Service
- Cache: redis:7-alpine — Deployment (1 replica) + ClusterIP Service
- Database: postgres:16-alpine — StatefulSet (1 replica) + PVC (1Gi) + headless Service

## How to Run
1. Start Minikube:
   minikube start --driver=docker
2. Apply all manifests:
   kubectl apply -f k8s/
3. Verify everything is running:
   kubectl get all
4. Access the frontend:
   minikube service frontend --url

## Folder Structure
- k8s/         — all Kubernetes YAML manifests
- screenshots/ — evidence for each numbered task (1.1 through 10.1)
- answers.md   — written responses to all 9 checkpoint questions
- README.md    — this file

## Key Concepts Demonstrated
- Self-healing: deleting a pod in a Deployment triggers automatic replacement
- Scaling: kubectl scale deployment frontend --replicas=5/2
- Rolling update + rollback: kubectl set image / kubectl rollout undo
- Persistence: StatefulSet + PVC retains data across pod deletion/recreation
- Troubleshooting: ImagePullBackOff diagnosed via kubectl describe

## Cleanup
kubectl delete -f k8s/
minikube stop
