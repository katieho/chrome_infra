# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chrome_infra_log.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='chrome_infra_log.proto',
  package='crit_event.proto',
  serialized_pb='\n\x16\x63hrome_infra_log.proto\x12\x10\x63rit_event.proto\"\xe8\x03\n\x18\x43ommitQueuePatchsetEvent\x12\x44\n\x04type\x18\x01 \x01(\x0e\x32\x36.crit_event.proto.CommitQueuePatchsetEvent.CQEventType\x12S\n\x0bresult_type\x18\x02 \x01(\x0e\x32\x35.crit_event.proto.CommitQueuePatchsetEvent.ResultType:\x07UNKNOWN\"\xa6\x01\n\x0b\x43QEventType\x12\x11\n\rPATCH_FAILURE\x10\x00\x12\x0e\n\nPATCH_STOP\x10\x01\x12\x15\n\x11PATCH_TREE_CLOSED\x10\x02\x12\x13\n\x0fPATCH_THROTTLED\x10\x03\x12\x19\n\x15PATCH_READY_TO_COMMIT\x10\x04\x12\x16\n\x12PATCH_COMMIT_START\x10\x05\x12\x15\n\x11PATCH_COMMIT_DONE\x10\x06\"\x87\x01\n\nResultType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x10\n\x0cMISSING_LGTM\x10\x01\x12\x10\n\x0cINVALID_LGTM\x10\x02\x12\x12\n\x0e\x46\x41ILED_TRYJOBS\x10\x03\x12\x11\n\rCOMMIT_FAILED\x10\x04\x12\r\n\tCOMMITTED\x10\n\x12\x12\n\x0eUSER_CANCELLED\x10\x0b\"i\n\x0b\x43odeVersion\x12\x12\n\nsource_url\x18\x01 \x01(\t\x12\r\n\x05\x64irty\x18\x02 \x01(\x08\x12\x0f\n\x07version\x18\x03 \x01(\t\x12\x10\n\x08git_hash\x18\x04 \x01(\t\x12\x14\n\x0csvn_revision\x18\x05 \x01(\x05\"\x82\x02\n\x0cServiceEvent\x12\x46\n\x04type\x18\x01 \x01(\x0e\x32/.crit_event.proto.ServiceEvent.ServiceEventType:\x07UNKNOWN\x12\x33\n\x0c\x63ode_version\x18\x02 \x03(\x0b\x32\x1d.crit_event.proto.CodeVersion\x12\x13\n\x0bstack_trace\x18\x03 \x01(\t\"`\n\x10ServiceEventType\x12\x0b\n\x07UNKNOWN\x10\x00\x12\t\n\x05START\x10\x01\x12\x08\n\x04STOP\x10\x02\x12\n\n\x06UPDATE\x10\x03\x12\x13\n\x0f\x43URRENT_VERSION\x10\x04\x12\t\n\x05\x43RASH\x10\x05\"\xb5\x03\n\nBuildEvent\x12\x39\n\x04type\x18\x01 \x01(\x0e\x32+.crit_event.proto.BuildEvent.BuildEventType\x12\x11\n\thost_name\x18\x02 \x01(\t\x12\x12\n\nbuild_name\x18\x03 \x01(\t\x12\x14\n\x0c\x62uild_number\x18\x04 \x01(\x05\x12 \n\x18\x62uild_scheduling_time_ms\x18\x05 \x01(\x03\x12\x11\n\tstep_name\x18\x06 \x01(\t\x12\x13\n\x0bstep_number\x18\x07 \x01(\x05\x12\x41\n\x06result\x18\x08 \x01(\x0e\x32(.crit_event.proto.BuildEvent.BuildResult:\x07UNKNOWN\"4\n\x0e\x42uildEventType\x12\r\n\tSCHEDULER\x10\x00\x12\t\n\x05\x42UILD\x10\x01\x12\x08\n\x04STEP\x10\x02\"l\n\x0b\x42uildResult\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x0b\n\x07SUCCESS\x10\x01\x12\x0b\n\x07\x46\x41ILURE\x10\x02\x12\x11\n\rINFRA_FAILURE\x10\x03\x12\x0b\n\x07WARNING\x10\x04\x12\x0b\n\x07SKIPPED\x10\x05\x12\t\n\x05RETRY\x10\x06\"S\n\x10InfraEventSource\x12\x11\n\thost_name\x18\x01 \x01(\t\x12\x16\n\x0e\x61ppengine_name\x18\x02 \x01(\t\x12\x14\n\x0cservice_name\x18\x03 \x01(\t\"\xc3\x03\n\x10\x43hromeInfraEvent\x12Q\n\x0etimestamp_kind\x18\x01 \x01(\x0e\x32\x30.crit_event.proto.ChromeInfraEvent.TimestampKind:\x07UNKNOWN\x12\x10\n\x08trace_id\x18\x02 \x01(\t\x12\x0f\n\x07span_id\x18\x03 \x01(\t\x12\x11\n\tparent_id\x18\x04 \x01(\t\x12\x38\n\x0c\x65vent_source\x18\x05 \x01(\x0b\x32\".crit_event.proto.InfraEventSource\x12\x35\n\rservice_event\x18\x06 \x01(\x0b\x32\x1e.crit_event.proto.ServiceEvent\x12\x45\n\x11\x63q_patchset_event\x18\x07 \x01(\x0b\x32*.crit_event.proto.CommitQueuePatchsetEvent\x12\x31\n\x0b\x62uild_event\x18\x08 \x01(\x0b\x32\x1c.crit_event.proto.BuildEvent\";\n\rTimestampKind\x12\x0b\n\x07UNKNOWN\x10\x00\x12\t\n\x05POINT\x10\x01\x12\t\n\x05\x42\x45GIN\x10\x02\x12\x07\n\x03\x45ND\x10\x03')



_COMMITQUEUEPATCHSETEVENT_CQEVENTTYPE = _descriptor.EnumDescriptor(
  name='CQEventType',
  full_name='crit_event.proto.CommitQueuePatchsetEvent.CQEventType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='PATCH_FAILURE', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PATCH_STOP', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PATCH_TREE_CLOSED', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PATCH_THROTTLED', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PATCH_READY_TO_COMMIT', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PATCH_COMMIT_START', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PATCH_COMMIT_DONE', index=6, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=229,
  serialized_end=395,
)

_COMMITQUEUEPATCHSETEVENT_RESULTTYPE = _descriptor.EnumDescriptor(
  name='ResultType',
  full_name='crit_event.proto.CommitQueuePatchsetEvent.ResultType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='MISSING_LGTM', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INVALID_LGTM', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAILED_TRYJOBS', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COMMIT_FAILED', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='COMMITTED', index=5, number=10,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='USER_CANCELLED', index=6, number=11,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=398,
  serialized_end=533,
)

_SERVICEEVENT_SERVICEEVENTTYPE = _descriptor.EnumDescriptor(
  name='ServiceEventType',
  full_name='crit_event.proto.ServiceEvent.ServiceEventType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='START', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STOP', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPDATE', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CURRENT_VERSION', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CRASH', index=5, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=805,
  serialized_end=901,
)

_BUILDEVENT_BUILDEVENTTYPE = _descriptor.EnumDescriptor(
  name='BuildEventType',
  full_name='crit_event.proto.BuildEvent.BuildEventType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SCHEDULER', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BUILD', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='STEP', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1179,
  serialized_end=1231,
)

_BUILDEVENT_BUILDRESULT = _descriptor.EnumDescriptor(
  name='BuildResult',
  full_name='crit_event.proto.BuildEvent.BuildResult',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAILURE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INFRA_FAILURE', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WARNING', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SKIPPED', index=5, number=5,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='RETRY', index=6, number=6,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1233,
  serialized_end=1341,
)

_CHROMEINFRAEVENT_TIMESTAMPKIND = _descriptor.EnumDescriptor(
  name='TimestampKind',
  full_name='crit_event.proto.ChromeInfraEvent.TimestampKind',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='POINT', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='BEGIN', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='END', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1821,
  serialized_end=1880,
)


_COMMITQUEUEPATCHSETEVENT = _descriptor.Descriptor(
  name='CommitQueuePatchsetEvent',
  full_name='crit_event.proto.CommitQueuePatchsetEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='crit_event.proto.CommitQueuePatchsetEvent.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='result_type', full_name='crit_event.proto.CommitQueuePatchsetEvent.result_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _COMMITQUEUEPATCHSETEVENT_CQEVENTTYPE,
    _COMMITQUEUEPATCHSETEVENT_RESULTTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=45,
  serialized_end=533,
)


_CODEVERSION = _descriptor.Descriptor(
  name='CodeVersion',
  full_name='crit_event.proto.CodeVersion',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='source_url', full_name='crit_event.proto.CodeVersion.source_url', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='dirty', full_name='crit_event.proto.CodeVersion.dirty', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='version', full_name='crit_event.proto.CodeVersion.version', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='git_hash', full_name='crit_event.proto.CodeVersion.git_hash', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='svn_revision', full_name='crit_event.proto.CodeVersion.svn_revision', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=535,
  serialized_end=640,
)


_SERVICEEVENT = _descriptor.Descriptor(
  name='ServiceEvent',
  full_name='crit_event.proto.ServiceEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='crit_event.proto.ServiceEvent.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='code_version', full_name='crit_event.proto.ServiceEvent.code_version', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='stack_trace', full_name='crit_event.proto.ServiceEvent.stack_trace', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SERVICEEVENT_SERVICEEVENTTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=643,
  serialized_end=901,
)


_BUILDEVENT = _descriptor.Descriptor(
  name='BuildEvent',
  full_name='crit_event.proto.BuildEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='crit_event.proto.BuildEvent.type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='host_name', full_name='crit_event.proto.BuildEvent.host_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='build_name', full_name='crit_event.proto.BuildEvent.build_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='build_number', full_name='crit_event.proto.BuildEvent.build_number', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='build_scheduling_time_ms', full_name='crit_event.proto.BuildEvent.build_scheduling_time_ms', index=4,
      number=5, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='step_name', full_name='crit_event.proto.BuildEvent.step_name', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='step_number', full_name='crit_event.proto.BuildEvent.step_number', index=6,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='result', full_name='crit_event.proto.BuildEvent.result', index=7,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _BUILDEVENT_BUILDEVENTTYPE,
    _BUILDEVENT_BUILDRESULT,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=904,
  serialized_end=1341,
)


_INFRAEVENTSOURCE = _descriptor.Descriptor(
  name='InfraEventSource',
  full_name='crit_event.proto.InfraEventSource',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='host_name', full_name='crit_event.proto.InfraEventSource.host_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='appengine_name', full_name='crit_event.proto.InfraEventSource.appengine_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='service_name', full_name='crit_event.proto.InfraEventSource.service_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1343,
  serialized_end=1426,
)


_CHROMEINFRAEVENT = _descriptor.Descriptor(
  name='ChromeInfraEvent',
  full_name='crit_event.proto.ChromeInfraEvent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp_kind', full_name='crit_event.proto.ChromeInfraEvent.timestamp_kind', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=True, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='trace_id', full_name='crit_event.proto.ChromeInfraEvent.trace_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='span_id', full_name='crit_event.proto.ChromeInfraEvent.span_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='parent_id', full_name='crit_event.proto.ChromeInfraEvent.parent_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='event_source', full_name='crit_event.proto.ChromeInfraEvent.event_source', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='service_event', full_name='crit_event.proto.ChromeInfraEvent.service_event', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cq_patchset_event', full_name='crit_event.proto.ChromeInfraEvent.cq_patchset_event', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='build_event', full_name='crit_event.proto.ChromeInfraEvent.build_event', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CHROMEINFRAEVENT_TIMESTAMPKIND,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1429,
  serialized_end=1880,
)

_COMMITQUEUEPATCHSETEVENT.fields_by_name['type'].enum_type = _COMMITQUEUEPATCHSETEVENT_CQEVENTTYPE
_COMMITQUEUEPATCHSETEVENT.fields_by_name['result_type'].enum_type = _COMMITQUEUEPATCHSETEVENT_RESULTTYPE
_COMMITQUEUEPATCHSETEVENT_CQEVENTTYPE.containing_type = _COMMITQUEUEPATCHSETEVENT;
_COMMITQUEUEPATCHSETEVENT_RESULTTYPE.containing_type = _COMMITQUEUEPATCHSETEVENT;
_SERVICEEVENT.fields_by_name['type'].enum_type = _SERVICEEVENT_SERVICEEVENTTYPE
_SERVICEEVENT.fields_by_name['code_version'].message_type = _CODEVERSION
_SERVICEEVENT_SERVICEEVENTTYPE.containing_type = _SERVICEEVENT;
_BUILDEVENT.fields_by_name['type'].enum_type = _BUILDEVENT_BUILDEVENTTYPE
_BUILDEVENT.fields_by_name['result'].enum_type = _BUILDEVENT_BUILDRESULT
_BUILDEVENT_BUILDEVENTTYPE.containing_type = _BUILDEVENT;
_BUILDEVENT_BUILDRESULT.containing_type = _BUILDEVENT;
_CHROMEINFRAEVENT.fields_by_name['timestamp_kind'].enum_type = _CHROMEINFRAEVENT_TIMESTAMPKIND
_CHROMEINFRAEVENT.fields_by_name['event_source'].message_type = _INFRAEVENTSOURCE
_CHROMEINFRAEVENT.fields_by_name['service_event'].message_type = _SERVICEEVENT
_CHROMEINFRAEVENT.fields_by_name['cq_patchset_event'].message_type = _COMMITQUEUEPATCHSETEVENT
_CHROMEINFRAEVENT.fields_by_name['build_event'].message_type = _BUILDEVENT
_CHROMEINFRAEVENT_TIMESTAMPKIND.containing_type = _CHROMEINFRAEVENT;
DESCRIPTOR.message_types_by_name['CommitQueuePatchsetEvent'] = _COMMITQUEUEPATCHSETEVENT
DESCRIPTOR.message_types_by_name['CodeVersion'] = _CODEVERSION
DESCRIPTOR.message_types_by_name['ServiceEvent'] = _SERVICEEVENT
DESCRIPTOR.message_types_by_name['BuildEvent'] = _BUILDEVENT
DESCRIPTOR.message_types_by_name['InfraEventSource'] = _INFRAEVENTSOURCE
DESCRIPTOR.message_types_by_name['ChromeInfraEvent'] = _CHROMEINFRAEVENT

class CommitQueuePatchsetEvent(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _COMMITQUEUEPATCHSETEVENT

  # @@protoc_insertion_point(class_scope:crit_event.proto.CommitQueuePatchsetEvent)

class CodeVersion(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CODEVERSION

  # @@protoc_insertion_point(class_scope:crit_event.proto.CodeVersion)

class ServiceEvent(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SERVICEEVENT

  # @@protoc_insertion_point(class_scope:crit_event.proto.ServiceEvent)

class BuildEvent(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BUILDEVENT

  # @@protoc_insertion_point(class_scope:crit_event.proto.BuildEvent)

class InfraEventSource(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INFRAEVENTSOURCE

  # @@protoc_insertion_point(class_scope:crit_event.proto.InfraEventSource)

class ChromeInfraEvent(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CHROMEINFRAEVENT

  # @@protoc_insertion_point(class_scope:crit_event.proto.ChromeInfraEvent)


# @@protoc_insertion_point(module_scope)
