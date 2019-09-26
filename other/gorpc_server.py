# 编译 proto 文件
# python -m grpc_tools.protoc --python_out=. --grpc_python_out=. -I. helloworld.proto
#
# python -m grpc_tools.protoc: python 下的 protoc 编译器通过 python 模块(module) 实现, 所以说这一步非常省心
# --python_out=. : 编译生成处理 protobuf 相关的代码的路径, 这里生成到当前目录
# --grpc_python_out=. : 编译生成处理 grpc 相关的代码的路径, 这里生成到当前目录
# -I. helloworld.proto : proto 文件的路径, 这里的 proto 文件在当前目录

# C:\Programs\Python\Python37\python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=C:\workspace\code\self\github\bookServer\src\wager\proto  -I. C:\workspace\code\self\github\bookServer\src\wager\proto\py_rpc.proto



#build dcker
#sudo docker build -t registry.cn-beijing.aliyuncs.com/lefeng/phone_wager_py_beta:v1.0.2 -f ./Dockerfile  .
#sudo docker run -it -p 50051:50051 registry.cn-beijing.aliyuncs.com/lefeng/phone_wager_py_beta:v1.0.2 /bin/bash
#sudo docker push registry.cn-beijing.aliyuncs.com/lefeng/phone_wager_py_beta:v1.0.2

from concurrent import futures
import time
import grpc
import py_rpc_pb2
import py_rpc_pb2_grpc

import pandas as pd
import tushare as ts

# 实现 proto 文件中定义的 GreeterServicer
class Greeter(py_rpc_pb2_grpc.HelloServicer):
    # 实现 proto 文件中定义的 rpc 调用
    def SayHello(self, request, context):
        return py_rpc_pb2.HelloReply(message = 'hello2 {msg}'.format(msg = request.name))


class StockService(py_rpc_pb2_grpc.StockPriceServicer):
  
    
    
  # 实现 proto 文件中定义的 rpc 调用
  def GetPrice(self, request, context):
    print("GetPrice run...")
    re = py_rpc_pb2.LastPriceRsp(error=-1)
    try:
      df = ts.get_index()
      # print(df)
      #这里有问题，应该是和昨天收盘比涨跌，不是今天开盘
      AStock = df.loc[df.code == '000001']
      re.code = AStock.loc[0, 'code']
      re.name = AStock.loc[0, 'name']
      re.closePrice = AStock.loc[0, 'close']
      re.openPrice = AStock.loc[0, 'open']
      re.error = 0
    except Exception as e:
      print(e)
      re.error = -2
    return re


def serve():
    # 启动 rpc 服务
    print("run server ....")
    server = None
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        py_rpc_pb2_grpc.add_HelloServicer_to_server(Greeter(), server)
        py_rpc_pb2_grpc.add_StockPriceServicer_to_server(StockService(), server)
        server.add_insecure_port('[::]:50051')
        server.start()
    
        while True:
            time.sleep(60*60*24) # one day in seconds
    except KeyboardInterrupt:
        if server is not None:
            server.stop(0)
    except Exception as e:
      print("exception..  ")
      print(e)

if __name__ == '__main__':
  # df = ts.get_index()
  # # print(df)
  # re = py_rpc_pb2.LastPriceRsp(error=-1)
  # AStock = df.loc[df.code == '000001']
  # print(AStock)
  # re.code = AStock.loc[0, 'code']
  # re.name = AStock.loc[0, 'name']
  # re.price = AStock.loc[0, 'close']
  serve()