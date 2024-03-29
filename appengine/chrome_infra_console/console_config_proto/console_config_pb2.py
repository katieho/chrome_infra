# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: console_config.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='console_config.proto',
  package='',
  serialized_pb='\n\x14\x63onsole_config.proto\"\xc3\x02\n\nConsoleCfg\x12\x1e\n\x04pane\x18\x01 \x03(\x0b\x32\x10.ConsoleCfg.Pane\x1a\x94\x02\n\x04Pane\x12\x0c\n\x04info\x18\x01 \x02(\t\x12%\n\x05graph\x18\x02 \x03(\x0b\x32\x16.ConsoleCfg.Pane.Graph\x1a\xd6\x01\n\x05Graph\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\x35\n\ntimeseries\x18\x02 \x03(\x0b\x32!.ConsoleCfg.Pane.Graph.Timeseries\x1a\x87\x01\n\nTimeseries\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x36\n\x05\x66ield\x18\x02 \x03(\x0b\x32\'.ConsoleCfg.Pane.Graph.Timeseries.Field\x12\x0e\n\x06metric\x18\x03 \x02(\t\x1a#\n\x05\x46ield\x12\x0b\n\x03key\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x02(\t')




_CONSOLECFG_PANE_GRAPH_TIMESERIES_FIELD = _descriptor.Descriptor(
  name='Field',
  full_name='ConsoleCfg.Pane.Graph.Timeseries.Field',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='ConsoleCfg.Pane.Graph.Timeseries.Field.key', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='ConsoleCfg.Pane.Graph.Timeseries.Field.value', index=1,
      number=2, type=9, cpp_type=9, label=2,
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
  serialized_start=313,
  serialized_end=348,
)

_CONSOLECFG_PANE_GRAPH_TIMESERIES = _descriptor.Descriptor(
  name='Timeseries',
  full_name='ConsoleCfg.Pane.Graph.Timeseries',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='ConsoleCfg.Pane.Graph.Timeseries.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='field', full_name='ConsoleCfg.Pane.Graph.Timeseries.field', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='metric', full_name='ConsoleCfg.Pane.Graph.Timeseries.metric', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_CONSOLECFG_PANE_GRAPH_TIMESERIES_FIELD, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=213,
  serialized_end=348,
)

_CONSOLECFG_PANE_GRAPH = _descriptor.Descriptor(
  name='Graph',
  full_name='ConsoleCfg.Pane.Graph',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='ConsoleCfg.Pane.Graph.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='timeseries', full_name='ConsoleCfg.Pane.Graph.timeseries', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_CONSOLECFG_PANE_GRAPH_TIMESERIES, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=134,
  serialized_end=348,
)

_CONSOLECFG_PANE = _descriptor.Descriptor(
  name='Pane',
  full_name='ConsoleCfg.Pane',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='info', full_name='ConsoleCfg.Pane.info', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='graph', full_name='ConsoleCfg.Pane.graph', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_CONSOLECFG_PANE_GRAPH, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=72,
  serialized_end=348,
)

_CONSOLECFG = _descriptor.Descriptor(
  name='ConsoleCfg',
  full_name='ConsoleCfg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pane', full_name='ConsoleCfg.pane', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_CONSOLECFG_PANE, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=25,
  serialized_end=348,
)

_CONSOLECFG_PANE_GRAPH_TIMESERIES_FIELD.containing_type = _CONSOLECFG_PANE_GRAPH_TIMESERIES;
_CONSOLECFG_PANE_GRAPH_TIMESERIES.fields_by_name['field'].message_type = _CONSOLECFG_PANE_GRAPH_TIMESERIES_FIELD
_CONSOLECFG_PANE_GRAPH_TIMESERIES.containing_type = _CONSOLECFG_PANE_GRAPH;
_CONSOLECFG_PANE_GRAPH.fields_by_name['timeseries'].message_type = _CONSOLECFG_PANE_GRAPH_TIMESERIES
_CONSOLECFG_PANE_GRAPH.containing_type = _CONSOLECFG_PANE;
_CONSOLECFG_PANE.fields_by_name['graph'].message_type = _CONSOLECFG_PANE_GRAPH
_CONSOLECFG_PANE.containing_type = _CONSOLECFG;
_CONSOLECFG.fields_by_name['pane'].message_type = _CONSOLECFG_PANE
DESCRIPTOR.message_types_by_name['ConsoleCfg'] = _CONSOLECFG

class ConsoleCfg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType

  class Pane(_message.Message):
    __metaclass__ = _reflection.GeneratedProtocolMessageType

    class Graph(_message.Message):
      __metaclass__ = _reflection.GeneratedProtocolMessageType

      class Timeseries(_message.Message):
        __metaclass__ = _reflection.GeneratedProtocolMessageType

        class Field(_message.Message):
          __metaclass__ = _reflection.GeneratedProtocolMessageType
          DESCRIPTOR = _CONSOLECFG_PANE_GRAPH_TIMESERIES_FIELD

          # @@protoc_insertion_point(class_scope:ConsoleCfg.Pane.Graph.Timeseries.Field)
        DESCRIPTOR = _CONSOLECFG_PANE_GRAPH_TIMESERIES

        # @@protoc_insertion_point(class_scope:ConsoleCfg.Pane.Graph.Timeseries)
      DESCRIPTOR = _CONSOLECFG_PANE_GRAPH

      # @@protoc_insertion_point(class_scope:ConsoleCfg.Pane.Graph)
    DESCRIPTOR = _CONSOLECFG_PANE

    # @@protoc_insertion_point(class_scope:ConsoleCfg.Pane)
  DESCRIPTOR = _CONSOLECFG

  # @@protoc_insertion_point(class_scope:ConsoleCfg)


# @@protoc_insertion_point(module_scope)
