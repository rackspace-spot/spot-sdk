# Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import uuid
from typing import Dict, List, Optional
from datetime import datetime
import requests
from urllib.parse import urljoin

from classes import *


class RackspaceSpotClient:
    """
    Main client for interacting with the Rackspace Spot API.
    
    This client provides methods for managing cloudspaces, spot node pools,
    on-demand node pools, and retrieving market pricing information.
    """
    
    def __init__(
        self,
        refresh_token: str,
        base_url: str = "https://spot.rackspace.com",
        oauth_url: str = "https://login.spot.rackspace.com",
        timeout: int = 30
    ):
        """
        Initialize the Rackspace Spot client.
        
        Args:
            refresh_token: Your Rackspace Spot refresh token
            base_url: The base URL for the API (default: production)
            oauth_url: The OAuth URL for authentication
            timeout: Request timeout in seconds
        """
        self.refresh_token = refresh_token
        self.base_url = base_url.rstrip('/')
        self.oauth_url = oauth_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.access_token = None
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'rackspace-spot-python-sdk/1.0'
        })
        
        # Authenticate on initialization
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate and get access token."""
        auth_data = {
            'grant_type': 'refresh_token',
            'client_id': 'mwG3lUMV8KyeMqHe4fJ5Bb3nM1vBvRNa',
            'refresh_token': self.refresh_token
        }
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        try:
            response = self.session.post(
                f"{self.oauth_url}/oauth/token",
                data=auth_data,
                headers=headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get('id_token')
            
            if not self.access_token:
                raise RackspaceSpotAPIError("Failed to obtain access token")
            
            # Update session headers with bearer token
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
            
        except requests.exceptions.RequestException as e:
            raise RackspaceSpotAPIError(f"Authentication failed: {str(e)}")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None,
        authenticated: bool = True
    ) -> requests.Response:
        """Make an HTTP request to the API."""
        url = urljoin(self.base_url + "/", endpoint.lstrip('/'))
        
        headers = {}
        if not authenticated:
            headers = {'Authorization': ''}  # Remove auth header for unauthenticated endpoints
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None,
                params=params,
                headers=headers if not authenticated else None,
                timeout=self.timeout
            )

            if response.status_code == 401 and authenticated:
                # Token might be expired, try to re-authenticate
                self._authenticate()
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data if data else None,
                    params=params,
                    timeout=self.timeout
                )
            
            if not response.ok:
                error_msg = f"API request failed with status {response.status_code}"
                try:
                    error_detail = response.json()
                    if 'message' in error_detail:
                        error_msg += f": {error_detail['message']}"
                except:
                    error_msg += f": {response.text}"

                raise RackspaceSpotAPIError(
                    error_msg, 
                    status_code=response.status_code, 
                    response=response
                )
            
            return response
            
        except requests.exceptions.RequestException as e:
            raise RackspaceSpotAPIError(f"Request failed: {str(e)}")
    
    # Organization methods
    def list_organizations(self) -> List[Organization]:
        """List all organizations."""
        response = self._make_request('GET', '/apis/auth.ngpc.rxt.io/v1/organizations')
        data = response.json()
        
        organizations = []
        for org_data in data.get('organizations', []):
            organizations.append(Organization(
                id=org_data['id'],
                name=org_data['name'],
                display_name=org_data['display_name'],
                namespace=org_data['metadata']['namespace']
            ))
        
        return organizations
    
    # Region methods
    def list_regions(self) -> List[Region]:
        """List all available regions."""
        response = self._make_request('GET', '/apis/ngpc.rxt.io/v1/regions')
        data = response.json()
        
        regions = []
        for item in data.get('items', []):
            spec = item.get('spec', {})
            provider = spec.get('provider', {})
            
            regions.append(Region(
                name=item['metadata']['name'],
                country=spec.get('country'),
                description=spec.get('description'),
                provider_type=provider.get('providerType'),
                provider_region_name=provider.get('providerRegionName')
            ))
        
        return regions
    
    def get_region(self, name: str) -> Region:
        """Get a specific region by name."""
        response = self._make_request('GET', f'/apis/ngpc.rxt.io/v1/regions/{name}')
        data = response.json()
        
        spec = data.get('spec', {})
        provider = spec.get('provider', {})
        
        return Region(
            name=data['metadata']['name'],
            country=spec.get('country'),
            description=spec.get('description'),
            provider_type=provider.get('providerType'),
            provider_region_name=provider.get('providerRegionName')
        )
    
    # Server class methods
    def list_server_classes(self) -> List[ServerClassInfo]:
        """List all available server classes."""
        response = self._make_request('GET', '/apis/ngpc.rxt.io/v1/serverclasses')
        data = response.json()
        
        server_classes = []
        for item in data.get('items', []):
            spec = item.get('spec', {})
            status = item.get('status', {})
            resources = spec.get('resources', {})
            on_demand = spec.get('onDemandPricing', {})
            spot_pricing = status.get('spotPricing', {})
            
            server_classes.append(ServerClassInfo(
                name=item['metadata']['name'],
                display_name=spec.get('displayName'),
                category=spec.get('category'),
                flavor_type=spec.get('flavorType'),
                cpu=resources.get('cpu'),
                memory=resources.get('memory'),
                region=spec.get('region'),
                availability=spec.get('availability'),
                on_demand_cost=on_demand.get('cost'),
                spot_hammer_price=spot_pricing.get('hammerPricePerHour'),
                spot_market_price=spot_pricing.get('marketPricePerHour')
            ))
        
        return server_classes
    
    def get_server_class(self, name: str) -> ServerClassInfo:
        """Get a specific server class by name."""
        response = self._make_request('GET', f'/apis/ngpc.rxt.io/v1/serverclasses/{name}')
        data = response.json()
        
        spec = data.get('spec', {})
        status = data.get('status', {})
        resources = spec.get('resources', {})
        on_demand = spec.get('onDemandPricing', {})
        spot_pricing = status.get('spotPricing', {})
        
        return ServerClassInfo(
            name=data['metadata']['name'],
            display_name=spec.get('displayName'),
            category=spec.get('category'),
            flavor_type=spec.get('flavorType'),
            cpu=resources.get('cpu'),
            memory=resources.get('memory'),
            region=spec.get('region'),
            availability=spec.get('availability'),
            on_demand_cost=on_demand.get('cost'),
            spot_hammer_price=spot_pricing.get('hammerPricePerHour'),
            spot_market_price=spot_pricing.get('marketPricePerHour')
        )
    
    # CloudSpace methods
    def list_cloudspaces(self, namespace: str) -> List[CloudSpace]:
        """List all cloudspaces in a namespace."""
        response = self._make_request('GET', f'/apis/ngpc.rxt.io/v1/namespaces/{namespace}/cloudspaces')
        data = response.json()
        
        cloudspaces = []
        for item in data.get('items', []):
            spec = item.get('spec', {})
            status = item.get('status', {})
            
            cloudspace = CloudSpace(
                name=item['metadata']['name'],
                namespace=item['metadata']['namespace'],
                region=spec['region'],
                kubernetes_version=spec['kubernetesVersion'],
                webhook=spec.get('webhook'),
                cni=spec.get('cni', 'calico'),
                ha_control_plane=spec.get('HAControlPlane', False),
                cloud=spec.get('cloud', 'default'),
                api_server_endpoint=status.get('APIServerEndpoint'),
                phase=status.get('phase'),
                health=status.get('health'),
                current_kubernetes_version=status.get('currentKubernetesVersion')
            )
            
            # Parse first ready timestamp
            if status.get('firstReadyTimestamp'):
                try:
                    cloudspace.first_ready_timestamp = datetime.fromisoformat(
                        status['firstReadyTimestamp'].replace('Z', '+00:00')
                    )
                except:
                    pass
            
            cloudspaces.append(cloudspace)
        
        return cloudspaces
    
    def get_cloudspace(self, namespace: str, name: str) -> CloudSpace:
        """Get a specific cloudspace by name."""
        response = self._make_request('GET', f'/apis/ngpc.rxt.io/v1/namespaces/{namespace}/cloudspaces/{name}')
        data = response.json()
        if response.status_code == 404:
            return None
        spec = data.get('spec', {})
        status = data.get('status', {})
        if not response.ok:
            raise RackspaceSpotAPIError(
                f"Failed to get cloudspace {name}: {response.status_code}",
                status_code=response.status_code,
                response=response
            )
        cloudspace = CloudSpace(
            name=data['metadata']['name'],
            namespace=data['metadata']['namespace'],
            region=spec['region'],
            kubernetes_version=spec['kubernetesVersion'],
            webhook=spec.get('webhook'),
            cni=spec.get('cni', 'calico'),
            ha_control_plane=spec.get('HAControlPlane', False),
            cloud=spec.get('cloud', 'default'),
            api_server_endpoint=status.get('APIServerEndpoint'),
            phase=status.get('phase'),
            health=status.get('health'),
            current_kubernetes_version=status.get('currentKubernetesVersion')
        )
        
        # Parse first ready timestamp
        if status.get('firstReadyTimestamp'):
            try:
                cloudspace.first_ready_timestamp = datetime.fromisoformat(
                    status['firstReadyTimestamp'].replace('Z', '+00:00')
                )
            except:
                pass
        
        return cloudspace
    
    def create_cloudspace(self, cloudspace: CloudSpace) -> CloudSpace:
        """Create a new cloudspace."""
        payload = {
            "apiVersion": "ngpc.rxt.io/v1",
            "kind": "CloudSpace",
            "metadata": {
                "name": cloudspace.name,
                "namespace": cloudspace.namespace
            },
            "spec": {
                "region": cloudspace.region,
                "kubernetesVersion": cloudspace.kubernetes_version,
                "cni": cloudspace.cni,
                "HAControlPlane": cloudspace.ha_control_plane,
                "cloud": cloudspace.cloud
            }
        }
        
        if cloudspace.webhook:
            payload["spec"]["webhook"] = cloudspace.webhook
        
        response = self._make_request(
            'POST', 
            f'/apis/ngpc.rxt.io/v1/namespaces/{cloudspace.namespace}/cloudspaces',
            data=payload
        )
        
        data = response.json()
        return self._parse_cloudspace(data)
    
    def delete_cloudspace(self, namespace: str, name: str) -> bool:
        """Delete a cloudspace."""
        self._make_request('DELETE', f'/apis/ngpc.rxt.io/v1/namespaces/{namespace}/cloudspaces/{name}')
        return True
    
    def _parse_cloudspace(self, data: Dict) -> CloudSpace:
        """Parse cloudspace data from API response."""
        spec = data.get('spec', {})
        status = data.get('status', {})
        
        cloudspace = CloudSpace(
            name=data['metadata']['name'],
            namespace=data['metadata']['namespace'],
            region=spec['region'],
            kubernetes_version=spec['kubernetesVersion'],
            webhook=spec.get('webhook'),
            cni=spec.get('cni', 'calico'),
            ha_control_plane=spec.get('HAControlPlane', False),
            cloud=spec.get('cloud', 'default'),
            api_server_endpoint=status.get('APIServerEndpoint'),
            phase=status.get('phase'),
            health=status.get('health'),
            current_kubernetes_version=status.get('currentKubernetesVersion')
        )
        
        if status.get('firstReadyTimestamp'):
            try:
                cloudspace.first_ready_timestamp = datetime.fromisoformat(
                    status['firstReadyTimestamp'].replace('Z', '+00:00')
                )
            except:
                pass
        
        return cloudspace
    
    # SpotNodePool methods
    def list_spot_node_pools(self, namespace: str) -> List[SpotNodePool]:
        """List all spot node pools in a namespace."""
        response = self._make_request('GET', f'/apis/ngpc.rxt.io/v1/namespaces/{namespace}/spotnodepools')
        data = response.json()
        
        pools = []
        for item in data.get('items', []):
            pools.append(self._parse_spot_node_pool(item))
        
        return pools
    
    def get_spot_node_pool(self, namespace: str, name: str) -> SpotNodePool:
        """Get a specific spot node pool by name."""
        response = self._make_request('GET', f'/apis/ngpc.rxt.io/v1/namespaces/{namespace}/spotnodepools/{name}')
        data = response.json()
        
        return self._parse_spot_node_pool(data)
    
    def create_spot_node_pool(self, pool: SpotNodePool) -> SpotNodePool:
        """Create a new spot node pool."""
        # Generate UUID name if not provided
        if not pool.name:
            pool.name = str(uuid.uuid4()).lower()
        
        payload = {
            "apiVersion": "ngpc.rxt.io/v1",
            "kind": "SpotNodePool",
            "metadata": {
                "name": pool.name,
                "namespace": pool.namespace
            },
            "spec": {
                "cloudSpace": pool.cloudspace,
                "serverClass": pool.server_class,
                "desired": pool.desired,
                "bidPrice": pool.bid_price,
                "autoscaling": {
                    "enabled": pool.autoscaling_enabled
                }
            }
        }
        
        if pool.autoscaling_enabled:
            if pool.min_nodes is not None:
                payload["spec"]["autoscaling"]["minNodes"] = pool.min_nodes
            if pool.max_nodes is not None:
                payload["spec"]["autoscaling"]["maxNodes"] = pool.max_nodes
        
        response = self._make_request(
            'POST',
            f'/apis/ngpc.rxt.io/v1/namespaces/{pool.namespace}/spotnodepools',
            data=payload
        )
        
        data = response.json()
        return self._parse_spot_node_pool(data)
    
    def delete_spot_node_pool(self, namespace: str, name: str) -> bool:
        """Delete a spot node pool."""
        self._make_request('DELETE', f'/apis/ngpc.rxt.io/v1/namespaces/{namespace}/spotnodepools/{name}')
        return True
    
    def _parse_spot_node_pool(self, data: Dict) -> SpotNodePool:
        """Parse spot node pool data from API response."""
        spec = data.get('spec', {})
        status = data.get('status', {})
        autoscaling = spec.get('autoscaling', {})
        
        return SpotNodePool(
            name=data['metadata']['name'],
            namespace=data['metadata']['namespace'],
            cloudspace=spec['cloudSpace'],
            server_class=spec['serverClass'],
            desired=spec['desired'],
            bid_price=spec['bidPrice'],
            autoscaling_enabled=autoscaling.get('enabled', False),
            min_nodes=autoscaling.get('minNodes'),
            max_nodes=autoscaling.get('maxNodes'),
            bid_status=status.get('bidStatus'),
            won_count=status.get('wonCount')
        )
    
    # OnDemandNodePool methods
    def list_on_demand_node_pools(self, namespace: str) -> List[OnDemandNodePool]:
        """List all on-demand node pools in a namespace."""
        response = self._make_request('GET', f'/apis/ngpc.rxt.io/v1/namespaces/{namespace}/ondemandnodepools')
        data = response.json()
        
        pools = []
        for item in data.get('items', []):
            pools.append(self._parse_on_demand_node_pool(item))
        
        return pools
    
    def get_on_demand_node_pool(self, namespace: str, name: str) -> OnDemandNodePool:
        """Get a specific on-demand node pool by name."""
        response = self._make_request('GET', f'/apis/ngpc.rxt.io/v1/namespaces/{namespace}/ondemandnodepools/{name}')
        data = response.json()
        
        return self._parse_on_demand_node_pool(data)
    
    def create_on_demand_node_pool(self, pool: OnDemandNodePool) -> OnDemandNodePool:
        """Create a new on-demand node pool."""
        # Generate UUID name if not provided
        if not pool.name:
            pool.name = str(uuid.uuid4()).lower()
        
        payload = {
            "apiVersion": "ngpc.rxt.io/v1",
            "kind": "OnDemandNodePool",
            "metadata": {
                "name": pool.name,
                "namespace": pool.namespace
            },
            "spec": {
                "cloudSpace": pool.cloudspace,
                "serverClass": pool.server_class,
                "desired": pool.desired
            }
        }
        
        response = self._make_request(
            'POST',
            f'/apis/ngpc.rxt.io/v1/namespaces/{pool.namespace}/ondemandnodepools',
            data=payload
        )
        
        data = response.json()
        return self._parse_on_demand_node_pool(data)
    
    def delete_on_demand_node_pool(self, namespace: str, name: str) -> bool:
        """Delete an on-demand node pool."""
        self._make_request('DELETE', f'/apis/ngpc.rxt.io/v1/namespaces/{namespace}/ondemandnodepools/{name}')
        return True
    
    def _parse_on_demand_node_pool(self, data: Dict) -> OnDemandNodePool:
        """Parse on-demand node pool data from API response."""
        spec = data.get('spec', {})
        status = data.get('status', {})
        
        return OnDemandNodePool(
            name=data['metadata']['name'],
            namespace=data['metadata']['namespace'],
            cloudspace=spec['cloudSpace'],
            server_class=spec['serverClass'],
            desired=spec['desired'],
            reserved_count=status.get('reservedCount'),
            reserved_status=status.get('reservedStatus')
        )
    
    # Pricing and market data methods (unauthenticated)
    def get_price_history(self, server_class: str) -> PriceHistory:
        """Get price history for a server class (unauthenticated)."""
        # Use different base URL for price history
        price_url = f"https://ngpc-prod-public-data.s3.us-east-2.amazonaws.com/history/{server_class}"
        
        response = requests.get(price_url, timeout=self.timeout)
        if not response.ok:
            raise RackspaceSpotAPIError(
                f"Failed to get price history for {server_class}: {response.status_code}",
                status_code=response.status_code,
                response=response
            )
        
        data = response.json()
        return PriceHistory(
            server_class=data['auction'],
            history=data['history']
        )
