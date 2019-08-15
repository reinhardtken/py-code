# 编译 proto 文件
# python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto
#
# python -m grpc_tools.protoc: python 下的 protoc 编译器通过 python 模块(module) 实现, 所以说这一步非常省心
# --python_out=. : 编译生成处理 protobuf 相关的代码的路径, 这里生成到当前目录
# --grpc_python_out=. : 编译生成处理 grpc 相关的代码的路径, 这里生成到当前目录
# -I. helloworld.proto : proto 文件的路径, 这里的 proto 文件在当前目录

# C:\Programs\Python\Python37\python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=C:\workspace\code\self\github\bookServer\src\wager\proto  -I. C:\workspace\code\self\github\bookServer\src\wager\proto\py_rpc.proto


from concurrent import futures
import time
import grpc
import py_rpc_pb2
import py_rpc_pb2_grpc

# 实现 proto 文件中定义的 GreeterServicer
class Greeter(py_rpc_pb2_grpc.HelloServicer):
    # 实现 proto 文件中定义的 rpc 调用
    def SayHello(self, request, context):
        return py_rpc_pb2.HelloReply(message = 'hello {msg}'.format(msg = request.name))


def serve():
    # 启动 rpc 服务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    py_rpc_pb2_grpc.add_HelloServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(60*60*24) # one day in seconds
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()