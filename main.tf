# main.tf

# Provider configuration for AWS
provider "aws" {
  region = "us-east-1"
}

# VPC configuration
resource "aws_vpc" "my_vpc" {
  cidr_block = "10.0.0.0/16" 
}

# Subnet configuration
resource "aws_subnet" "public_subnet" {
  vpc_id            = aws_vpc.my_vpc.id  
  cidr_block        = "10.0.1.0/24"     
  availability_zone = "us-east-1a"      
}

# Internet Gateway configuration
resource "aws_internet_gateway" "my_igw" {
  vpc_id = aws_vpc.my_vpc.id
}


# Route Table configuration
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.my_vpc.id 

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.my_igw.id
  }
}

# Associate Route Table with Subnet
resource "aws_route_table_association" "public_subnet_association" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public_route_table.id
}

# Security Group configuration
resource "aws_security_group" "ssh_sg" {
  vpc_id = aws_vpc.my_vpc.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance configuration
resource "aws_instance" "gen-AI-study-ec2-instance" {
  ami               = "ami-080e1f13689e07408"  # ubuntu 22.04LTS
  instance_type     = "t3.xlarge"
  key_name          = "my-nvkp"

  root_block_device {
    volume_size = 100  // Set the root volume size to 100GB - required for LLM task (50GB should do)
  }

  subnet_id       = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.ssh_sg.id] 
  associate_public_ip_address = true
  
  tags = {
    Name = "gen-AI-study-ec2-instance"
  }
}


