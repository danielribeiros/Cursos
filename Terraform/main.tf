provider "aws" {
  region = "us-east-1"
  profile = "daribeiro.terraform"
}

##################################################################
# Data sources to get VPC, subnet, security group and AMI details
##################################################################
data "aws_vpc" "default" {
  default = true
}

data "aws_subnet_ids" "all" {
  vpc_id = "${data.aws_vpc.default.id}"
}

data "aws_ami" "amazon_linux" {
  most_recent = true

  filter {
    name = "name"

    values = [
      "amzn-ami-hvm-*-x86_64-gp2",
    ]
  }

  filter {
    name = "owner-alias"

    values = [
      "amazon",
    ]
  }
}

module "security_group" {
  source      = "terraform-aws-modules/security-group/aws"
  version     = "2.7.0"

  name        = "terraform"
  description = "Security group for example usage with EC2 instance and Terraform"
  vpc_id      = "${data.aws_vpc.default.id}"

  ingress_cidr_blocks = ["0.0.0.0/0"]
  ingress_rules       = ["http-80-tcp", "all-icmp", "ssh-22-tcp"]
  egress_rules        = ["all-all"]
}

resource "aws_eip" "this" {
  vpc      = true
  instance = "${module.ec2.id[0]}"
}

module "ec2_instance" {
  source = "github.com/terraform-community-modules/tf_aws_ec2_instance"


  instance_count = 2

  name                        = "ec2_terraform"
  ami                         = "${data.aws_ami.amazon_linux.id}"
  instance_type               = "t2.micro"
  subnet_id                   = "${element(data.aws_subnet_ids.all.ids, 0)}"
  vpc_security_group_ids      = ["${module.security_group.this_security_group_id}"]
  associate_public_ip_address = true
}

// module "ec2_with_t2_unlimited" {
  source = "../../"

  instance_count = 1

  name                        = "example-t2-unlimited"
  ami                         = "${data.aws_ami.amazon_linux.id}"
  instance_type               = "t2.micro"
  cpu_credits                 = "unlimited"
  subnet_id                   = "${element(data.aws_subnet_ids.all.ids, 0)}"
  vpc_security_group_ids      = ["${module.security_group.this_security_group_id}"]
  associate_public_ip_address = true
// }

//module "ec2_with_t3_unlimited" {
  source = "../../"

  instance_count = 1

  name                        = "example-t3-unlimited"
  ami                         = "${data.aws_ami.amazon_linux.id}"
  instance_type               = "t3.large"
  cpu_credits                 = "unlimited"
  subnet_id                   = "${element(data.aws_subnet_ids.all.ids, 0)}"
  vpc_security_group_ids      = ["${module.security_group.this_security_group_id}"]
  associate_public_ip_address = true
//}
