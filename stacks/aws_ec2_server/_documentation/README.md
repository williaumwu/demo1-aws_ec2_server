# aws_ec2_server

A stack that creates server

## Stack Variables

| Variable | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| hostname | string | Yes | Required | Hostname for the EC2 instance, used in Name tag |
| ssh_key_name | string | Yes | Required | Name of the SSH key pair to use for the instance |
| aws_default_region | string | No | "us-east-1" | AWS region where resources will be created |
| ami | string | No | "ami-055750c183ca68c38" | Default AMI ID to use if not using the AMI data source |
| associate_public_ip_address | bool | No | True | Whether to associate a public IP address with the instance |
| instance_type | string | No | "t3.micro" | EC2 instance type |
| disktype | string | No | "gp2" | EBS volume type for the root block device |
| disksize | number | No | 20 | Size of the root EBS volume in GB |
| user_data | string | Yes | Required | Base64 encoded user data to provide when launching the instance |
| ami_filter | string | No | "ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*" | Filter pattern to locate specific AMI |
| ami_owner | string | No | "099720109477" | AWS account ID of the AMI owner (Canonical for Ubuntu) |
| iam_instance_profile | string | Yes | Required | IAM instance profile to attach to the instance |
| subnet_id | string | Yes | Required | VPC Subnet ID to launch the instance in |
| security_group_ids | string | Yes | Required | Comma-separated list of security group IDs to associate with the instance |
| cloud_tags | ${map(string)} | No | {} | Additional tags as a map to apply to all resources |
