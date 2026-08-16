import json
import subprocess
import sys
from typing import List, Dict, Any

def run_gcloud_command(command: List[str]) -> Any:
    """Run a gcloud command and return parsed JSON output.

    Args:
        command: List of command parts (e.g., ['gcloud', 'projects', 'list', '--format=json'])

    Returns:
        Parsed JSON output as a Python object.

    Raises:
        RuntimeError: If gcloud is not installed, not authenticated, or command fails.
    """
    try:
        # Run the command and capture output
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True  # Raise CalledProcessError on non-zero exit
        )
        # Parse JSON output
        return json.loads(result.stdout)
    except FileNotFoundError:
        raise RuntimeError(
            "gcloud CLI not found. Please install Google Cloud SDK and ensure it's in your PATH."
        )
    except subprocess.CalledProcessError as e:
        # Check for common error messages
        if "Please login via:" in e.stderr or "authentication" in e.stderr.lower():
            raise RuntimeError(
                "gcloud CLI not authenticated. Please run 'gcloud auth login' and set a project."
            )
        elif "no valid credential" in e.stderr.lower():
            raise RuntimeError(
                "gcloud CLI not authenticated. Please run 'gcloud auth login' and set a project."
            )
        else:
            raise RuntimeError(f"gcloud command failed: {e.stderr}")
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse gcloud output as JSON: {e}")

def list_projects() -> List[Dict[str, Any]]:
    """List all accessible GCP projects.

    Returns:
        List of project dictionaries, each containing at least 'projectId'.
    """
    command = ["gcloud", "projects", "list", "--format=json"]
    projects = run_gcloud_command(command)
    # Extract relevant fields; we'll keep the whole object but we can filter if needed
    return projects

def scan_project_resources(project_id: str) -> List[Dict[str, Any]]:
    """Scan all resources in a GCP project using Cloud Asset API.

    Args:
        project_id: The GCP project ID.

    Returns:
        List of resource dictionaries with extracted fields:
        - assetType: The type of the resource (e.g., 'compute.googleapis.com/Instance')
        - name: The display name or full resource name
        - location: The location/zone/region of the resource (if available)
        - labels: The labels/tags associated with the resource (if available)
    """
    # Ensure the project ID is provided
    if not project_id:
        raise ValueError("Project ID must be provided")

    command = [
        "gcloud", "asset", "search-all-resources",
        f"--scope=projects/{project_id}",
        "--format=json"
    ]
    resources = run_gcloud_command(command)

    # Extract the fields we need
    extracted_resources = []
    for resource in resources:
        extracted = {
            "assetType": resource.get("assetType", ""),
            "name": resource.get("displayName") or resource.get("name", ""),
            "location": resource.get("location", ""),
            "labels": resource.get("labels", {})
        }
        extracted_resources.append(extracted)

    return extracted_resources