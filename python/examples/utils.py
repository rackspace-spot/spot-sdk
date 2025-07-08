# Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import argparse

def parse_args():
    """
    Parse command line arguments for the Rackspace Spot SDK operations.
    """
    parser = argparse.ArgumentParser(description="Running complete cycle of Rackspace Spot SDK operations")
    parser.add_argument('--refresh-token', required=True, help='Refresh token of organization for OAuth authentication in which all operations are to be performed')
    parser.add_argument('--complete-scenario', action='store_true', help='Run the complete scenario')
    parser.add_argument('--full-deployment', action='store_true', help='Run the full deployment')
    return parser.parse_args()
