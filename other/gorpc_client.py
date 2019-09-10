import grpc
import py_rpc_pb2
import py_rpc_pb2_grpc

def run():
    # 连接 rpc 服务器
    channel = grpc.insecure_channel('localhost:8080')
    # 调用 rpc 服务
    stub = py_rpc_pb2_grpc.HelloStub(channel)
    response = stub.SayHello(py_rpc_pb2.HelloRequest(name='czl'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()