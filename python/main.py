"""
Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0

Rackspace Spot Python SDK

A Python SDK for interacting with the Rackspace Spot API.
Provides an easy-to-use interface for managing cloudspaces, spot node pools, and on-demand node pools.
"""

from utils import parse_args
from full_deployment import example_full_deployment
from complete_scenario import example_complete_scenario

# Example usage

if __name__ == "__main__":
    # Initialize client
    args = parse_args()
    
    # Initialize client with refresh token
    refresh_token = args.refresh_token
    if not refresh_token:
        print("Refresh token is required.")
        exit(1)

    if args.complete_scenario:
        example_complete_scenario(refresh_token=refresh_token)

    if args.full_deployment:
        example_full_deployment(refresh_token=refresh_token)

    if not (args.complete_scenario or args.full_deployment):
        print("Please provide the --complete-scenario or --full-deployment argument to run the examples.")
        exit(1)
    
