import argparse
import uuid

from rackspace_spot_sdk.client import RackspaceSpotClient
from rackspace_spot_sdk.classes import CloudSpace, KubernetesVersion, SpotNodePool

def parse_args():
    """
    Parse command line arguments for the Rackspace Spot SDK operations.
    """
    parser = argparse.ArgumentParser(description="Running complete cycle of Rackspace Spot SDK operations")
    parser.add_argument('--refresh-token', required=True, help='Refresh token of organization for OAuth authentication in which all operations are to be performed')
    return parser.parse_args()

def create_cloudspace_and_spot_node_pool(refresh_token: str):
    client = RackspaceSpotClient(refresh_token=refresh_token)

    cloudspace_object = CloudSpace(
                name="test-cloudspace-123", # Make sure this name is unique in your namespace and cloudspace does not already exist.
                namespace=client.namespace,
                region="us-east-iad-1",
                kubernetes_version=KubernetesVersion.V1_31_1.value
            )

    cloudspace = client.create_cloudspace(cloudspace_object)

    print(f"Creation requested submitted for cloudspace: {cloudspace.name}")
    
    pool_obj = SpotNodePool(
                name=str(uuid.uuid4()).lower(),
                namespace=client.namespace,
                cloudspace=cloudspace.name,
                server_class="gp.vs1.medium-iad",
                desired=2,
                bid_price="0.5" # update as per current market price
            )
    spot_pool = client.create_spot_node_pool(pool_obj)

    print(f"Creation requested submitted for spot node pool: {spot_pool.name}")
    print("Creation of spot pool with nodes takes some minutes ( upto 20 minutes )...")
    print("Please check the status of spot pool in the Rackspace Spot UI.\n Thanks")


if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    
    # Get refresh token from args
    refresh_token = args.refresh_token
    if not refresh_token:
        print("Refresh token is required.")
        exit(1)

    create_cloudspace_and_spot_node_pool(refresh_token=refresh_token)
