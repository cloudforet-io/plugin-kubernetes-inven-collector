from schematics import Model
from schematics.types import ModelType, ListType, StringType, FloatType, DateTimeType, IntType, BooleanType, DictType
from spaceone.inventory.libs.schema.base import ObjectMeta, LabelSelector, LocalObjectReference, ObjectReference


class ServiceReference(Model):
    name = StringType(serialize_when_none=False)
    namespace = StringType(serialize_when_none=False)
    path = StringType(serialize_when_none=False)
    port = IntType(serialize_when_none=False)


class WebhookClientConfig(Model):
    caBundle = StringType(serialize_when_none=False)
    service = ModelType(ServiceReference, serialize_when_none=False)
    url = StringType(serialize_when_none=False)


class WebhookConversion(Model):
    clientConfig = ModelType(WebhookClientConfig, serialize_when_none=False)
    conversionReviewVersions = ListType(StringType(), serialize_when_none=False)


class CustomResourceConversion(Model):
    strategy = StringType(serialize_when_none=False)
    webhook = ModelType(WebhookConversion, serialize_when_none=False)


class CustomResourceDefinitionNames(Model):
    categories = ListType(StringType(), serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    listKind = StringType(serialize_when_none=False)
    plural = StringType(serialize_when_none=False)
    shortNames = ListType(StringType(), serialize_when_none=False)
    singular = StringType(serialize_when_none=False)


class CustomResourceColumnDefinition(Model):
    description = StringType(serialize_when_none=False)
    format = StringType(serialize_when_none=False)
    jsonPath = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    priority = IntType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class CustomResourceDefinitionVersion(Model):
    additionalPrinterColumns = ListType(ModelType(CustomResourceColumnDefinition), serialize_when_none=False)
    deprecated = BooleanType(serialize_when_none=False)
    deprecationWarning = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    served = BooleanType(serialize_when_none=False)
    storage = BooleanType(serialize_when_none=False)


class CustomResourceDefinitionSpec(Model):
    conversion = ModelType(CustomResourceConversion, serialize_when_none=False)
    group = StringType(serialize_when_none=False)
    names = ModelType(CustomResourceDefinitionNames, serialize_when_none=False)
    preserveUnknownFields = BooleanType(serialize_when_none=False)
    scope = StringType(serialize_when_none=False)
    versions = ListType(ModelType(CustomResourceDefinitionVersion), serialize_when_none=False)


class CustomResourceDefinitionCondition(Model):
    lastTransitionTime = DateTimeType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)


class CustomResourceDefinitionStatus(Model):
    acceptedNames = ModelType(CustomResourceDefinitionNames, serialize_when_none=False)
    conditions = ListType(ModelType(CustomResourceDefinitionCondition), serialize_when_none=False)
    storedVersions = ListType(StringType(), serialize_when_none=False)


class CustomResourceDefinition(Model):
    api_version = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(CustomResourceDefinitionSpec, serialize_when_none=False)
    status = ModelType(CustomResourceDefinitionStatus, serialize_when_none=False)

    def reference(self):
        return {
            "resource_id": self.uid,
            "external_link": f""
        }
