# Integrating Terraform Code with Config0

## Overview
This guide explains how to integrate your existing Terraform code into Config0 to create end-to-end developer solutions with single entry points. This includes:
- Terraform to Terraform connections
- Terraform to Ansible connections

## Getting Started
We'll begin by assuming you have existing Terraform code in place.

### Existing Resources
- **Repositories**:
  - Terraform repository "demo1-aws_ssh_keys" for SSH key generation and upload
  - Terraform repository "demo1-aws_ec2_server" for EC2 server creation
  - Ansible playbook "demo1-jenkins" for Jenkins installation

## Example: Integrating demo1-aws_ec2_server

If you have simple Terraform code in the "terraform" folder, follow these steps to create a stack:

### 1. Download Config0's Helper Stack Generation Script
```bash
curl https://raw.githubusercontent.com/config0-hub/config0_publisher/main/config0_publisher/bin/stack_gen -o /tmp/stack_gen
chmod 755 /tmp/stack_gen
```

### 2. Create Configuration File
The easiest approach is to create a config.yml file using a heredoc:

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

### 3. Create the stack

```bash
/tmp/stack_gen -c /tmp/stackgen-ec2-server.yml 
```

### 4. Replace "FIX ME" with stack.hostname 

```bash
sed -i 's/FIX ME/stack.hostname/g' stacks/aws_ec2_server/_main/run.py
```

### 5. Create contrib_repo.yml in config0 folder

This is the quickest way to get started, although there is an implicit approach that will be presented later.

We'll first provide an explicit configuration with config0/contrib_repo.yml:
- For execgroup (execution group which is a group of files like Terraform that are executed together):
  - "ec2_server" is the name of the execgroup
  - "terraform" is the application name (other examples include ansible, pulumi, cloudformation)
  - "terraform" is the folder where the Terraform files are located
- For stack (entry point for this Terraform code):
  - "aws_ec2_server" is the name of this stack
  - "stacks" is where the stack files are found

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

After completing these steps:
1. Check in your code and have Config0 evaluate this repository for additions/changes
2. This Terraform code and its execution now becomes:
   - Immutable
   - Portable
   - Easily reusable by other upstream Terraform and DevOps code