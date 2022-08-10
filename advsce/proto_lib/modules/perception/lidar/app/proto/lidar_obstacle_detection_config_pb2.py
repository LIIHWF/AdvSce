# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: modules/perception/lidar/app/proto/lidar_obstacle_detection_config.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='modules/perception/lidar/app/proto/lidar_obstacle_detection_config.proto',
  package='apollo.perception.lidar',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\nHmodules/perception/lidar/app/proto/lidar_obstacle_detection_config.proto\x12\x17\x61pollo.perception.lidar\"\x8c\x01\n\x1cLidarObstacleDetectionConfig\x12\'\n\x08\x64\x65tector\x18\x01 \x01(\t:\x15PointPillarsDetection\x12\x1d\n\x0fuse_map_manager\x18\x02 \x01(\x08:\x04true\x12$\n\x16use_object_filter_bank\x18\x03 \x01(\x08:\x04true')
)




_LIDAROBSTACLEDETECTIONCONFIG = _descriptor.Descriptor(
  name='LidarObstacleDetectionConfig',
  full_name='apollo.perception.lidar.LidarObstacleDetectionConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='detector', full_name='apollo.perception.lidar.LidarObstacleDetectionConfig.detector', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=_b("PointPillarsDetection").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='use_map_manager', full_name='apollo.perception.lidar.LidarObstacleDetectionConfig.use_map_manager', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='use_object_filter_bank', full_name='apollo.perception.lidar.LidarObstacleDetectionConfig.use_object_filter_bank', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=242,
)

DESCRIPTOR.message_types_by_name['LidarObstacleDetectionConfig'] = _LIDAROBSTACLEDETECTIONCONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LidarObstacleDetectionConfig = _reflection.GeneratedProtocolMessageType('LidarObstacleDetectionConfig', (_message.Message,), dict(
  DESCRIPTOR = _LIDAROBSTACLEDETECTIONCONFIG,
  __module__ = 'modules.perception.lidar.app.proto.lidar_obstacle_detection_config_pb2'
  # @@protoc_insertion_point(class_scope:apollo.perception.lidar.LidarObstacleDetectionConfig)
  ))
_sym_db.RegisterMessage(LidarObstacleDetectionConfig)


# @@protoc_insertion_point(module_scope)
