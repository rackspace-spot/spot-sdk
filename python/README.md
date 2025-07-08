# 🚀 Rackspace Spot SDK Script Runner

The Python scripts in **examples** folder demonstrates how to use the **Rackspace Spot SDK** for orchestrating cloud resources such as cloudspaces, spot pools, and on-demand pools. You can execute operations like: **Create Clouspace**, **Delete Cloudspace**, **Complete Scenario**, **Full Deployment** depending on the flags provided for latter two.

---

## 📚 Overview

The Rackspace Spot SDK provides tools to manage cloud resources programmatically. This script helps you:

- Understand the complete lifecycle of Rackspace Spot resources.
- Simulate production-like workflows.
- Validate integration in CI/CD pipelines.

---

## 🧪 Scenario Types

### ✅ Create and Delete Cloudspaces:
-  Simulates **creation** of **cloudspace** with **spotnodepool**
-  **Delete** above created **cloudspace** and **spotnodepool**

> Use this to understand how to create and delete cloudspace successfully.

---

### ✅ Complete Scenario

Simulates a full Rackspace Spot workflow:

- Lists available **regions** and **server classes**.
- Creates a **cloudspace**, one **spot pool**, and one **on-demand pool**.
- Lists all created resources.
- Cleans up the created resources.

> Use this to understand the SDK's capabilities in a simple, guided flow.

---

### ✅ Full Deployment

Simulates a scalable deployment lifecycle with three stages:

1. **Create Environment**: Provisions one cloudspace and multiple spot/on-demand pools based on `dynamic_pools_config.py`.
2. **Get Environment**: Lists all created resources.
3. **Cleanup Environment**: Tears down the created resources.

> Ideal for integration testing or use in automation pipelines.

---

## ⚙️ Prerequisites

### 🔧 Requirements

- Python **3.10** or newer
- A **refresh token** from Rackspace Spot

> On macOS/Linux, use `python3` and `pip3` if `python` defaults to Python 2.

---

### 🔑 How to Obtain a Refresh Token

1. Go to: [Rackspace Spot API Access Page](https://spot.rackspace.com/ui/api-access/terraform)
2. Navigate to **API Access > Terraform**
3. Click **Get New Token**
4. Use the **refresh token** in the script

---

## 🛠️ Installation
### 📦 Option 1: Install directly from GitHub (for end users or automation)
```bash
# (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

pip install git+https://github.com/rackspace-spot/spot-sdk.git#subdirectory=python
```
- To see how to use the SDK in your own project, refer to the sample script:
- 📄 [`examples/create_cloudspace.py`](./examples/create_cloudspace.py) – Demonstrates how to initialize the client and create a cloudspace using the SDK.
- You can use this as a reference to integrate the SDK in your own Python code.

---

###  📦 Option 2: Clone and install locally (Recommended for contributors)
```bash
# Clone the repository
git clone <repo_url>
cd spot_sdk
cd python

# (Optional) Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

#  Install runtime dependencies like setuptools for other dependencies installation
pip install -r requirements.txt 

#  Install SDK in editable mode - (🧩 Enable local SDK usage)
pip install -e .     
```

## 📦 Script Description
This script accepts a required OAuth --refresh-token and one of the flags:

| Argument                 | Description                               
| ------------------------ | -----------------------------------------
| `--refresh-token`        | OAuth refresh token (Always required)
| `--complete-scenario`    | To run the complete scenario 
| `--full-deployment`      | To run the full deployment


## ▶️ Usage Examples (Must be in **python** directory to run commands)
### ✅ 1. Run Cloudspace creation with Spotnodepool scenario
You can simply run the script with your refresh token:

```bash
python examples/create_cloudspace.py --refresh-token <YOUR_REFRESH_TOKEN>
```

### ✅ 2. Run Cloudspace deletion with Spotnodepool scenario
You can simply run the script with your refresh token:
(Make sure that the cloudspace with the given name in delete_cloudspace.py file exists in the organization associated with the incoming refresh token)
```bash
python examples/delete_cloudspace.py --refresh-token <YOUR_REFRESH_TOKEN>
```

### ✅ 3. Run Only the Complete Scenario
You can simply run the script with your refresh token:

```bash
python examples/main.py --refresh-token <YOUR_REFRESH_TOKEN> --complete-scenario
```

## ✅ 4. Run Only the Full Deployment
To run just the full deployment and skip the complete scenario:

```bash
python examples/main.py --refresh-token <YOUR_REFRESH_TOKEN> --full-deployment
```

## ✅ 5. Run Both Scenarios
This will execute both scenarios one after another:

```bash
python examples/main.py --refresh-token <YOUR_REFRESH_TOKEN> --complete-scenario --full-deployment
```

## ❌ 6. Run Neither Scenario (Invalid – Will Exit)
This will result in an error because no scenarios are selected:

```bash
python examples/main.py --refresh-token <YOUR_REFRESH_TOKEN>
```
Output:

```bash 
Please provide the --complete-scenario or --full-deployment argument to run the examples.
```

## 📦 Configuration Options
Edit dynamic_pools_config.py to customize:

- Number of spot pools

- Number of on-demand pools

- Resource specifications

- If you wish to choose a different serverclass (which may also depend on the region where your Cloudspace is deployed or available), please refer to the Public API documentation in the Additional References section below.

### Additional References:
All public available APIs can be found in the [Rackspace Spot Public API Documentation](https://spot.rackspace.com/docs/rackspace-spot-public-api)

## 🧩 Usecase
- **Create and Delete Cloudspaces**: Useful for understanding the cloudspace creation and deletion operations in Rackspace Spot. Ideal for first-time users exploring the SDK.
- **Complete Scenario**: Useful for understanding the end-to-end flow of resource creation and how the Rackspace Spot system works. Ideal for first-time users exploring the SDK.
- **Full Deployment**: Designed for CI/CD pipelines to test the system's functionality and resource orchestration in environments that closely resemble production.

## 🛠️ Troubleshooting
If you encounter issues:

- Verify your Python version meets the minimum requirement (3.8+)
- Ensure your refresh token is valid and has the necessary permissions
- Check that all dependencies are properly installed
- Verify you're in the correct directory (python folder)

## 🧑‍💻 Support
For documentation, please refer to the [official Rackspace Spot documentation](https://spot.rackspace.com/docs/en). For support, ask your questions in the [Rackspace community discussions](https://github.com/rackerlabs/spot/discussions), or drop us an email.

## 📜 License
**Copyright © Rackspace US, Inc. or its affiliates. All Rights Reserved.**  

`SPDX-License-Identifier: Apache-2.0`
