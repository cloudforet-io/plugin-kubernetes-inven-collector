from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, DictType
from spaceone.inventory.libs.schema.base import ObjectMeta, LabelSelector, LocalObjectReference, ObjectReference


class HelmMaintainer(Model):
    name = StringType(serialize_when_none=False)
    email = StringType(serialize_when_none=False)


class HelmChartMetadata(Model):
    name = StringType(serialize_when_none=False)
    home = StringType(serialize_when_none=False)
    sources = ListType(StringType(), serialize_when_none=False)
    version = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    keywords = ListType(StringType(), serialize_when_none=False)
    maintainers = ListType(ModelType(HelmMaintainer), deserialize_from="maintainers", serialize_when_none=False)
    icon = StringType(serialize_when_none=False)
    api_version = StringType(deserialize_from="apiVersion", serialize_when_none=False)
    app_version = StringType(deserialize_from="appVersion", serialize_when_none=False)


class HelmChartTemplate(Model):
    name = StringType(serialize_when_none=False)
    #skipping data because data size is too much big and useless
    #data = StringType(serialize_when_none=False)


class HelmChartLockDependencies(Model):
    name = StringType(serialize_when_none=False)
    version = StringType(serialize_when_none=False)
    repository = StringType(serialize_when_none=False)


class HelmChartLock(Model):
    generated = StringType(serialize_when_none=False)
    digest = StringType(serialize_when_none=False)
    dependencies = ListType(ModelType(HelmChartLockDependencies), serialize_when_none=False)


class HelmChart(Model):
    metadata = ModelType(HelmChartMetadata, deserialize_from='metadata', serialize_when_none=False)
    lock = ModelType(HelmChartLock, serialize_when_none=False)
    templates = ListType(ModelType(HelmChartTemplate), serialize_when_none=False)

    """
    Other param will be managed later

    templates
    values
    schema
    files
    """


class HelmInfo(Model):
    first_deployed = StringType(serialize_when_none=False)
    last_deployed = StringType(serialize_when_none=False)
    deleted = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    #notes = StringType(serialize_when_none=False)


class HelmMetadataLabels(Model):
    name = StringType(serialize_when_none=False)
    owner = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    version = StringType(serialize_when_none=False)


class HelmMetadata(Model):
    creation_timestamp = DateTimeType(serialize_when_none=False)
    labels = ModelType(HelmMetadataLabels, serialize_when_none=False)


class HelmRelease(Model):
    name = StringType(serialize_when_none=False)
    info = ModelType(HelmInfo, deserialize_from='info', serialize_when_none=False)
    chart = ModelType(HelmChart, deserialize_from='chart', serialize_when_none=False)
    #manifest = StringType(serialize_when_none=False)
    version = StringType(serialize_when_none=False)
    namespace = StringType(serialize_when_none=False)
    """
    Other param will be managed later
    manifest
    """


class HelmData(Model):
    release = ModelType(HelmRelease, deserialize_from="release", serialize_when_none=False)


class Release(Model):
    api_version = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    data = ModelType(HelmData, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.uid,
            "external_link": f""
        }
