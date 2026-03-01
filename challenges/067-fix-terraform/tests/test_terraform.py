"""Tests for Challenge 067: Fix Terraform Config."""

import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "setup"))

TF_PATH = Path(__file__).parent.parent / "setup" / "main.tf"


def read_tf():
    return TF_PATH.read_text()


def get_resource_blocks(content):
    return re.findall(r'resource\s+"(\w+)"\s+"(\w+)"', content)


def get_variable_blocks(content):
    return re.findall(r'variable\s+"(\w+)"', content)


def get_variable_usages(content):
    return re.findall(r'var\.(\w+)', content)


def test_no_circular_references():
    content = read_tf()
    resources = get_resource_blocks(content)
    resource_names = {f"{rtype}.{rname}" for rtype, rname in resources}

    deps = {}
    for rtype, rname in resources:
        block_pattern = rf'resource\s+"{rtype}"\s+"{rname}"\s*\{{(.*?)\n\}}'
        match = re.search(block_pattern, content, re.DOTALL)
        if match:
            body = match.group(1)
            refs = set()
            for ref_match in re.finditer(r'(aws_\w+)\.(\w+)\.', body):
                ref_name = f"{ref_match.group(1)}.{ref_match.group(2)}"
                if ref_name in resource_names:
                    refs.add(ref_name)
            deps[f"{rtype}.{rname}"] = refs

    for res_a, deps_a in deps.items():
        for dep in deps_a:
            deps_of_dep = deps.get(dep, set())
            assert res_a not in deps_of_dep, \
                f"Circular reference: {res_a} <-> {dep}"


def test_all_variables_declared():
    content = read_tf()
    declared = set(get_variable_blocks(content))
    used = set(get_variable_usages(content))
    undeclared = used - declared
    assert len(undeclared) == 0, \
        f"Variables used but not declared: {undeclared}"


def test_resource_type_names_valid():
    content = read_tf()
    resources = get_resource_blocks(content)
    for rtype, rname in resources:
        assert "_" in rtype, \
            f"Resource type '{rtype}' should follow provider_resource format"
        assert rtype.startswith("aws_"), \
            f"Resource type '{rtype}' should start with 'aws_' for AWS provider"


def test_ec2_instance_resource_type():
    content = read_tf()
    assert 'resource "aws_instance"' in content, \
        "EC2 instance must use 'aws_instance' resource type, not 'ec2_instance'"
    assert 'resource "ec2_instance"' not in content, \
        "Must not use 'ec2_instance' (invalid resource type)"


def test_outputs_reference_valid_resources():
    content = read_tf()
    resources = get_resource_blocks(content)
    resource_keys = {f"{rtype}.{rname}" for rtype, rname in resources}

    output_refs = re.findall(r'value\s*=\s*(aws_\w+\.\w+)', content)
    for ref in output_refs:
        assert ref in resource_keys, \
            f"Output references '{ref}' which is not a declared resource"


def test_subnet_references_vpc_directly():
    content = read_tf()
    subnet_match = re.search(
        r'resource\s+"aws_subnet"\s+"\w+"\s*\{(.*?)\n\}', content, re.DOTALL
    )
    assert subnet_match, "Must have an aws_subnet resource"
    subnet_body = subnet_match.group(1)
    assert "aws_vpc" in subnet_body, \
        "Subnet vpc_id should reference the VPC resource directly"


def test_security_group_references_vpc_directly():
    content = read_tf()
    sg_match = re.search(
        r'resource\s+"aws_security_group"\s+"\w+"\s*\{(.*?)\n\}', content, re.DOTALL
    )
    assert sg_match, "Must have an aws_security_group resource"
    sg_body = sg_match.group(1)
    assert "aws_vpc" in sg_body, \
        "Security group vpc_id should reference the VPC resource directly"


def test_provider_configured():
    content = read_tf()
    assert re.search(r'provider\s+"aws"', content), \
        "Must have an AWS provider block"
