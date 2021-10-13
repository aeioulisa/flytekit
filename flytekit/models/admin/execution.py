import flyteidl.admin.execution_pb2 as _execution_pb2
import flyteidl.admin.node_execution_pb2 as _node_execution_pb2
import flyteidl.admin.task_execution_pb2 as _task_execution_pb2
import pytz as _pytz

from flytekit.models import common as _common_models
from flytekit.models import literals as _literals_models
from flytekit.models.core import execution as _core_execution
from flytekit.models.core import identifier as _identifier


class ExecutionMetadata(_common_models.FlyteIdlEntity):
    class ExecutionMode(object):
        MANUAL = 0
        SCHEDULED = 1
        SYSTEM = 2

    def __init__(self, mode, principal, nesting):
        """
        :param int mode: An enum value from ExecutionMetadata.ExecutionMode which specifies how the job started.
        :param Text principal: The entity that triggered the execution
        :param int nesting: An integer representing how deeply nested the workflow is (i.e. was it triggered by a parent
            workflow)
        """
        self._mode = mode
        self._principal = principal
        self._nesting = nesting

    @property
    def mode(self):
        """
        An enum value from ExecutionMetadata.ExecutionMode which specifies how the job started.
        :rtype: int
        """
        return self._mode

    @property
    def principal(self):
        """
        The entity that triggered the execution
        :rtype: Text
        """
        return self._principal

    @property
    def nesting(self):
        """
        An integer representing how deeply nested the workflow is (i.e. was it triggered by a parent workflow)
        :rtype: int
        """
        return self._nesting

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.admin.execution_pb2.ExecutionMetadata
        """
        return _execution_pb2.ExecutionMetadata(mode=self.mode, principal=self.principal, nesting=self.nesting)

    @classmethod
    def from_flyte_idl(cls, pb2_object):
        """
        :param flyteidl.admin.execution_pb2.ExecutionMetadata pb2_object:
        :return: ExecutionMetadata
        """
        return cls(
            mode=pb2_object.mode,
            principal=pb2_object.principal,
            nesting=pb2_object.nesting,
        )


class ExecutionSpec(_common_models.FlyteIdlEntity):
    def __init__(
        self,
        launch_plan,
        metadata,
        notifications=None,
        disable_all=None,
        labels=None,
        annotations=None,
        auth_role=None,
        max_parallelism=None,
    ):
        """
        :param flytekit.models.core.identifier.Identifier launch_plan: Launch plan unique identifier to execute
        :param ExecutionMetadata metadata: The metadata to be associated with this execution
        :param NotificationList notifications: List of notifications for this execution.
        :param bool disable_all: If true, all notifications should be disabled.
        :param flytekit.models.common.Labels labels: Labels to apply to the execution.
        :param flytekit.models.common.Annotations annotations: Annotations to apply to the execution
        :param flytekit.models.common.AuthRole auth_role: The authorization method with which to execute the workflow.
        :param max_parallelism int: Controls the maximum number of tasknodes that can be run in parallel for the entire
            workflow. This is useful to achieve fairness. Note: MapTasks are regarded as one unit, and
            parallelism/concurrency of MapTasks is independent from this.

        """
        self._launch_plan = launch_plan
        self._metadata = metadata
        self._notifications = notifications
        self._disable_all = disable_all
        self._labels = labels or _common_models.Labels({})
        self._annotations = annotations or _common_models.Annotations({})
        self._auth_role = auth_role or _common_models.AuthRole()
        self._max_parallelism = max_parallelism

    @property
    def launch_plan(self):
        """
        If the values were too large, this is the URI where the values were offloaded.
        :rtype: flytekit.models.core.identifier.Identifier
        """
        return self._launch_plan

    @property
    def metadata(self):
        """
        :rtype: ExecutionMetadata
        """
        return self._metadata

    @property
    def notifications(self):
        """
        :rtype: Optional[NotificationList]
        """
        return self._notifications

    @property
    def disable_all(self):
        """
        :rtype: Optional[bool]
        """
        return self._disable_all

    @property
    def labels(self):
        """
        :rtype: flytekit.models.common.Labels
        """
        return self._labels

    @property
    def annotations(self):
        """
        :rtype: flytekit.models.common.Annotations
        """
        return self._annotations

    @property
    def auth_role(self):
        """
        :rtype: flytekit.models.common.AuthRole
        """
        return self._auth_role

    @property
    def max_parallelism(self) -> int:
        return self._max_parallelism

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.admin.execution_pb2.ExecutionSpec
        """
        return _execution_pb2.ExecutionSpec(
            launch_plan=self.launch_plan.to_flyte_idl(),
            metadata=self.metadata.to_flyte_idl(),
            notifications=self.notifications.to_flyte_idl() if self.notifications else None,
            disable_all=self.disable_all,
            labels=self.labels.to_flyte_idl(),
            annotations=self.annotations.to_flyte_idl(),
            auth_role=self._auth_role.to_flyte_idl() if self.auth_role else None,
            max_parallelism=self.max_parallelism,
        )

    @classmethod
    def from_flyte_idl(cls, p):
        """
        :param flyteidl.admin.execution_pb2.ExecutionSpec p:
        :return: ExecutionSpec
        """
        return cls(
            launch_plan=_identifier.Identifier.from_flyte_idl(p.launch_plan),
            metadata=ExecutionMetadata.from_flyte_idl(p.metadata),
            notifications=NotificationList.from_flyte_idl(p.notifications) if p.HasField("notifications") else None,
            disable_all=p.disable_all if p.HasField("disable_all") else None,
            labels=_common_models.Labels.from_flyte_idl(p.labels),
            annotations=_common_models.Annotations.from_flyte_idl(p.annotations),
            auth_role=_common_models.AuthRole.from_flyte_idl(p.auth_role),
            max_parallelism=p.max_parallelism,
        )


class LiteralMapBlob(_common_models.FlyteIdlEntity):
    def __init__(self, values=None, uri=None):
        """
        :param flytekit.models.literals.LiteralMap values:
        :param Text uri:
        """
        self._values = values
        self._uri = uri

    @property
    def values(self):
        """
        :rtype: flytekit.models.literals.LiteralMap
        """
        return self._values

    @property
    def uri(self):
        """
        :rtype: Text
        """
        return self._uri

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.admin.execution_pb2.LiteralMapBlob
        """
        return _execution_pb2.LiteralMapBlob(
            values=self.values.to_flyte_idl() if self.values is not None else None,
            uri=self.uri,
        )

    @classmethod
    def from_flyte_idl(cls, pb):
        """
        :param flyteidl.admin.execution_pb2.LiteralMapBlob pb:
        :rtype: LiteralMapBlob
        """
        values = None
        if pb.HasField("values"):
            values = LiteralMapBlob.from_flyte_idl(pb.values)
        return cls(values=values, uri=pb.uri if pb.HasField("uri") else None)


class Execution(_common_models.FlyteIdlEntity):
    def __init__(self, id, spec, closure):
        """
        :param flytekit.models.core.identifier.WorkflowExecutionIdentifier id:
        :param Text id:
        :param ExecutionSpec spec:
        :param ExecutionClosure closure:
        """
        self._id = id
        self._spec = spec
        self._closure = closure

    @property
    def id(self):
        """
        :rtype: flytekit.models.core.identifier.WorkflowExecutionIdentifier
        """
        return self._id

    @property
    def closure(self):
        """
        :rtype: ExecutionClosure
        """
        return self._closure

    @property
    def spec(self):
        """
        :rtype: ExecutionSpec
        """
        return self._spec

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.admin.execution_pb2.Execution
        """
        return _execution_pb2.Execution(
            id=self.id.to_flyte_idl(),
            closure=self.closure.to_flyte_idl(),
            spec=self.spec.to_flyte_idl(),
        )

    @classmethod
    def from_flyte_idl(cls, pb):
        """
        :param flyteidl.admin.execution_pb2.Execution pb:
        :rtype: Execution
        """
        return cls(
            id=_identifier.WorkflowExecutionIdentifier.from_flyte_idl(pb.id),
            closure=ExecutionClosure.from_flyte_idl(pb.closure),
            spec=ExecutionSpec.from_flyte_idl(pb.spec),
        )


class ExecutionClosure(_common_models.FlyteIdlEntity):
    def __init__(self, phase, started_at, error=None, outputs=None):
        """
        :param int phase: From the flytekit.models.core.execution.WorkflowExecutionPhase enum
        :param datetime.datetime started_at:
        :param flytekit.models.core.execution.ExecutionError error:
        :param LiteralMapBlob outputs:
        """
        self._phase = phase
        self._started_at = started_at
        self._error = error
        self._outputs = outputs

    @property
    def error(self):
        """
        :rtype: flytekit.models.core.execution.ExecutionError
        """
        return self._error

    @property
    def phase(self):
        """
        From the flytekit.models.core.execution.WorkflowExecutionPhase enum
        :rtype: int
        """
        return self._phase

    @property
    def started_at(self):
        """
        :rtype: datetime.datetime
        """
        return self._started_at

    @property
    def outputs(self):
        """
        :rtype: LiteralMapBlob
        """
        return self._outputs

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.admin.execution_pb2.ExecutionClosure
        """
        obj = _execution_pb2.ExecutionClosure(
            phase=self.phase,
            error=self.error.to_flyte_idl() if self.error is not None else None,
            outputs=self.outputs.to_flyte_idl() if self.outputs is not None else None,
        )
        obj.started_at.FromDatetime(self.started_at.astimezone(_pytz.UTC).replace(tzinfo=None))
        return obj

    @classmethod
    def from_flyte_idl(cls, pb2_object):
        """
        :param flyteidl.admin.execution_pb2.ExecutionClosure pb2_object:
        :rtype: ExecutionClosure
        """
        error = None
        if pb2_object.HasField("error"):
            error = _core_execution.ExecutionError.from_flyte_idl(pb2_object.error)
        outputs = None
        if pb2_object.HasField("outputs"):
            outputs = LiteralMapBlob.from_flyte_idl(pb2_object.outputs)
        return cls(
            error=error,
            outputs=outputs,
            phase=pb2_object.phase,
            started_at=pb2_object.started_at.ToDatetime().replace(tzinfo=_pytz.UTC),
        )


class TaskExecutionClosure(_common_models.FlyteIdlEntity):
    def __init__(
        self,
        phase,
        logs,
        started_at,
        duration,
        created_at,
        updated_at,
        output_uri=None,
        error=None,
    ):
        """
        :param int phase: Enum value from flytekit.models.core.execution.TaskExecutionPhase
        :param list[flytekit.models.core.execution.TaskLog] logs: List of all logs associated with the execution.
        :param datetime.datetime started_at:
        :param datetime.timedelta duration:
        :param datetime.datetime created_at:
        :param datetime.datetime updated_at:
        :param Text output_uri: If task is successful and in terminal state, this will be the path to the output
            literals.
        :param flytekit.models.core.execution.ExecutionError error: If task has failed and in terminal state, this will
            be set to the error encountered.
        """
        self._phase = phase
        self._logs = logs
        self._started_at = started_at
        self._duration = duration
        self._created_at = created_at
        self._updated_at = updated_at
        self._output_uri = output_uri
        self._error = error

    @property
    def phase(self):
        """
        Enum value from flytekit.models.core.execution.TaskExecutionPhase
        :rtype: int
        """
        return self._phase

    @property
    def logs(self):
        """
        :rtype: list[flytekit.models.core.execution.TaskLog]
        """
        return self._logs

    @property
    def started_at(self):
        """
        :rtype: datetime.datetime
        """
        return self._started_at

    @property
    def created_at(self):
        """
        :rtype: datetime.datetime
        """
        return self._created_at

    @property
    def updated_at(self):
        """
        :rtype: datetime.datetime
        """
        return self._updated_at

    @property
    def duration(self):
        """
        :rtype: datetime.timedelta
        """
        return self._duration

    @property
    def output_uri(self):
        """
        :rtype: Text
        """
        return self._output_uri

    @property
    def error(self):
        """
        :rtype: flytekit.models.core.execution.ExecutionError
        """
        return self._error

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.admin.task_execution_pb2.TaskExecutionClosure
        """
        p = _task_execution_pb2.TaskExecutionClosure(
            phase=self.phase,
            logs=[l.to_flyte_idl() for l in self.logs],
            output_uri=self.output_uri,
            error=self.error.to_flyte_idl() if self.error is not None else None,
        )
        p.started_at.FromDatetime(self.started_at)
        p.created_at.FromDatetime(self.created_at)
        p.updated_at.FromDatetime(self.updated_at)
        p.duration.FromTimedelta(self.duration)
        return p

    @classmethod
    def from_flyte_idl(cls, p):
        """
        :param flyteidl.admin.task_execution_pb2.TaskExecutionClosure p:
        :rtype: TaskExecutionClosure
        """
        return cls(
            phase=p.phase,
            logs=[_core_execution.TaskLog.from_flyte_idl(l) for l in p.logs],
            output_uri=p.output_uri if p.HasField("output_uri") else None,
            error=_core_execution.ExecutionError.from_flyte_idl(p.error) if p.HasField("error") else None,
            started_at=p.started_at.ToDatetime(),
            created_at=p.created_at.ToDatetime(),
            updated_at=p.updated_at.ToDatetime(),
            duration=p.duration.ToTimedelta(),
        )


class TaskExecution(_common_models.FlyteIdlEntity):
    def __init__(self, id, input_uri, closure, is_parent):
        """
        :param flytekit.models.core.identifier.TaskExecutionIdentifier id:
        :param Text input_uri:
        :param TaskExecutionClosure closure:
        :param bool is_parent:
        """
        self._id = id
        self._input_uri = input_uri
        self._closure = closure
        self._is_parent = is_parent

    @property
    def id(self):
        """
        :rtype: flytekit.models.core.identifier.TaskExecutionIdentifier
        """
        return self._id

    @property
    def input_uri(self):
        """
        :rtype: Text
        """
        return self._input_uri

    @property
    def closure(self):
        """
        :rtype: TaskExecutionClosure
        """
        return self._closure

    @property
    def is_parent(self):
        """
        :rtype: bool
        """
        return self._is_parent

    def to_flyte_idl(self):
        """
        :rtype: flyteidl.admin.task_execution_pb2.TaskExecution
        """
        return _task_execution_pb2.TaskExecution(
            id=self.id.to_flyte_idl(),
            input_uri=self.input_uri,
            closure=self.closure.to_flyte_idl(),
            is_parent=self.is_parent,
        )

    @classmethod
    def from_flyte_idl(cls, proto):
        """
        :param flyteidl.admin.task_execution_pb2.TaskExecution proto:
        :rtype: TaskExecution
        """
        return cls(
            id=_identifier.TaskExecutionIdentifier.from_flyte_idl(proto.id),
            input_uri=proto.input_uri,
            closure=TaskExecutionClosure.from_flyte_idl(proto.closure),
            is_parent=proto.is_parent,
        )


class NotificationList(_common_models.FlyteIdlEntity):
    def __init__(self, notifications):
        """
        :param list[flytekit.models.common.Notification] notifications: A simple list of notifications.
        """
        self._notifications = notifications

    @property
    def notifications(self):
        """
        :rtype: list[flytekit.models.common.Notification]
        """
        return self._notifications

    def to_flyte_idl(self):
        """
        :rtype:  flyteidl.admin.execution_pb2.NotificationList
        """
        return _execution_pb2.NotificationList(notifications=[n.to_flyte_idl() for n in self.notifications])

    @classmethod
    def from_flyte_idl(cls, pb2_object):
        """
        :param flyteidl.admin.execution_pb2.NotificationList pb2_object:
        :rtype: NotificationList
        """
        return cls([_common_models.Notification.from_flyte_idl(p) for p in pb2_object.notifications])


class _CommonDataResponse(_common_models.FlyteIdlEntity):
    """
    Currently, node, task, and workflow execution all have the same get data response. So we'll create this common
    superclass to reduce code duplication until things diverge in the future.
    """

    def __init__(self, inputs, outputs, full_inputs, full_outputs):
        """
        :param _common_models.UrlBlob inputs:
        :param _common_models.UrlBlob outputs:
        :param _literals_pb2.LiteralMap full_inputs:
        :param _literals_pb2.LiteralMap full_outputs:
        """
        self._inputs = inputs
        self._outputs = outputs
        self._full_inputs = full_inputs
        self._full_outputs = full_outputs

    @property
    def inputs(self):
        """
        :rtype: _common_models.UrlBlob
        """
        return self._inputs

    @property
    def outputs(self):
        """
        :rtype: _common_models.UrlBlob
        """
        return self._outputs

    @property
    def full_inputs(self):
        """
        :rtype: _literals_pb2.LiteralMap
        """
        return self._full_inputs

    @property
    def full_outputs(self):
        """
        :rtype: _literals_pb2.LiteralMap
        """
        return self._full_outputs


class WorkflowExecutionGetDataResponse(_CommonDataResponse):
    @classmethod
    def from_flyte_idl(cls, pb2_object):
        """
        :param _execution_pb2.WorkflowExecutionGetDataResponse pb2_object:
        :rtype: WorkflowExecutionGetDataResponse
        """
        return cls(
            inputs=_common_models.UrlBlob.from_flyte_idl(pb2_object.inputs),
            outputs=_common_models.UrlBlob.from_flyte_idl(pb2_object.outputs),
            full_inputs=_literals_models.LiteralMap.from_flyte_idl(pb2_object.full_inputs),
            full_outputs=_literals_models.LiteralMap.from_flyte_idl(pb2_object.full_outputs),
        )

    def to_flyte_idl(self):
        """
        :rtype: _execution_pb2.WorkflowExecutionGetDataResponse
        """
        return _execution_pb2.WorkflowExecutionGetDataResponse(
            inputs=self.inputs.to_flyte_idl(),
            outputs=self.outputs.to_flyte_idl(),
            full_inputs=self.full_inputs.to_flyte_idl(),
            full_outputs=self.full_outputs.to_flyte_idl(),
        )


class TaskExecutionGetDataResponse(_CommonDataResponse):
    @classmethod
    def from_flyte_idl(cls, pb2_object):
        """
        :param _task_execution_pb2.TaskExecutionGetDataResponse pb2_object:
        :rtype: TaskExecutionGetDataResponse
        """
        return cls(
            inputs=_common_models.UrlBlob.from_flyte_idl(pb2_object.inputs),
            outputs=_common_models.UrlBlob.from_flyte_idl(pb2_object.outputs),
            full_inputs=_literals_models.LiteralMap.from_flyte_idl(pb2_object.full_inputs),
            full_outputs=_literals_models.LiteralMap.from_flyte_idl(pb2_object.full_outputs),
        )

    def to_flyte_idl(self):
        """
        :rtype: _task_execution_pb2.TaskExecutionGetDataResponse
        """
        return _task_execution_pb2.TaskExecutionGetDataResponse(
            inputs=self.inputs.to_flyte_idl(),
            outputs=self.outputs.to_flyte_idl(),
            full_inputs=self.full_inputs.to_flyte_idl(),
            full_outputs=self.full_outputs.to_flyte_idl(),
        )


class NodeExecutionGetDataResponse(_CommonDataResponse):
    @classmethod
    def from_flyte_idl(cls, pb2_object):
        """
        :param _node_execution_pb2.NodeExecutionGetDataResponse pb2_object:
        :rtype: NodeExecutionGetDataResponse
        """
        return cls(
            inputs=_common_models.UrlBlob.from_flyte_idl(pb2_object.inputs),
            outputs=_common_models.UrlBlob.from_flyte_idl(pb2_object.outputs),
            full_inputs=_literals_models.LiteralMap.from_flyte_idl(pb2_object.full_inputs),
            full_outputs=_literals_models.LiteralMap.from_flyte_idl(pb2_object.full_outputs),
        )

    def to_flyte_idl(self):
        """
        :rtype: _node_execution_pb2.NodeExecutionGetDataResponse
        """
        return _node_execution_pb2.NodeExecutionGetDataResponse(
            inputs=self.inputs.to_flyte_idl(),
            outputs=self.outputs.to_flyte_idl(),
            full_inputs=self.full_inputs.to_flyte_idl(),
            full_outputs=self.full_outputs.to_flyte_idl(),
        )
