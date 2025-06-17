# Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from typing import Dict, List, Optional, Union, Any
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import requests


class ServerClass(Enum):
    """Common server class types."""
    GP_VS1_MEDIUM_IAD = "gp.vs1.medium-iad"
    GP_VS1_LARGE_IAD = "gp.vs1.large-iad"
    GP_VS1_XLARGE_IAD = "gp.vs1.xlarge-iad"
    GP_VS1_2XLARGE_IAD = "gp.vs1.2xlarge-iad"
    MH_VS1_MEDIUM_IAD = "mh.vs1.medium-iad"
    MH_VS1_LARGE_IAD = "mh.vs1.large-iad"
    MH_VS1_XLARGE_IAD = "mh.vs1.xlarge-iad"
    MH_VS1_2XLARGE_IAD = "mh.vs1.2xlarge-iad"
    CH_VS1_MEDIUM_IAD = "ch.vs1.medium-iad"
    CH_VS1_LARGE_IAD = "ch.vs1.large-iad"
    CH_VS1_XLARGE_IAD = "ch.vs1.xlarge-iad"
    CH_VS1_2XLARGE_IAD = "ch.vs1.2xlarge-iad"


class KubernetesVersion(Enum):
    """Available Kubernetes versions."""
    V1_31_1 = "1.31.1"
    V1_30_10 = "1.30.10"
    V1_29_6 = "1.29.6"


class CNI(Enum):
    """Container Network Interface options."""
    CALICO = "calico"
    CILIUM = "cilium"
    BYOCNI = "byocni"


@dataclass
class Organization:
    """Represents an organization."""
    id: str
    name: str
    display_name: str
    namespace: str


@dataclass
class Region:
    """Represents a region."""
    name: str
    country: Optional[str] = None
    description: Optional[str] = None
    provider_type: Optional[str] = None
    provider_region_name: Optional[str] = None


@dataclass
class ServerClassInfo:
    """Represents server class information."""
    name: str
    display_name: Optional[str] = None
    category: Optional[str] = None
    flavor_type: Optional[str] = None
    cpu: Optional[str] = None
    memory: Optional[str] = None
    region: Optional[str] = None
    availability: Optional[str] = None
    on_demand_cost: Optional[str] = None
    spot_hammer_price: Optional[str] = None
    spot_market_price: Optional[str] = None


@dataclass
class CloudSpace:
    """Represents a cloudspace (Kubernetes cluster)."""
    name: str
    namespace: str
    region: str
    kubernetes_version: str
    webhook: Optional[str] = None
    cni: str = CNI.CALICO.value
    ha_control_plane: bool = False
    cloud: str = "default"
    
    # Status fields (read-only)
    api_server_endpoint: Optional[str] = None
    phase: Optional[str] = None
    health: Optional[str] = None
    current_kubernetes_version: Optional[str] = None
    first_ready_timestamp: Optional[datetime] = None


@dataclass
class SpotNodePool:
    """Represents a spot node pool."""
    name: str
    namespace: str
    cloudspace: str
    server_class: str
    desired: int
    bid_price: str
    autoscaling_enabled: bool = False
    min_nodes: Optional[int] = None
    max_nodes: Optional[int] = None
    
    # Status fields (read-only)
    bid_status: Optional[str] = None
    won_count: Optional[int] = None


@dataclass
class OnDemandNodePool:
    """Represents an on-demand node pool."""
    name: str
    namespace: str
    cloudspace: str
    server_class: str
    desired: int
    
    # Status fields (read-only)
    reserved_count: Optional[int] = None
    reserved_status: Optional[str] = None


@dataclass
class PriceHistory:
    """Represents price history for a server class."""
    server_class: str
    history: List[Dict[str, Union[int, float]]]


class RackspaceSpotAPIError(Exception):
    """Custom exception for Rackspace Spot API errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[requests.Response] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

