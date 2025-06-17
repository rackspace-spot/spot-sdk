# Introduction:

# Pre-requisites:
1. Need to have organization (namespace) setted up already to perform CRUD operations in cluster.
2. Need to have billing setted up in that organzation already to perform CRUD operations related to organization, cloudspaces, nodepools in cluster.

# Terminologies:
1. Organization:

    - Organization is a representation as a collection of cloudspaces (Kubernetes clusters). 

    - Each organization has a unique name and organization ID (namespace) associated with it.

    - Each organization requires setting up a separate billing account for its management.

2. Namespace: 

    - The namespace is a representation to identify any organization in Spot Platform. 

    - Each organization has a unique namespace associated with it. 

    - The namespace is used to scope resources and operations within the Spot platform. 

    - Each namespace start with org-.

    - To obtain desired namespace, leverage API: list all organizations to retrieve the details of all organizations, including their associated namespaces.

3. Cloudspace:

    - Cloudspace is a representation of a Kubernetes cluster in your namespace.

    - Each cloudspace is associated with a specific region and will contain SpotNodePool and OnDemandNodePool for storing servers bidded on platform.

4. SpotNodePools and OnDemandNodePools: 

    - The SpotNodePools and OnDemandNodePools are nodepools that will contain servers that users have bidded for. 

    - When creating the SpotNodePools and OnDemandNodePools, cloudspace should already be created.

    - Billing should be enabled in your organization for the SpotNodePools and OnDemandNodePools to be created.

# Setup
Refer each language specific setup configuration in their respective folders.

# Additional References:
All public available APIs can be found in the [Rackspace Spot Public API Documentation](https://spot.rackspace.com/rackspace-spot-public-api)

## 📜 License
**Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.**  

`SPDX-License-Identifier: Apache-2.0`
