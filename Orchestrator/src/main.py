import sys
import os
import time
import uuid
from concurrent import futures
import grpc

sys.path.append(os.path.join(os.path.dirname(__file__), 'proto'))
from proto import greeting_pb2_grpc, greeting_pb2
from proto import aiClientDef_pb2_grpc, aiClientDef_pb2
import neatImpl

token = "321"
clientList = []


def GenNewClientId():
    newId = (str(uuid.uuid4()))
    clientList.append(newId)
    return newId


class Greeter(greeting_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print("Greetings from %s!" % request.name)
        return greeting_pb2.HelloReply(message='Hello, {}'.format(request.name))


class AiClient(aiClientDef_pb2_grpc.AiClientServicer):
    def RegisterClient(self, request, context):
        if (token == request.token):
            return aiClientDef_pb2.RegisterReply(token=token, clientId=GenNewClientId())
        return

    def Target(self, request, context):
        if token == request.token:
            neatImpl.inputStack.push(request.clientId, request.targetPos.x, request.targetPos.y, request.targetPos.z)
            while True:
                aim_at = neatImpl.outputList.get(request.clientId)
                time.sleep(0.1)
                if aim_at is not None:
                    break
            return aiClientDef_pb2.TargetReply(token=token, clientId=request.clientId, aimAt={
                "jaw": aim_at[1],
                "pitch": aim_at[2],
                "roll": aim_at[3],
                "holdLength": aim_at[4]
            })
        return

    def Result(self, request, context):
        if token == request.token:
            neatImpl.resultList.append(request.clientId, request.nearestPointToTarget, request.arrowHit)
            return aiClientDef_pb2.ResultReply(token=token, clientId=request.clientId, ack=True)
        return aiClientDef_pb2.ResultReply(token=token, clientId=request.clientId, ack=False)


def serveAiServer():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    aiClientDef_pb2_grpc.add_AiClientServicer_to_server(AiClient(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


def handleConsole(executor):
    while True:
        command = input("Enter a command:")
        if command == "exit":
            sys.exit()
        if command == "start":
            executor.submit(neatImpl.run())


with futures.ThreadPoolExecutor(max_workers=10) as executor:
    # Schedule the gRPC server to run
    executor.submit(serveAiServer)

    # Handle terminal commands in the main thread
    handleConsole(executor)
