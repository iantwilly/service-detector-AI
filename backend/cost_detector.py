from typing import List, Dict, Any
from collections import defaultdict

def analyze_cost(resources: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze GCP resources for cost insights.

    Args:
        resources: List of resource dictionaries from scan_project_resources.

    Returns:
        A dictionary containing cost analysis results.
    """
    if not resources:
        return {
            "total_resources": 0,
            "by_service": {},
            "potential_savings_opportunities": [],
            "summary": "No resources found in the project."
        }

    # Group resources by assetType (service)
    service_count = defaultdict(int)
    service_resources = defaultdict(list)
    for resource in resources:
        asset_type = resource.get("assetType", "unknown")
        service_count[asset_type] += 1
        service_resources[asset_type].append(resource)

    # Convert to regular dict for JSON serialization
    by_service = dict(service_count)

    # Identify potential savings opportunities (basic heuristics)
    opportunities = []

    # Example: Look for idle compute instances (we don't have utilization data, so just note)
    compute_instances = service_resources.get("compute.googleapis.com/Instance", [])
    if compute_instances:
        opportunities.append({
            "type": "Compute Engine Instances",
            "count": len(compute_instances),
            "suggestion": "Review utilization of compute instances. Consider stopping or right-sizing idle instances.",
            "potential_savings": "Medium to High"
        })

    # Example: Look for storage buckets
    storage_buckets = service_resources.get("storage.googleapis.com/Bucket", [])
    if storage_buckets:
        opportunities.append({
            "type": "Cloud Storage Buckets",
            "count": len(storage_buckets),
            "suggestion": "Review storage buckets for outdated or duplicate data. Consider lifecycle policies.",
            "potential_savings": "Low to Medium"
        })

    # Example: Look for reserved instances or committed use discounts (we don't have that data, so skip)
    # We could look for specific labels that indicate environment (e.g., env: dev) and suggest turning off after hours.

    # Summary
    total_resources = len(resources)
    summary = f"Found {total_resources} resources across {len(by_service)} services."

    return {
        "total_resources": total_resources,
        "by_service": by_service,
        "potential_savings_opportunities": opportunities,
        "summary": summary
    }