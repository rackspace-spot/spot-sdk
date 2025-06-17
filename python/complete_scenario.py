# Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import time

from client import RackspaceSpotClient
from classes import RackspaceSpotAPIError
from utils import *


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
            namespace = orgs[0].namespace
            print(f"Using namespace: {namespace}")
            
            time.sleep(5)

            # List available regions
            regions = client.list_regions()
            print(f"Available regions: {[r.name for r in regions]}")
            
            time.sleep(5)

            # List server classes
            server_classes = client.list_server_classes()
            print(f"Available server classes: {[sc.name for sc in server_classes[:5]]}")
            
            time.sleep(5)

            # Get price history for a server class
            try:
                price_history = client.get_price_history("gp.vs1.medium-iad")
                print(f"Price history entries: {len(price_history.history)}")
            except Exception as e:
                print(f"Could not get price history: {e}")

            time.sleep(5)

            time.sleep(5)

            # Create a cloudspace
            cloudspace = create_basic_cloudspace(
                client=client,
                name="test-generate-cloudspace-from-sdk",
                namespace=namespace,
                region="us-east-iad-1"
            )
            print(f"Creation requested submitted for cloudspace: {cloudspace.name}")
            
            print("Waiting for cloudspace to be ready for couple of minutes (upto 3 minutes )...")

            time.sleep(3*60)

            # Wait for cloudspace to be ready
            cloudspace = wait_for_cloudspace_ready(
                client=client,
                namespace=namespace,
                name=cloudspace.name
            )

            print(f"Clouspace - {cloudspace.name} is now ready to use.")

            # Create a spot node pool
            spot_pool = create_basic_spot_pool(
                client=client,
                namespace=namespace,
                cloudspace_name=cloudspace.name,
                server_class="gp.vs1.medium-iad",
                desired_nodes=2,
                bid_price="0.5"
            )
            print(f"Creation requested submitted for spot node pool: {spot_pool.name}")
            
            # Create a ondemand node pool
            ondemand_pool = create_basic_on_demand_pool(
                client=client,
                namespace=namespace,
                cloudspace_name=cloudspace.name,
                server_class="gp.vs1.medium-iad",
                desired_nodes=2
            )
            print(f"Creation requested submitted for ondemand node pool: {ondemand_pool.name}")
            
            print("Waiting for spot pool and ondemand pool to be ready for some minutes ( upto 20 minutes )...")

            time.sleep(20*60)

            # List cloudspaces
            print("Listing cloudspaces in namespace...")

            cloudspaces = client.list_cloudspaces(namespace)
            print(f"Cloudspaces in namespace: {[cs.name for cs in cloudspaces]}")

            time.sleep(5)

            # List spot pools
            print("Listing spot pools in namespace...")

            spot_pools_list = client.list_spot_node_pools(namespace)
            print(f"Spot Pools in namespace: {[cs.name for cs in spot_pools_list]}")

            time.sleep(5)

            # List ondemand pools
            print("Listing ondemand pools in namespace...")

            ondemand_pools_list = client.list_on_demand_node_pools(namespace)
            print(f"Ondemand Pools in namespace: {[cs.name for cs in ondemand_pools_list]}")

            time.sleep(5)

            print("Deleting resources in cluster")
            # Delete spot pools.
            print("Deleting spot pools...")
            client.delete_spot_node_pool(namespace, spot_pool.name)
            
            time.sleep(60)
            # Delete on-demand pools
            print("Deleting on-demand pools...")
            client.delete_on_demand_node_pool(namespace, ondemand_pool.name)
            
            time.sleep(60)

            # Delete cloudspaces
            print("Deleting cloudspace...")
            client.delete_cloudspace(namespace, cloudspace.name)
            
    except RackspaceSpotAPIError as e:
        print(f"API Error: {e.message}")
        if e.status_code:
            print(f"Status Code: {e.status_code}")
    except Exception as e:
        print(f"Error: {e}")