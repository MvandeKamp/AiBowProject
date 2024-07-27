package de.mvdk.aibowproject;

import AiBowProject.API.AiClientDef;
import AiBowProject.API.AiClientGrpc;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;
import io.grpc.stub.StreamObserver;

public class GrpcClient {
    public GrpcClient(String host, int port) {
        // Create a channel to the server
        ManagedChannel channel = ManagedChannelBuilder.forAddress("localhost", 50051)
                .usePlaintext()  // Use plaintext (non-TLS) for local testing
                .build();

        // Create an asynchronous stub for the service
        AiClientGrpc.AiClientStub asyncStub = AiClientGrpc.newStub(channel);
        AiClientGrpc.AiClientStub blockStub = AiClientGrpc.newStub(channel);

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
            blockStub.registerClient(request, responseObserver);
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
}
