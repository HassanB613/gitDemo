import os
import boto3

def test_aws_identity():
    region = os.environ.get("AWS_REGION", "us-east-1")
    sts = boto3.client("sts", region_name=region)
    ident = sts.get_caller_identity()
    print("CallerIdentity:", ident)
    assert "Arn" in ident
