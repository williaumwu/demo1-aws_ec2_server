# Integrating Terraform Code with Config0

## Overview
This guide explains how to integrate your existing Terraform code into Config0.  
This Terraform code and its execution then become:
   - Immutable
   - Portable
   - Easily reusable by other upstream Terraform and DevOps code
      - Terraform to Terraform connections
      - Terraform to Ansible connections

## Process Diagram
```
+-------------------------+
|       terraform/        |
|       data.tf           |
|       main.tf           |
|       outputs.tf        |
|       variables.tf      |
|       provider.tf       |
+-------------------------+
            |
            | imported as
            v
+--------------------------------------------+
| williaumwu:::demo1-aws_ec2_server::        |
| ec2_server                                 |
| (execgroup)                                |
|                                            |
+--------------------------------------------+
            |                 |
            | creates         | connected to
            v                 |
+-------------------------+   |
| /tmp/stackgen-          |   |
| ec2-server.yml          |   |
|                         |   |
+-------------------------+   |
            |                 |
            | imports         |
            v                 v
+--------------------------------------------+
| williaumwu:::aws_ec2_server                |
| (stack)                                    |
|                                            |
|                                            |
+--------------------------------------------+
```

### Diagram Explanation
- **Top box**: Your existing Terraform code files
- **Second box**: The Config0 execgroup created from your Terraform code
- **Middle box**: Configuration file for stack generation
- **Bottom box**: The resulting Config0 stack that can be reused across projects
- **Arrows**: Show the workflow and relationships between components

## Getting Started
We'll begin by assuming users have existing Terraform code in place.

### Prerequisites
- GitHub account
- Existing Terraform code for EC2 server creation

### Existing Resources
Terraform repository `demo1-aws_ec2_server` (this repository) for EC2 server creation

## Example: Integrating demo1-aws_ec2_server

We have simple Terraform code in the "terraform" folder. Follow these steps to create a stack:

### 1. Download Config0's Helper Stack Generation Script
```bash
curl https://raw.githubusercontent.com/config0-hub/config0_publisher/main/config0_publisher/bin/stack_gen -o /tmp/stack_gen
chmod 755 /tmp/stack_gen
```

### 2. Create Configuration File
The easiest approach is to create a config.yml file with these parameters:

- **tf_variables_file**: Location of the terraform variables file
- **execgroup**: The user provides the group "name" to files that are to be executed together (in this case, terraform files). We'll reference this later in `config0/contrib_repo.yml`
- **resource_type**: The user provides the resource_type to summarize the output of the execgroup. In this case, "server" is the only output of this execgroup of Terraform code.
- **timeout**: Maximum execution time in seconds (10 minutes is usually sufficient for server creation)
- **tf_runtime**: The terraform runtime format `<terraform/tofu>:<version>`
- **dest_dir**: Destination directory for the generated Config0 stack
- **stack_name**: Name of the Config0 stack

Use [^1] the following heredoc below for the Terraform code in this forked repository.
```bash
cat > /tmp/stackgen-ec2-server.yml << 'EOF'
tf_variables_file: terraform/variables.tf
execgroup: williaumwu:::demo1-aws_ec2_server::ec2_server
resource_type: server
timeout: 600
tf_runtime: tofu:1.9.1
dest_dir: stacks
stack_name: aws_ec2_server
EOF
```

### 3. Run Stack Generation Script
Execute the stack_gen script with your configuration file to generate the Config0 stack:

```bash
/tmp/stack_gen /tmp/stackgen-ec2-server.yml
```

This command processes your Terraform code and creates the necessary Config0 stack structure in the specified destination directory.

### 4. Replace "FIX ME" with stack.hostname 
The resource name ideally should be assigned a stack variable or string with stack variables. In this case, we will use the stack hostname (stack.hostname) as the resource name.

```bash
sed -i 's/FIX ME/stack.hostname/g' stacks/aws_ec2_server/_main/run.py
```

### 5. Create contrib_repo.yml
Create the configuration file that maps your existing code to Config0 assets:

#### Understanding the Mapping

##### 1) Execgroup Mapping
Repository location of terraform code is mapped to a Config0 execgroup with the format:
```
<username>:::<repo_name>::<execgroup name>
```

For example:
```
Config0 execgroup => williaumwu:::demo1-aws_ec2_server::ec2_server
```

##### 2) Stack Mapping
Repository location of generated Config0 stack follows the format:
```
<username>:::<stack name>
```

For example:
```
Config0 stack => williaumwu:::aws_ec2_server
```

#### Creating the Configuration File

Use the following heredoc below:
```bash
mkdir -p config0

cat > config0/contrib_repo.yml << 'EOF'
assets:
  execgroups:
    - name: ec2_server
      app_name: terraform
      folder: terraform
  stacks:
    - name: aws_ec2_server
      folder: stacks
EOF
```

This explicit approach is the quickest way to get started to import the Terraform code as a Config0 execgroup and the Config0 stack that refers to this Terraform code. 

The implicit approach is the easiest way to manage and scale the imports moving forward. This will be featured and shown in other tutorials.

### 6. Submit Changes to Config0
After completing these steps, check in your code and have Config0 evaluate this repository for additions/changes.
It will find a new execgroup and a new stack.

## Validation
After submitting your changes, you should see:
- A new execgroup available in Config0
- A new stack available for use in your Config0 environment

## Next Steps
Once your integration is complete, you can:
- Execute the Terraform code through Config0 launch yml `config0/config0.yml`
- Use the stack in automation workflows
- Share it with your team for reuse

[^1]: Change "williaumwu" to your Github username if you're doing this demo.
[^2]: Note: Stacks are first class citizens so do not contain the repository name.

