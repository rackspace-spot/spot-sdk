# Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse
import uuid 

from client import RackspaceSpotClient
from classes import *

# Convenience functions for common operations
def create_basic_cloudspace(
    client: RackspaceSpotClient,
    name: str,
    namespace: str,
    region: str = "us-east-iad-1",
    kubernetes_version: str = KubernetesVersion.V1_31_1.value
) -> CloudSpace:
    """Create a basic cloudspace with default settings."""
    cloudspace = CloudSpace(
        name=name,
        namespace=namespace,
        region=region,
        kubernetes_version=kubernetes_version
    )
    return client.create_cloudspace(cloudspace)


def create_basic_spot_pool(
    client: RackspaceSpotClient,
    namespace: str,
    cloudspace_name: str,
    server_class: str,
    desired_nodes: int,
    bid_price: str,
    name: Optional[str] = None
) -> SpotNodePool:
    """Create a basic spot node pool."""
    pool = SpotNodePool(
        name=name or str(uuid.uuid4()).lower(),
        namespace=namespace,
        cloudspace=cloudspace_name,
        server_class=server_class,
        desired=desired_nodes,
        bid_price=bid_price
    )
    return client.create_spot_node_pool(pool)


def create_basic_on_demand_pool(
    client: RackspaceSpotClient,
    namespace: str,
    cloudspace_name: str,
    server_class: str,
    desired_nodes: int,
    name: Optional[str] = None
) -> OnDemandNodePool:
    """Create a basic on-demand node pool."""
    pool = OnDemandNodePool(
        name=name or str(uuid.uuid4()).lower(),
        namespace=namespace,
        cloudspace=cloudspace_name,
        server_class=server_class,
        desired=desired_nodes
    )
    return client.create_on_demand_node_pool(pool)

# Additional utility functions
def wait_for_cloudspace_ready(
    client: RackspaceSpotClient,
    namespace: str,
    name: str,
    timeout: int = 1200,
    poll_interval: int = 60
) -> CloudSpace:
    """
    Wait for a cloudspace to be ready.
    
    Args:
        client: The RackspaceSpotClient instance
        namespace: The namespace of the cloudspace
        name: The name of the cloudspace
        timeout: Maximum time to wait in seconds
        poll_interval: Time between polls in seconds
    
    Returns:
        The ready cloudspace
    
    Raises:
        RackspaceSpotAPIError: If cloudspace doesn't become ready within timeout
    """
    import time
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            cloudspace = client.get_cloudspace(namespace, name)
            
            if cloudspace.phase == "Ready" and cloudspace.health == "Healthy":
                return cloudspace
            
            if cloudspace.phase == "Failed":
                raise RackspaceSpotAPIError(f"Cloudspace {name} failed to deploy")
            
            print(f"Cloudspace {name} status: {cloudspace.phase} (health: {cloudspace.health})")
            time.sleep(poll_interval)
            
        except RackspaceSpotAPIError as e:
            if e.status_code == 404:
                # Cloudspace not found yet, continue waiting
                time.sleep(poll_interval)
                continue
            else:
                raise
    
    raise RackspaceSpotAPIError(f"Cloudspace {name} did not become ready within {timeout} seconds")


def parse_args():
    """
    Parse command line arguments for the Rackspace Spot SDK operations.
    """
    parser = argparse.ArgumentParser(description="Running complete cycle of Rackspace Spot SDK operations")
    parser.add_argument('--refresh-token', required=True, help='Refresh token for OAuth authentication')
    parser.add_argument('--complete-scenario', action='store_true', help='Run the complete scenario')
    parser.add_argument('--full-deployment', action='store_true', help='Run the full deployment')
    return parser.parse_args()
