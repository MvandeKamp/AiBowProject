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
            workItemId = (str(uuid.uuid4()))
            neatImpl.inputStack.push(request.clientId, request.targetPos.x, request.targetPos.y, request.targetPos.z, workItemId)
            while True:
                aim_at = neatImpl.outputList.get(request.clientId, workItemId)
                time.sleep(0.1)
                if aim_at is not None:
                    break
            target_reply = aiClientDef_pb2.TargetReply()
            target_reply.clientId = request.clientId
            target_reply.token = request.token
            target_reply.workItemId = workItemId

            aim_reply = aiClientDef_pb2.AimAt()
            aim_reply.jaw = aim_at[1]
            aim_reply.pitch = aim_at[2]
            aim_reply.holdLength = aim_at[3]
            target_reply.aimtAtPos.CopyFrom(aim_reply)
            neatImpl.outputList.remove(aim_at[0])
            return target_reply
        return

    def Result(self, request, context):
        if token == request.token:
            neatImpl.resultList.append(request.clientId, request.nearestPointToTarget, request.arrowHit, request.workItemId)
            return aiClientDef_pb2.ResultReply(token=token, clientId=request.clientId, ack=True, workItemId=request.workItemId)
        return aiClientDef_pb2.ResultReply(token=token, clientId=request.clientId, ack=False, workItemId=request.workItemId)


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
