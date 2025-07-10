# Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import time
from typing import Dict, List, Optional, Any

from rackspace_spot_sdk.client import RackspaceSpotClient
from rackspace_spot_sdk.classes import KubernetesVersion, CloudSpace, SpotNodePool, OnDemandNodePool

class RackspaceSpotManager:
    """
    Higher-level manager class for common Rackspace Spot operations.
    
    This class provides simplified methods for managing entire environments
    and common workflows.
    """
    
    def __init__(self, client: RackspaceSpotClient):
        """Initialize with a RackspaceSpotClient."""
        self.client = client
    
    def create_environment(
        self,
        cloudspace_name: str,
        namespace: str,
        region: str = "us-east-iad-1",
        kubernetes_version: str = KubernetesVersion.V1_31_1.value,
        spot_pools: Optional[List[Dict[str, Any]]] = None,
        on_demand_pools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create a complete environment with cloudspace and node pools.
        
        Args:
            cloudspace_name: Base name for resource cloudspace
            namespace: Namespace to create resources in
            region: Region to deploy to
            kubernetes_version: Kubernetes version to use
            spot_pools: List of spot pool configurations
            on_demand_pools: List of on-demand pool configurations
        
        Returns:
            Dictionary containing created resources
        """
        # Create cloudspace

        cloudspace = None

        result = {
            'cloudspace': cloudspace,
            'spot_pools': [],
            'on_demand_pools': []
        }

        try:
            cloudspace = self.client.get_cloudspace(namespace, cloudspace_name)
        except Exception as e:
            cloudspace = None
        if cloudspace:
            print(f"Cloudspace {cloudspace_name} already exists in namespace {namespace}.")
            print("Leveraging existing cloudspace for spot and ondemand resource pools creation.")
        else:
            cloudspace_object = CloudSpace(
                name=cloudspace_name,
                namespace=namespace,
                region=region,
                kubernetes_version=kubernetes_version
            )
            cloudspace = self.client.create_cloudspace(cloudspace_object)

            print(f"Creating Cloudspace: {cloudspace.name} in namespace {namespace} with region {region} and kubernetes version {kubernetes_version}.")

        result['cloudspace'] = cloudspace

        # Create spot pools
        if spot_pools:
            for _, pool_config in enumerate(spot_pools):
                pool_obj = SpotNodePool(
                    namespace=namespace,
                    cloudspace=cloudspace_name,
                    **pool_config
                )
                pool = self.client.create_spot_node_pool(pool_obj)
                result['spot_pools'].append(pool)
        
        # Create on-demand pools
        if on_demand_pools:
            for _, pool_config in enumerate(on_demand_pools):
                pool_obj = OnDemandNodePool(
                    namespace=namespace,
                    cloudspace=cloudspace_name,
                    **pool_config
                )
                pool = self.client.create_on_demand_node_pool(pool_obj)
                result['on_demand_pools'].append(pool)
        
        print("Waiting for resources - spot pool and ondemand pool to be ready ... (upto 20 minutes)")
        time.sleep(20*60)
        return result
    
    def cleanup_environment(self, namespace: str, resources: dict) -> bool:
        """
        Clean up all resources with a given name prefix.
        
        Args:
            namespace: Namespace to clean up
            name_prefix: Prefix of resources to clean up
        
        Returns:
            True if cleanup was successful
        """
        try:
            # Delete spot pools
            spot_pools = self.client.list_spot_node_pools(namespace)
            for user_pool in resources['spot_pools']:
                for available_pool in spot_pools:
                    if available_pool.name == user_pool.name:
                        self.client.delete_spot_node_pool(namespace, user_pool.name)
            
            # Delete on-demand pools
            on_demand_pools = self.client.list_on_demand_node_pools(namespace)
            for user_pool in resources['on_demand_pools']:
                for available_pool in on_demand_pools:
                    if available_pool.name == user_pool.name:
                        self.client.delete_on_demand_node_pool(namespace, user_pool.name)
            
            # Delete cloudspaces
            cloudspaces = self.client.list_cloudspaces(namespace)
            for cloudspace in cloudspaces:
                if cloudspace.name == resources["cloudspace"].name:
                    self.client.delete_cloudspace(namespace, cloudspace.name)

            print("Resource cleanup completed successfully.")
            return True
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
            return False
    
    def get_environment_status(self, namespace: str) -> Dict[str, Any]:
        """
        Get status of all resources in a namespace.
        
        Args:
            namespace: Namespace to check
        
        Returns:
            Dictionary with status information
        """
        try:
            cloudspaces = self.client.list_cloudspaces(namespace)
            spot_pools = self.client.list_spot_node_pools(namespace)
            on_demand_pools = self.client.list_on_demand_node_pools(namespace)
            
            return {
                'cloudspaces': {
                    'count': len(cloudspaces),
                    'ready': len([cs for cs in cloudspaces if cs.phase == 'Ready']),
                    'details': [
                        {
                            'name': cs.name,
                            'phase': cs.phase,
                            'health': cs.health,
                            'kubernetes_version': cs.current_kubernetes_version
                        }
                        for cs in cloudspaces
                    ]
                },
                'spot_pools': {
                    'count': len(spot_pools),
                    'total_desired': sum(pool.desired for pool in spot_pools),
                    'total_won': sum(pool.won_count or 0 for pool in spot_pools),
                    'details': [
                        {
                            'name': pool.name,
                            'cloudspace': pool.cloudspace,
                            'desired': pool.desired,
                            'won_count': pool.won_count,
                            'bid_status': pool.bid_status
                        }
                        for pool in spot_pools
                    ]
                },
                'on_demand_pools': {
                    'count': len(on_demand_pools),
                    'total_desired': sum(pool.desired for pool in on_demand_pools),
                    'total_reserved': sum(pool.reserved_count or 0 for pool in on_demand_pools),
                    'details': [
                        {
                            'name': pool.name,
                            'cloudspace': pool.cloudspace,
                            'desired': pool.desired,
                            'reserved_count': pool.reserved_count,
                            'reserved_status': pool.reserved_status
                        }
                        for pool in on_demand_pools
                    ]
                }
            }
            
        except Exception as e:
            return {'error': str(e)}

