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
- Existing resources are specified using the `data` keyword they include:
    - VPC - Virtual private cloud.
    - Public Subnet - a subsection of the VPC that is accessible externally.
    - ECS cluster - this is the cluster of machines our dashboard will run on.
- Local variables are defined by the `locals` keyword this defines:
    - API keys - for running the lambda pipelines.
    - Database variables - to securely access the RDS instance.
    - Image URIs - for the ECR repositories to be used.
- New resources are defined by the `resource` keyword and these services can be grouped into the following:
    - RDS:
        - The RDS instance - the database itself.
        - Database subnet group - the specific subnet the RDS will run on.
        - Database security group - the rules of accessing the database.
    - Lambda:
        - The lambda function - created by recursion through the use of a `local` block.
        - AWS cloudwatch rules - allows for logging.
        - IAM role - an administration role that allows the lambdas to execute and to pull images from ECR. These are assigned by recursion and a `if` statement so that only the minimum required permisions are granted.
    - State machine: 
        - Step function - creates two step functions that target the lambdas to run either hourly or quadhorally.
        - IAM role - an administration role that allows the state machine to execute.
    - ECS:
        - IAM role - an administration role that allows the ECS task to execute.
        - AWS cloudwatch rules - allows for logging by ecs.
        - ECS task definition - this defines which ECR image will be loaded and on what machine.
        - ECS service - a system that restarts the ECS task upon failure.
    - Eventbridge:
        - Cloudwatch roles - allows for logging by eventbridge
        - Eventbridge bus - A quadhoral, hourly and weekly eventbridge triggers are provisioned

#### variables.tf
- Defines the secret variables used in `main.tf`.
- Contains no sensitive information, only the name and type of each sensitive variable
#### terraform.tfvars
- This is not provided by this repository and needs to be created.
- Contains the secret variables defined in `variables.tf`.
- This file name has been added to the `.gitignore` so that your details are not leaked.