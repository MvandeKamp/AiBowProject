package de.mvdk.aibowproject;

import AiBowProject.API.AiClientDef;
import com.google.protobuf.Descriptors;
import com.sun.jna.platform.win32.Guid;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.StatusRuntimeException;
import io.grpc.stub.StreamObserver;
import net.minecraft.world.phys.Vec2;
import net.minecraft.world.phys.Vec3;

import java.util.Objects;

import static AiBowProject.API.AiClientGrpc.*;

public class GrpcClient {
    private ManagedChannel channel;
    public String clientId = "";
    private String token = "321";
    private PlayerMovementHandler movementHandler;
    public String workItemID;

    public GrpcClient(String host, int port, PlayerMovementHandler playerMovementHandler) {
        movementHandler = playerMovementHandler;
        // Create a channel to the server
        channel = ManagedChannelBuilder.forAddress("localhost", 50051)
                .usePlaintext()  // Use plaintext (non-TLS) for local testing
                .build();
        this.clientId = this.RegisterClient();
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
            return reply.getClientId();
        } catch (StatusRuntimeException e) {
            System.out.println("RPC failed: " + e.getStatus());
        }
        return "";
    }

    public void TargetRequest(Vec3 targetPos){
        AiClientStub asyncStub = newStub(channel);

        AiClientDef.TargetRequest request = AiClientDef.TargetRequest.newBuilder()
                .setToken(this.token)
                .setClientId(this.clientId)
                .setTargetPos(AiClientDef.TargetPos.newBuilder()
                        .setX((float) targetPos.x)
                        .setY((float) targetPos.y)
                        .setZ((float) targetPos.z)
                        .build())
                .build();

        asyncStub.target(request, new StreamObserver<AiClientDef.TargetReply>() {
            @Override
            public void onNext(AiClientDef.TargetReply reply) {
                try {
                    //Dont want to process the same workitem twice will request a new one just for resilancy
                    if(!Objects.equals(workItemID, reply.getWorkItemId())){
                       workItemID = reply.getWorkItemId();
                    } else {
                       TargetRequest(targetPos);
                        return;
                    }
                    movementHandler.aimPos = new Vec2(reply.getAimtAtPos().getJaw(), reply.getAimtAtPos().getPitch());
                    movementHandler.fireTicks = 20;
                    movementHandler.shouldFire = true;
                } catch (Exception e) {

                }
            }

            @Override
            public void onError(Throwable t) {
                System.out.println("RPC failed: " + t);
            }

            @Override
            public void onCompleted() {
            }
        });
    }

    public boolean ResultSubmission(boolean arrowHit, double distanceNearestToTarget){
        AiClientBlockingStub blockStub = newBlockingStub(channel);

        Descriptors.Descriptor desc = AiClientDef.ResultSubmission.getDescriptor();


        // Fail save for old or duplicated arrows so we dont send submissions twice
        if(workItemID == null){
            return false;
        }


        AiClientDef.ResultSubmission request = AiClientDef.ResultSubmission.newBuilder()
                .setClientId(this.clientId)
                .setArrowHit(arrowHit)
                .setToken(this.token)
                .setNearestPointToTarget((float) distanceNearestToTarget)
                .setWorkItemId(workItemID)
                .build();

        try {
            AiClientDef.ResultReply reply = blockStub.result(request);

            // RESET Work ItemId
            workItemID = null;
            return reply.getAck();
        } catch (StatusRuntimeException e) {
            System.out.println("RPC failed: " + e.getStatus());
        }
        return false;
    }
}
