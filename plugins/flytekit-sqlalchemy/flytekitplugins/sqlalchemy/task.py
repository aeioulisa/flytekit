import typing
from dataclasses import dataclass

import pandas as pd
from sqlalchemy import create_engine  # type: ignore

import flytekit.models.core.task
from flytekit import current_context, kwtypes
from flytekit.core.base_sql_task import SQLTask
from flytekit.core.context_manager import SerializationSettings
from flytekit.core.python_customized_container_task import PythonCustomizedContainerTask
from flytekit.core.shim_task import ShimTaskExecutor
from flytekit.models.core.security import Secret
from flytekit.types.schema import FlyteSchema


@dataclass
class SQLAlchemyConfig(object):
    """
    Use this configuration to configure task. String should be standard
    sqlalchemy connector format
    (https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls).
    Database can be found:
      - within the container
      - or from a publicly accessible source

    Args:
        uri: default sqlalchemy connector
        connect_args: sqlalchemy kwarg overrides -- ex: host
        secret_connect_args: flyte secrets loaded into sqlalchemy connect args
            -- ex: {"password": flytekit.models.security.Secret(name=SECRET_NAME, group=SECRET_GROUP)}
    """

    uri: str
    connect_args: typing.Optional[typing.Dict[str, typing.Any]] = None
    secret_connect_args: typing.Optional[typing.Dict[str, Secret]] = None

    @staticmethod
    def _secret_to_dict(secret: Secret) -> typing.Dict[str, typing.Optional[str]]:
        return {
            "group": secret.group,
            "key": secret.key,
            "group_version": secret.group_version,
            "mount_requirement": secret.mount_requirement.value,
        }

    def secret_connect_args_to_dicts(self) -> typing.Optional[typing.Dict[str, typing.Dict[str, typing.Optional[str]]]]:
        if self.secret_connect_args is None:
            return None

        secret_connect_args_dicts = {}
        for key, secret in self.secret_connect_args.items():
            secret_connect_args_dicts[key] = self._secret_to_dict(secret)

        return secret_connect_args_dicts


class SQLAlchemyTask(PythonCustomizedContainerTask[SQLAlchemyConfig], SQLTask[SQLAlchemyConfig]):
    """
    Makes it possible to run client side SQLAlchemy queries that optionally return a FlyteSchema object

    TODO: How should we use pre-built containers for running portable tasks like this. Should this always be a
          referenced task type?
    """

    _SQLALCHEMY_TASK_TYPE = "sqlalchemy"

    def __init__(
        self,
        name: str,
        query_template: str,
        task_config: SQLAlchemyConfig,
        inputs: typing.Optional[typing.Dict[str, typing.Type]] = None,
        output_schema_type: typing.Optional[typing.Type[FlyteSchema]] = None,
        container_image: str = "ghcr.io/flyteorg/flytekit:sqlalchemy-75fc68cd2d0a71588359039f94daab09d68cac11",
        **kwargs,
    ):
        output_schema = output_schema_type if output_schema_type else FlyteSchema
        outputs = kwtypes(results=output_schema)

        super().__init__(
            name=name,
            task_config=task_config,
            executor_type=SQLAlchemyTaskExecutor,
            task_type=self._SQLALCHEMY_TASK_TYPE,
            query_template=query_template,
            container_image=container_image,
            inputs=inputs,
            outputs=outputs,
            **kwargs,
        )

    @property
    def output_columns(self) -> typing.Optional[typing.List[str]]:
        c = self.python_interface.outputs["results"].column_names()
        return c if c else None

    def get_custom(self, settings: SerializationSettings) -> typing.Dict[str, typing.Any]:
        return {
            "query_template": self.query_template,
            "uri": self.task_config.uri,
            "connect_args": self.task_config.connect_args or {},
            "secret_connect_args": self.task_config.secret_connect_args_to_dicts(),
        }


class SQLAlchemyTaskExecutor(ShimTaskExecutor[SQLAlchemyTask]):
    def execute_from_model(self, tt: flytekit.models.core.task.TaskTemplate, **kwargs) -> typing.Any:
        if tt.custom["secret_connect_args"] is not None:
            for key, secret_dict in tt.custom["secret_connect_args"].items():
                value = current_context().secrets.get(group=secret_dict["group"], key=secret_dict["key"])
                tt.custom["connect_args"][key] = value

        engine = create_engine(tt.custom["uri"], connect_args=tt.custom["connect_args"], echo=False)
        print(f"Connecting to db {tt.custom['uri']}")

        interpolated_query = SQLAlchemyTask.interpolate_query(tt.custom["query_template"], **kwargs)
        print(f"Interpolated query {interpolated_query}")
        with engine.begin() as connection:
            df = pd.read_sql_query(interpolated_query, connection)
        return df
