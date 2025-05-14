from config0_publisher.terraform import TFConstructor


def run(stackargs):

    # instantiate authoring stack
    stack = newStack(stackargs)

    # Add default variables
    stack.parse.add_required(key="hostname",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_required(key="ssh_key_name",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_optional(key="aws_default_region",
                             default="us-east-1",
                             tags="tfvar,db,resource,tf_exec_env",
                             types="str")
    
    stack.parse.add_optional(key="ami",
                             default="ami-055750c183ca68c38",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_optional(key="associate_public_ip_address",
                             default=True,
                             tags="tfvar,db",
                             types="bool")
    
    stack.parse.add_optional(key="instance_type",
                             default="t3.micro",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_optional(key="disktype",
                             default="gp2",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_optional(key="disksize",
                             default="20",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_required(key="user_data",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_optional(key="ami_filter",
                             default="ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_optional(key="ami_owner",
                             default="099720109477",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_required(key="iam_instance_profile",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_required(key="subnet_id",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_required(key="security_group_ids",
                             tags="tfvar,db",
                             types="str")
    
    stack.parse.add_optional(key="cloud_tags",
                             default={},
                             tags="tfvar,db",
                             types="dict")
    
    # Add execgroup
    stack.add_execgroup("williaumwu:::demo1-aws_ec2_server::ec2_server",
                        "tf_execgroup")

    # Add substack
    stack.add_substack('config0-publish:::tf_executor')

    # Initialize
    stack.init_variables()
    stack.init_execgroups()
    stack.init_substacks()

    stack.set_variable("timeout", 600)

    # use the terraform constructor (helper)
    tf = TFConstructor(stack=stack,
                       execgroup_name=stack.tf_execgroup.name,
                       provider="aws",
                       tf_runtime="tofu:1.9.1",
                       resource_name=FIX ME,
                       resource_type="server")

    # finalize the tf_executor
    stack.tf_executor.insert(display=True,
                             **tf.get())

    return stack.get_results()
