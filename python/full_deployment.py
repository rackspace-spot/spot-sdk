# Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json

from client import RackspaceSpotClient
from classes import RackspaceSpotAPIError
from manager import RackspaceSpotManager
from dynamic_pools_config import spot_pools_config, on_demand_pools_config

# Example of complete environment setup
def example_full_deployment(refresh_token: str):
    """
    Example showing how to run a full deployment using the Rackspace Spot SDK Script.
    This includes create environment, get environment status of all resources, and clean up environment.
    """

    print("Starting full deployment example...")

    client = RackspaceSpotClient(refresh_token=refresh_token)
    manager = RackspaceSpotManager(client)
    
    # Get namespace
    orgs = client.list_organizations()
    namespace = orgs[0].namespace
    
    # Obtain number and config of pools needed
    spot_pools = spot_pools_config
    
    on_demand_pools = on_demand_pools_config
    
    try:
        # Create environment
        environment = manager.create_environment(
            cloudspace_name="full-deployment-sdk-cloudspace",
            namespace=namespace,
            region="us-east-iad-1",
            spot_pools=spot_pools,
            on_demand_pools=on_demand_pools,
        )

        print("Environment created successfully!")
        print(f"Cloudspace: {environment['cloudspace'].name}")
        print(f"Spot pools: {len(environment['spot_pools'])}")
        print(f"On-demand pools: {len(environment['on_demand_pools'])}")

        # Get environment status
        status = manager.get_environment_status(namespace)
        print("\nEnvironment Status:")
        print(json.dumps(status, indent=2, default=str))
        
        # Cleanup environment
        print("\nCleaning up environment...")
        status = manager.cleanup_environment(namespace, environment)
        if status:
            print("Environment cleaned up successfully.")
        else:
            print("Failed to clean up environment.")
            
    except RackspaceSpotAPIError as e:
        print(f"Deployment failed: {e.message}")

