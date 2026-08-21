import json
from kubernetes import client, config

def collect_incident_context(namespace="default"):
    # Load cluster config from local environment
    config.load_kube_config()
    v1 = client.CoreV1Api()
    
    incident_report = {
        "namespace": namespace,
        "failed_pods": []
    }
    
    pods = v1.list_namespaced_pod(namespace)
    for pod in pods.items:
        # Check container statuses for crash or error indicators
        pod_status = pod.status
        is_failing = False
        reason = "Unknown"
        
        if pod_status.container_statuses:
            for cs in pod_status.container_statuses:
                if cs.state.waiting and cs.state.waiting.reason in ["CrashLoopBackOff", "ImagePullBackOff", "ErrImagePull"]:
                    is_failing = True
                    reason = cs.state.waiting.reason
                elif cs.state.terminated and cs.state.terminated.exit_code != 0:
                    is_failing = True
                    reason = f"TerminatedExitCode_{cs.state.terminated.exit_code}"

        if is_failing:
            pod_name = pod.metadata.name
            
            # Fetch container logs (recent crash trace)
            try:
                logs = v1.read_namespaced_pod_log(pod_name, namespace, tail_lines=15)
            except Exception as e:
                logs = f"Error retrieving logs: {str(e)}"
                
            # Fetch associated cluster events
            events = v1.list_namespaced_event(namespace, field_selector=f"involvedObject.name={pod_name}")
            event_messages = [f"[{e.type}] {e.reason}: {e.message}" for e in events.items]
            
            incident_report["failed_pods"].append({
                "pod_name": pod_name,
                "app_label": pod.metadata.labels.get("app", "unknown"),
                "detected_issue": reason,
                "logs": logs.strip(),
                "events": event_messages[-5:]  # Last 5 events
            })
            
    return incident_report

if __name__ == "__main__":
    report = collect_incident_context()
    print(json.dumps(report, indent=2))
