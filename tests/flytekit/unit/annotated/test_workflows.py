import typing

import pytest

from flytekit.annotated import context_manager
from flytekit.annotated.context_manager import Image, ImageConfig
from flytekit.annotated.task import task
from flytekit.annotated.workflow import WorkflowFailurePolicy, WorkflowMetadata, WorkflowMetadataDefaults, workflow
from flytekit.common.exceptions.user import FlyteValidationException


def test_metadata_values():
    with pytest.raises(FlyteValidationException):
        WorkflowMetadata(on_failure=0)

    wm = WorkflowMetadata(on_failure=WorkflowFailurePolicy.FAIL_IMMEDIATELY)
    assert wm.on_failure == WorkflowFailurePolicy.FAIL_IMMEDIATELY


def test_default_metadata_values():
    with pytest.raises(FlyteValidationException):
        WorkflowMetadataDefaults(3)

    wm = WorkflowMetadataDefaults(interruptible=False)
    assert wm.interruptible is False


def test_workflow_values():
    @task
    def t1(a: int) -> typing.NamedTuple("OutputsBC", t1_int_output=int, c=str):
        a = a + 2
        return a, "world-" + str(a)

    @workflow(interruptible=True, failure_policy=WorkflowFailurePolicy.FAIL_AFTER_EXECUTABLE_NODES_COMPLETE)
    def wf(a: int) -> (str, str):
        x, y = t1(a=a)
        u, v = t1(a=x)
        return y, v

    registration_settings = context_manager.RegistrationSettings(
        project="proj",
        domain="dom",
        version="123",
        image_config=ImageConfig(Image(name="name", fqn="asdf/fdsa", tag="123")),
        env={},
        iam_role="test:iam:role",
        service_account=None,
    )
    with context_manager.FlyteContext.current_context().new_registration_settings(
        registration_settings=registration_settings
    ):
        sdk_wf = wf.get_registerable_entity()
        assert sdk_wf.metadata_defaults.interruptible
        assert sdk_wf.metadata.on_failure == 1
