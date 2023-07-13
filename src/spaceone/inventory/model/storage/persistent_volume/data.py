from schematics import Model
from schematics.types import (
    ModelType,
    ListType,
    StringType,
    FloatType,
    DateTimeType,
    IntType,
    BooleanType,
    DictType,
)
from spaceone.inventory.libs.schema.base import (
    ObjectMeta,
    LabelSelector,
    Condition,
    AWSElasticBlockStoreVolumeSource,
    AzureDiskVolumeSource,
    SecretReference,
    ObjectReference,
    FCVolumeSource,
    GCEPersistentDiskVolumeSource,
    HostPathVolumeSource,
    NFSVolumeSource,
    NodeSelector,
    PhotonPersistentDiskVolumeSource,
    PortworxVolumeSource,
    QuobyteVolumeSource,
    RBDPersistentVolumeSource,
)


class CinderPersistentVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    secret_ref = ModelType(SecretReference, serialize_when_none=False)
    volume_id = StringType(serialize_when_none=False)


class CephFSPersistentVolumeSource(Model):
    monitors = ListType(StringType(), serialize_when_none=False)
    path = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    secret_file = StringType(serialize_when_none=False)
    secret_ref = ModelType(SecretReference, serialize_when_none=False)
    user = StringType(serialize_when_none=False)


class AzureFilePersistentVolumeSource(Model):
    read_only = BooleanType(serialize_when_none=False)
    secret_name = StringType(serialize_when_none=False)
    secret_namespace = StringType(serialize_when_none=False)
    share_name = StringType(serialize_when_none=False)


class CSIPersistentVolumeSource(Model):
    controller_expand_secret_ref = ModelType(SecretReference, serialize_when_none=False)
    controller_publish_secret_ref = ModelType(
        SecretReference, serialize_when_none=False
    )
    driver = StringType(serialize_when_none=False)
    fs_type = StringType(serialize_when_none=False)
    node_publish_secret_ref = ModelType(SecretReference, serialize_when_none=False)
    node_stage_secret_ref = ModelType(SecretReference, serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    volume_attributes = DictType(StringType(), serialize_when_none=False)
    volume_handle = StringType(serialize_when_none=False)


class FlexPersistentVolumeSource(Model):
    driver = StringType(serialize_when_none=False)
    fs_type = StringType(serialize_when_none=False)
    options = DictType(StringType(), serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    secret_ref = ModelType(SecretReference, serialize_when_none=False)


class FlockerVolumeSource(Model):
    dataset_name = StringType(serialize_when_none=False)
    dataset_uuid = StringType(serialize_when_none=False)


class GlusterfsPersistentVolumeSource(Model):
    endpoints = StringType(serialize_when_none=False)
    endpoints_namespace = StringType(serialize_when_none=False)
    path = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)


class ISCSIPersistentVolumeSource(Model):
    chap_auth_discovery = StringType(serialize_when_none=False)
    chap_auth_session = StringType(serialize_when_none=False)
    fs_type = StringType(serialize_when_none=False)
    initiator_name = StringType(serialize_when_none=False)
    iqn = StringType(serialize_when_none=False)
    iscsi_interface = StringType(serialize_when_none=False)
    lun = IntType(serialize_when_none=False)
    portals = ListType(StringType(), serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    secret_ref = ModelType(SecretReference, serialize_when_none=False)
    target_portal = StringType(serialize_when_none=False)


class LocalVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    path = StringType(serialize_when_none=False)


class VolumeNodeAffinity(Model):
    required = ModelType(NodeSelector, serialize_when_none=False)


class ScaleIOPersistentVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    gateway = StringType(serialize_when_none=False)
    protection_domain = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    secret_ref = ModelType(SecretReference, serialize_when_none=False)
    ssl_enabled = BooleanType(serialize_when_none=False)
    storage_mode = StringType(serialize_when_none=False)
    storage_pool = StringType(serialize_when_none=False)
    system = StringType(serialize_when_none=False)
    volume_name = StringType(serialize_when_none=False)


class StorageOSPersistentVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    read_only = BooleanType(serialize_when_none=False)
    secret_ref = ModelType(ObjectReference, serialize_when_none=False)
    volume_name = StringType(serialize_when_none=False)
    volume_namespace = StringType(serialize_when_none=False)


class VsphereVirtualDiskVolumeSource(Model):
    fs_type = StringType(serialize_when_none=False)
    storage_policy_id = StringType(serialize_when_none=False)
    storage_policy_name = StringType(serialize_when_none=False)
    volume_path = StringType(serialize_when_none=False)


class PersistentVolumeSpec(Model):
    access_modes = ListType(StringType(), serialize_when_none=False)
    capacity = DictType(StringType(), serialize_when_none=False)
    mount_options = ListType(StringType(), serialize_when_none=False)
    persistent_volume_reclaim_policy = StringType(serialize_when_none=False)
    storage_class_name = StringType(serialize_when_none=False)
    volume_mode = StringType(serialize_when_none=False)
    aws_elastic_block_store = ModelType(
        AWSElasticBlockStoreVolumeSource, serialize_when_none=False
    )
    azure_disk = ModelType(AzureDiskVolumeSource, serialize_when_none=False)
    azure_file = ModelType(AzureFilePersistentVolumeSource, serialize_when_none=False)
    cephfs = ModelType(CephFSPersistentVolumeSource, serialize_when_none=False)
    cinder = ModelType(CinderPersistentVolumeSource, serialize_when_none=False)
    claim_ref = ModelType(ObjectReference, serialize_when_none=False)
    csi = ModelType(CSIPersistentVolumeSource, serialize_when_none=False)
    fc = ModelType(FCVolumeSource, serialize_when_none=False)
    flex_volume = ModelType(FlexPersistentVolumeSource, serialize_when_none=False)
    flocker = ModelType(FlockerVolumeSource, serialize_when_none=False)
    gce_persistent_disk = ModelType(
        GCEPersistentDiskVolumeSource, serialize_when_none=False
    )
    glusterfs = ModelType(GlusterfsPersistentVolumeSource, serialize_when_none=False)
    host_path = ModelType(HostPathVolumeSource, serialize_when_none=False)
    iscsi = ModelType(ISCSIPersistentVolumeSource, serialize_when_none=False)
    local = ModelType(LocalVolumeSource, serialize_when_none=False)
    nfs = ModelType(NFSVolumeSource, serialize_when_none=False)
    node_affinity = ModelType(VolumeNodeAffinity, serialize_when_none=False)
    photon_persistent_disk = ModelType(
        PhotonPersistentDiskVolumeSource, serialize_when_none=False
    )
    portworx_volume = ModelType(PortworxVolumeSource, serialize_when_none=False)
    quobyte = ModelType(QuobyteVolumeSource, serialize_when_none=False)
    rbd = ModelType(RBDPersistentVolumeSource, serialize_when_none=False)
    scale_io = ModelType(ScaleIOPersistentVolumeSource, serialize_when_none=False)
    storageos = ModelType(StorageOSPersistentVolumeSource, serialize_when_none=False)
    vsphere_volume = ModelType(
        VsphereVirtualDiskVolumeSource, serialize_when_none=False
    )


class PersistentVolumeStatus(Model):
    message = StringType(serialize_when_none=False)
    phase = StringType(serialize_when_none=False)
    reason = StringType(serialize_when_none=False)


class PersistentVolume(Model):
    api_version = StringType(serialize_when_none=False)
    uid = StringType(serialize_when_none=False)
    kind = StringType(serialize_when_none=False)
    metadata = ModelType(ObjectMeta, serialize_when_none=False)
    spec = ModelType(PersistentVolumeSpec, serialize_when_none=False)
    status = ModelType(PersistentVolumeStatus, serialize_when_none=False)

    def reference(self):
        return {"resource_id": self.uid, "external_link": f""}
