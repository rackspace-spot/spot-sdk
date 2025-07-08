# Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import uuid
# Define configuration for any number of spot and on-demand pools you want to create.
spot_pools_config = [
    {
        'name': str(uuid.uuid4()).lower(),
        'server_class': 'gp.vs1.medium-iad',
        'desired': 2, # node count
        'bid_price': '0.55' # update as per current market price
    }
    ## .... Add more spot pools as needed here 
]

on_demand_pools_config = [
    {
        'name': str(uuid.uuid4()).lower(),
        'server_class': 'gp.vs1.medium-iad',
        'desired': 1  # node count
    }
    ## .... Add more on-demand pools as needed here 
]