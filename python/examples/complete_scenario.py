# Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import uuid
import time

from rackspace_spot_sdk.client import RackspaceSpotClient
from rackspace_spot_sdk.classes import RackspaceSpotAPIError, CloudSpace, SpotNodePool, OnDemandNodePool, KubernetesVersion


def example_complete_scenario(refresh_token: str):
    """
    Example showing how to run a complete scenario using the Rackspace Spot SDK Script.
    This includes creating a cloudspace, spot node pools, and on-demand node pools,
    and performing various operations like listing resources and deleting them.
    """
    print("Starting complete scenario example...")

    client = RackspaceSpotClient(refresh_token=refresh_token)
    
    try:
        # List organizations to get namespace
        orgs = client.list_organizations()
        if orgs:
            namespace = client.namespace
            if not namespace:
                raise RackspaceSpotAPIError("No namespace found in organizations for given refresh token. Please check whether refresh token belongs to valid organization.")

            # List available regions
            regions = client.list_regions()
            print(f"Available regions: {[r.name for r in regions]}")
            
            # List server classes
            server_classes = client.list_server_classes()
            print(f"Available server classes: {[sc.name for sc in server_classes[:5]]}")
            
            # Get price history for a server class
            try:
                price_history = client.get_price_history("gp.vs1.medium-iad")
                print(f"Price history entries: {len(price_history.history)}")
            except Exception as e:
                print(f"Could not get price history: {e}")

            print(f"Sending request for cloudspace creation with name: test-generate-cloudspace-from-sdk")

            # Create a cloudspace - assuming that cloudspace with same name doesn't exist already in your namespace.
            # If it exists, it will throw an error and would stop its execution.

            cloudspace_object = CloudSpace(
                name="test-generate-cloudspace-from-sdk",
                namespace=namespace,
                region="us-east-iad-1",
                kubernetes_version=KubernetesVersion.V1_31_1.value
            )

            cloudspace = client.create_cloudspace(cloudspace_object)

            print(f"Creation requested submitted for cloudspace: {cloudspace.name}")
            
            # Create a spot node pool
            pool_obj = SpotNodePool(
                name=str(uuid.uuid4()).lower(),
                namespace=namespace,
                cloudspace=cloudspace.name,
                server_class="gp.vs1.medium-iad",
                desired=2,
                bid_price="0.5" # update as per current market price
            )
            spot_pool = client.create_spot_node_pool(pool_obj)
            
            print(f"Creation requested submitted for spot node pool: {spot_pool.name}")
            
            # Create a ondemand node pool
            pool_obj = OnDemandNodePool(
                name=str(uuid.uuid4()).lower(),
                namespace=namespace,
                cloudspace=cloudspace.name,
                server_class="gp.vs1.medium-iad",
                desired=2
            )
            ondemand_pool = client.create_on_demand_node_pool(pool_obj)
            
            print(f"Creation requested submitted for ondemand node pool: {ondemand_pool.name}")
            print("Waiting for resources - spot pool and ondemand pool to be ready ... (upto 20 minutes)")
            time.sleep(20*60)

            # List cloudspaces
            print("Listing cloudspaces in namespace...")

            cloudspaces = client.list_cloudspaces(namespace)
            print(f"Cloudspaces in namespace: {[cs.name for cs in cloudspaces]}")

            # List spot pools
            print("Listing spot pools in namespace...")

            spot_pools_list = client.list_spot_node_pools(namespace)
            print(f"Spot Pools in namespace: {[cs.name for cs in spot_pools_list]}")

            # List ondemand pools
            print("Listing ondemand pools in namespace...")

            ondemand_pools_list = client.list_on_demand_node_pools(namespace)
            print(f"Ondemand Pools in namespace: {[cs.name for cs in ondemand_pools_list]}")

            print("Deleting resources in cluster")
            # Delete spot pools.
            print("Deleting spot pools...")
            client.delete_spot_node_pool(namespace, spot_pool.name)
            
            # Delete on-demand pools
            print("Deleting on-demand pools...")
            client.delete_on_demand_node_pool(namespace, ondemand_pool.name)
            
            # Delete cloudspaces
            print("Deleting cloudspace...")
            client.delete_cloudspace(namespace, cloudspace.name)
            
    except RackspaceSpotAPIError as e:
        print(f"API Error: {e.message}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
    except Exception as e:
        print(f"Error: {e}")