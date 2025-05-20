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
+----------------------+
| terraform/           |
|      data.tf         |
|      main.tf         |
|      outputs.tf      |
|      variables.tf    |
|      provider.tf     |
+----------------------+
            ]
            | terraform code
            | imported as Config0 execgroup
            v
+-----------------------------------------------------------+
| williaumwu:::demo1-aws_ec2_server::ec2_server (execgroup) |
+-----------------------------------------------------------+
            |                         |
            |                         | 
            v                         |
+---------------------------------+   |
| /tmp/stackgen-ec2-server.yml    |   | execgroup
+---------------------------------+   | used by stack
            |                         |
            | stack_gen               |
            | creates                 |
            | Config0 stack           |
            v                         v
+----------------------------------------+
| williaumwu:::aws_ec2_server (stack)    |
+----------------------------------------+
```

## Getting Started
We'll begin by assuming users have existing Terraform code in place.

### Existing Resources
Terraform repository `demo1-aws_ec2_server` (this repository) for EC2 server creation

## Example: Integrating demo1-aws_ec2_server

We have simple Terraform code in the "terraform" folder, follow these steps to create a stack:

### 1. Download Config0's Helper Stack Generation Script
```bash
curl https://raw.githubusercontent.com/config0-hub/config0_publisher/main/config0_publisher/bin/stack_gen -o /tmp/stack_gen
chmod 755 /tmp/stack_gen
```

### 2. Create Configuration File
The easiest approach is to create a config.yml file with these parameters:

- **tf_variables_file**: Location of the terraform variables file
- **execgroup**: A group of files to be executed together (in this case, terraform files). We'll reference this later in `config0/contrib_repo.yml`
- **resource_type**: The user provides the resource_type to summarize the output of the execgroup. In this case, "server" is the only output of this execgroup of Terraform code.
- **timeout**: Maximum execution time in seconds (10 minutes is usually sufficient for server creation)
- **tf_runtime**: The terraform runtime format `<terraform/tofu>:<version>`
- **dest_dir**: Destination directory for the generated Config0 stack
- **stack_name**: Name of the Config0 stack

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

### 4. Replace "FIX ME" with stack.hostname 

The resource name should be dynamically referenced within the stack. In this case, we will use the hostname as the resource name.

```bash
sed -i 's/FIX ME/stack.hostname/g' stacks/aws_ec2_server/_main/run.py
```

### 5. Create contrib_repo.yml

Create the configuration file that maps your existing code to Config0:

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

This explicit approach is the quickest way to get started to import the Terraform code as a Config0 execgroup and the Config0 stack that refers to this Terraform code. The implicit approach is the easiest way to manage and scale the imports moving forward.

After completing these steps, check in your code and have Config0 evaluate this repository for additions/changes.
It will find a new execgroup and a new stack.
