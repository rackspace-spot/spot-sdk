import argparse

from rackspace_spot_sdk.client import RackspaceSpotClient

def parse_args():
    """
    Parse command line arguments for the Rackspace Spot SDK operations.
    """
    parser = argparse.ArgumentParser(description="Running complete cycle of Rackspace Spot SDK operations")
    parser.add_argument('--refresh-token', required=True, help='Refresh token of organization for OAuth authentication in which all operations are to be performed')
    return parser.parse_args()

def delete_cloudspace(refresh_token: str):
    client = RackspaceSpotClient(refresh_token=refresh_token)

    name="test-cloudspace-123" # Make sure cloudspace already with this name exists in organization from which refresh token is obtained.

    try:
        client.delete_cloudspace(namespace=client.namespace, name=name)
    except Exception as e:
        print(f"Error deleting cloudspace: {e}")
        return

    print("Cloudspace deleted successfully")

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_args()
    
    # Get refresh token from args
    refresh_token = args.refresh_token
    if not refresh_token:
        print("Refresh token is required.")
        exit(1)

    delete_cloudspace(refresh_token=refresh_token)
