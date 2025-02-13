# Copyright 2019 The resource-policy-evaluation-library Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import collections
import pytest

from rpe.resources import Resource
from rpe.resources.gcp import GcpBigqueryDataset
from rpe.resources.gcp import GcpComputeInstance
from rpe.resources.gcp import GcpProject
from rpe.resources.gcp import GcpProjectIam
from rpe.resources.gcp import GcpPubsubSubscription
from rpe.resources.gcp import GcpPubsubSubscriptionIam
from rpe.resources.gcp import GcpPubsubTopic
from rpe.resources.gcp import GcpPubsubTopicIam
from rpe.resources.gcp import GcpSqlInstance
from rpe.resources.gcp import GcpStorageBucket
from rpe.resources.gcp import GcpStorageBucketIamPolicy

test_project = "my_project"
test_resource_name = "my_resource"

ResourceTestCase = collections.namedtuple('ResourceTestCase', 'input cls type name')

test_cases = [
    ResourceTestCase(
        input={
            'resource_type': 'bigquery.datasets',
            'resource_name': test_resource_name,
            'project_id': test_project
        },
        cls=GcpBigqueryDataset,
        type='gcp.bigquery.datasets',
        name='//bigquery.googleapis.com/projects/my_project/datasets/my_resource'
    ),
    ResourceTestCase(
        input={
            'resource_type': 'compute.instances',
            'resource_name': test_resource_name,
            'resource_location': 'us-central1-a',
            'project_id': test_project
        },
        cls=GcpComputeInstance,
        type='gcp.compute.instances',
        name='//compute.googleapis.com/projects/my_project/zones/us-central1-a/instances/my_resource'
    ),
    ResourceTestCase(
        input={
            'resource_type': 'cloudresourcemanager.projects',
            'resource_name': test_project,
            'project_id': test_project
        },
        cls=GcpProject,
        type='gcp.cloudresourcemanager.projects',
        name='//cloudresourcemanager.googleapis.com/projects/my_project'
    ),
    ResourceTestCase(
        input={
            'resource_type': 'cloudresourcemanager.projects.iam',
            'resource_name': test_project,
            'project_id': test_project
        },
        cls=GcpProjectIam,
        type='gcp.cloudresourcemanager.projects.iam',
        name='//cloudresourcemanager.googleapis.com/projects/my_project'
    ),
    ResourceTestCase(
        input={
            'resource_type': 'pubsub.projects.subscriptions',
            'resource_name': test_resource_name,
            'project_id': test_project
        },
        cls=GcpPubsubSubscription,
        type='gcp.pubsub.projects.subscriptions',
        name='//pubsub.googleapis.com/projects/my_project/subscriptions/my_resource'
    ),
    ResourceTestCase(
        input={
            'resource_type': 'pubsub.projects.subscriptions.iam',
            'resource_name': test_resource_name,
            'project_id': test_project
        },
        cls=GcpPubsubSubscriptionIam,
        type='gcp.pubsub.projects.subscriptions.iam',
        name='//pubsub.googleapis.com/projects/my_project/subscriptions/my_resource'
    ),
    ResourceTestCase(
        input={
            'resource_type': 'pubsub.projects.topics',
            'resource_name': test_resource_name,
            'project_id': test_project
        },
        cls=GcpPubsubTopic,
        type='gcp.pubsub.projects.topics',
        name='//pubsub.googleapis.com/projects/my_project/topics/my_resource'
    ),
    ResourceTestCase(
        input={
            'resource_type': 'pubsub.projects.topics.iam',
            'resource_name': test_resource_name,
            'project_id': test_project
        },
        cls=GcpPubsubTopicIam,
        type='gcp.pubsub.projects.topics.iam',
        name='//pubsub.googleapis.com/projects/my_project/topics/my_resource'
    ),
    ResourceTestCase(
        input={
            'resource_type': 'sqladmin.instances',
            'resource_name': test_resource_name,
            'project_id': test_project
        },
        cls=GcpSqlInstance,
        type='gcp.sqladmin.instances',
        name='//sql.googleapis.com/projects/my_project/instances/my_resource'
    ),
    ResourceTestCase(
        input={
            'resource_type': 'storage.buckets',
            'resource_name': test_resource_name,
            'project_id': test_project
        },
        cls=GcpStorageBucket,
        type='gcp.storage.buckets',
        name='//storage.googleapis.com/buckets/my_resource'
    ),
    ResourceTestCase(
        input={
            'resource_type': 'storage.buckets.iam',
            'resource_name': test_resource_name,
            'project_id': test_project
        },
        cls=GcpStorageBucketIamPolicy,
        type='gcp.storage.buckets.iam',
        name='//storage.googleapis.com/buckets/my_resource'
    )
]


@pytest.mark.parametrize(
    "case",
    test_cases,
    ids=[case.cls.__name__ for case in test_cases])
def test_gcp_resource_factory(case):
    r = Resource.factory("gcp", case.input)
    assert r.__class__ == case.cls
    assert r.type() == case.type


def test_gcp_resource_factory_invalid():
    with pytest.raises(AssertionError):
        Resource.factory('gcp', {})


@pytest.mark.parametrize(
    "case",
    test_cases,
    ids=[case.cls.__name__ for case in test_cases])
def test_gcp_full_resource_name(case):
    r = Resource.factory("gcp", case.input)
    assert r.full_resource_name() == case.name
