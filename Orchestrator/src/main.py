import sys
import os
from concurrent import futures
import grpc


sys.path.append(os.path.join(os.path.dirname(__file__), 'proto'))
from proto import greeting_pb2_grpc, greeting_pb2
from proto import aiClientDef_pb2_grpc, aiClientDef_pb2


class Greeter(greeting_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print("Greetings from %s!" % request.name)
        return greeting_pb2.HelloReply(message='Hello, {}'.format(request.name))


class AiClient(aiClientDef_pb2_grpc.AiClientServicer):
    def RegisterClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        print("Greetings from %s!")
        print("Greetings from %s!")
        return aiClientDef_pb2.RegisterReply(token="123", clientId="fdgd")

    def Target(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Result(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def serveAiServer():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aiClientDef_pb2_grpc.add_AiClientServicer_to_server(AiClient(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serveAiServer()
