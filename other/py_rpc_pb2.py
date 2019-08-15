# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: py_rpc.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='py_rpc.proto',
  package='proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x0cpy_rpc.proto\x12\x05proto\"\x1c\n\x0cHelloRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\x1d\n\nHelloReply\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x16\n\x07\x45\x63hoReq\x12\x0b\n\x03msg\x18\x01 \x01(\t\"\x16\n\x07\x45\x63hoRes\x12\x0b\n\x03msg\x18\x01 \x01(\t2=\n\x05Hello\x12\x34\n\x08SayHello\x12\x13.proto.HelloRequest\x1a\x11.proto.HelloReply\"\x00\x32.\n\x04\x45\x63ho\x12&\n\x04\x65\x63ho\x12\x0e.proto.EchoReq\x1a\x0e.proto.EchoResb\x06proto3')
)




_HELLOREQUEST = _descriptor.Descriptor(
  name='HelloRequest',
  full_name='proto.HelloRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='proto.HelloRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=23,
  serialized_end=51,
)


_HELLOREPLY = _descriptor.Descriptor(
  name='HelloReply',
  full_name='proto.HelloReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='proto.HelloReply.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=53,
  serialized_end=82,
)


_ECHOREQ = _descriptor.Descriptor(
  name='EchoReq',
  full_name='proto.EchoReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='msg', full_name='proto.EchoReq.msg', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=84,
  serialized_end=106,
)


_ECHORES = _descriptor.Descriptor(
  name='EchoRes',
  full_name='proto.EchoRes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='msg', full_name='proto.EchoRes.msg', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=108,
  serialized_end=130,
)

DESCRIPTOR.message_types_by_name['HelloRequest'] = _HELLOREQUEST
DESCRIPTOR.message_types_by_name['HelloReply'] = _HELLOREPLY
DESCRIPTOR.message_types_by_name['EchoReq'] = _ECHOREQ
DESCRIPTOR.message_types_by_name['EchoRes'] = _ECHORES
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

HelloRequest = _reflection.GeneratedProtocolMessageType('HelloRequest', (_message.Message,), {
  'DESCRIPTOR' : _HELLOREQUEST,
  '__module__' : 'py_rpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.HelloRequest)
  })
_sym_db.RegisterMessage(HelloRequest)

HelloReply = _reflection.GeneratedProtocolMessageType('HelloReply', (_message.Message,), {
  'DESCRIPTOR' : _HELLOREPLY,
  '__module__' : 'py_rpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.HelloReply)
  })
_sym_db.RegisterMessage(HelloReply)

EchoReq = _reflection.GeneratedProtocolMessageType('EchoReq', (_message.Message,), {
  'DESCRIPTOR' : _ECHOREQ,
  '__module__' : 'py_rpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.EchoReq)
  })
_sym_db.RegisterMessage(EchoReq)

EchoRes = _reflection.GeneratedProtocolMessageType('EchoRes', (_message.Message,), {
  'DESCRIPTOR' : _ECHORES,
  '__module__' : 'py_rpc_pb2'
  # @@protoc_insertion_point(class_scope:proto.EchoRes)
  })
_sym_db.RegisterMessage(EchoRes)



_HELLO = _descriptor.ServiceDescriptor(
  name='Hello',
  full_name='proto.Hello',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=132,
  serialized_end=193,
  methods=[
  _descriptor.MethodDescriptor(
    name='SayHello',
    full_name='proto.Hello.SayHello',
    index=0,
    containing_service=None,
    input_type=_HELLOREQUEST,
    output_type=_HELLOREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_HELLO)

DESCRIPTOR.services_by_name['Hello'] = _HELLO


_ECHO = _descriptor.ServiceDescriptor(
  name='Echo',
  full_name='proto.Echo',
  file=DESCRIPTOR,
  index=1,
  serialized_options=None,
  serialized_start=195,
  serialized_end=241,
  methods=[
  _descriptor.MethodDescriptor(
    name='echo',
    full_name='proto.Echo.echo',
    index=0,
    containing_service=None,
    input_type=_ECHOREQ,
    output_type=_ECHORES,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_ECHO)

DESCRIPTOR.services_by_name['Echo'] = _ECHO

# @@protoc_insertion_point(module_scope)
