# LMNH AWS Cloud Architecture
This folder contains the terraform config to provision the following cloud architecture displayed in _Figure 1_

![LMNH-cloud-architecture-diagram](../assets/starwatch_architecture_diagram.png)

__Figure 1__: Cloud architecture diagram for LMNH botanical data pipeline

## Setup
1. Ensure you have a valid AWS account with the following:
    - VPC
    - Public subnet

2. Install Terraform onto your local machine using the following for mac.
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```
This can also be done on windows or linux using readily available package installers.

3. Run the following command to initialise terraform in this folder:
```bash
terraform init
```
4. Using the AWS UI create four repositories on ECR for the following things:
    - Quadhoral OpenMeteo pipeline
    - Weekly OpenMeteo pipeline
    - Astronomy API pipeline
    - Aurorawatch API pipeline
    - Dashboard ECS image
    - SMS-Checker 

5. Make sure you have pushed the docker images of each respective folder in this repository to ensure terraform can provision the designed architecture.

6. Create a `terraform.tfvars` file containing the values for the variables shown in `variables.tf` in the following format.
```bash
AWS_ACCESS_KEY = "Value"
...
```
For this step you will need the `URI` of the pre-built ECR repositories.


## Usage
In case you would like to check you have setup correctly run the following:
```bash
terraform plan
```

Once happy to provision the cloud architecture run the following command:
```bash
terraform apply
```

In order to deprovision the cloud architecture run the following command:
```bash
terraform destroy
```

For these commands ensure you are in the terraform initialised folder when running these commands.

## How it works
#### main.tf
- This contains the terraform config required for provisioning the cloud architecture.
#### variables.tf
- Defines the secret variables used in `main.tf`.
#### terraform.tfvars
- This is not provided by this repository and needs to be created.
- Contains the secret variables defined in `variables.tf`.
- This file name has been added to the `.gitignore` so that your details are not leaked.