import sys
import os

SCENARIOS = {
    "oom": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: analytics-worker
  namespace: default
  labels:
    app: analytics-worker
spec:
  replicas: 1
  selector:
    matchLabels:
      app: analytics-worker
  template:
    metadata:
      labels:
        app: analytics-worker
    spec:
      containers:
      - name: worker
        image: alpine:latest
        command: ["/bin/sh", "-c"]
        args: ["echo 'Consuming memory...'; tail /dev/zero"]
        resources:
          limits:
            memory: "16Mi"
            cpu: "50m"
""",
    "bad_probe": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-processor
  namespace: default
  labels:
    app: order-processor
spec:
  replicas: 1
  selector:
    matchLabels:
      app: order-processor
  template:
    metadata:
      labels:
        app: order-processor
    spec:
      containers:
      - name: processor
        image: alpine:latest
        command: ["/bin/sh", "-c"]
        args: ["echo 'Running worker...'; sleep 3600"]
        livenessProbe:
          httpGet:
            path: /non-existent-endpoint
            port: 9999
          initialDelaySeconds: 2
          periodSeconds: 3
""",
    "bad_image": """apiVersion: apps/v1
kind: Deployment
metadata:
  name: inventory-service
  namespace: default
  labels:
    app: inventory-service
spec:
  replicas: 1
  selector:
    matchLabels:
      app: inventory-service
  template:
    metadata:
      labels:
        app: inventory-service
    spec:
      containers:
      - name: inventory
        image: non-existent-registry.internal/app:v9.9.9
"""
}

def inject(scenario_name):
    if scenario_name not in SCENARIOS:
        print(f"Unknown scenario '{scenario_name}'. Options: {list(SCENARIOS.keys())}")
        return
    manifest = SCENARIOS[scenario_name]
    with open("chaos_manifest.yaml", "w") as f:
        f.write(manifest)
    os.system("kubectl apply -f chaos_manifest.yaml")
    print(f"💥 Injected chaos scenario: '{scenario_name}'")

if __name__ == "__main__":
    choice = sys.argv[1] if len(sys.argv) > 1 else "oom"
    inject(choice)
