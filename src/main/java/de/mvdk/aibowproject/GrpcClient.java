package de.mvdk.aibowproject;

import AiBowProject.API.AiClientDef;
import AiBowProject.API.AiClientGrpc;
import com.google.protobuf.Descriptors;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;
import io.grpc.stub.StreamObserver;
import net.minecraft.world.phys.Vec3;

import javax.management.Descriptor;

import static AiBowProject.API.AiClientGrpc.*;

public class GrpcClient {
    private ManagedChannel channel;
    public String clientId = "";
    private String token = "321";

    public GrpcClient(String host, int port) {
        // Create a channel to the server
        channel = ManagedChannelBuilder.forAddress("localhost", 50051)
                .usePlaintext()  // Use plaintext (non-TLS) for local testing
                .build();

        // Create an asynchronous stub for the service
        AiClientStub asyncStub = newStub(channel);
        AiClientBlockingStub blockStub = newBlockingStub(channel);

        AiClientDef.RegisterRequest request = AiClientDef.RegisterRequest.newBuilder().setToken("test31").build();
        AiClientDef.RegisterReply response;

        // Create a StreamObserver for the response
        StreamObserver<AiClientDef.RegisterReply> responseObserver = new StreamObserver<AiClientDef.RegisterReply>() {
            @Override
            public void onNext(AiClientDef.RegisterReply response) {
                // Process the response
                System.out.println("Response: " + response.getClientId());
            }
            @Override
            public void onError(Throwable t) {
                // Handle the error
                t.printStackTrace();
            }
            @Override
            public void onCompleted() {
                // Called when the server has finished sending responses
                System.out.println("Server has completed sending responses.");
            }
        };

        try {
            blockStub.registerClient(request);
        } catch (StatusRuntimeException e) {
            System.out.println("RPC failed: " + e.getStatus());
            return;
        }

        // Build the request
        AiClientDef.RegisterRequest requests = AiClientDef.RegisterRequest.newBuilder()
                .setField(AiClientDef.RegisterRequest.getDescriptor().findFieldByNumber(1), "test")
                .build();

        // Create a StreamObserver for the request
        asyncStub.registerClient(requests, responseObserver);

        // Shutdown the channel (optional, depending on your application lifecycle)
        channel.shutdown();
    }

    private Descriptors.FieldDescriptor GetDescriptor(int fieldNumber, Descriptors.Descriptor descriptor) {
        return descriptor.findFieldByNumber(fieldNumber);
    }

    public String RegisterClient(){
        AiClientBlockingStub blockStub = newBlockingStub(channel);

        Descriptors.Descriptor desc = AiClientDef.RegisterRequest.getDescriptor();

        AiClientDef.RegisterRequest request = AiClientDef.RegisterRequest.newBuilder()
                .setField(GetDescriptor(1, desc), this.token)
                .build();

        try {
            AiClientDef.RegisterReply reply = blockStub.registerClient(request);
            this.clientId = reply.getClientId();
            return reply.getClientId();
        } catch (StatusRuntimeException e) {
            System.out.println("RPC failed: " + e.getStatus());
        }
        return "";
    }

    public Vec3 TargetRequest(Vec3 targetPos){
        AiClientBlockingStub blockStub = newBlockingStub(channel);

        Descriptors.Descriptor desc = AiClientDef.TargetRequest.getDescriptor();


        AiClientDef.TargetRequest request = AiClientDef.TargetRequest.newBuilder()
                .setField(GetDescriptor(1, desc), this.token)
                .setField(GetDescriptor(1, desc), this.clientId)
                // TODO: Implement the target Pos
                .build();

        try {
            AiClientDef.TargetReply reply = blockStub.target(request);
            // TODO Implement the target reply
        } catch (StatusRuntimeException e) {
            System.out.println("RPC failed: " + e.getStatus());
        }
        return new Vec3(targetPos.x, targetPos.y, targetPos.z);
    }

    public boolean ResultSubmission(boolean arrowHit, double distanceNearestToTarget){
        AiClientBlockingStub blockStub = newBlockingStub(channel);

        Descriptors.Descriptor desc = AiClientDef.ResultSubmission.getDescriptor();


        AiClientDef.ResultSubmission request = AiClientDef.ResultSubmission.newBuilder()
                .setClientId(this.clientId)
                .setArrowHit(arrowHit)
                .setToken(this.token)
                .setNearestPointToTarget((float) distanceNearestToTarget)
                .build();

        try {
            AiClientDef.ResultReply reply = blockStub.result(request);
            return reply.getAck();
        } catch (StatusRuntimeException e) {
            System.out.println("RPC failed: " + e.getStatus());
        }
        return false;
    }
}
