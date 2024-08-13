package de.mvdk.aibowproject;

import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.projectile.AbstractArrow;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.entity.EntityJoinLevelEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.server.ServerLifecycleHooks;

import java.util.HashMap;
import java.util.Map;

@Mod.EventBusSubscriber
public class ArrowEventHandler {
    private static final Map<AbstractArrow, TrackedArrowInfo> trackedArrows = new HashMap<>();
    private TargetManager targetManager;
    private GrpcClient grpcClient;

    public ArrowEventHandler(TargetManager targetManager, GrpcClient comClient){
        this.targetManager = targetManager;
        this.grpcClient = comClient;
    }

    @SubscribeEvent
    public void onArrowShot(EntityJoinLevelEvent event) {
        if (event.getEntity() instanceof AbstractArrow arrow) {
            trackedArrows.put(arrow, new TrackedArrowInfo(Double.MAX_VALUE, false, null)); // Initializing with a high distance and hit status as false
            System.out.println("Arrow shot! Tracking arrow: " + arrow);
        }
    }

    @SubscribeEvent
    public void onTick(TickEvent.ServerTickEvent event) {
        ServerLevel level = event.getServer().overworld();
        Map<AbstractArrow, TrackedArrowInfo> toRemove = new HashMap<>();
        for (Map.Entry<AbstractArrow, TrackedArrowInfo> entry : trackedArrows.entrySet()) {
            AbstractArrow arrow = entry.getKey();
            TrackedArrowInfo info = entry.getValue();
            if (!arrow.isAlive()) {
                toRemove.put(arrow, info);
                continue;
            }
            BlockPos closestTarget = targetManager.GetClosestTargetPos(arrow.position(), true);
            double distance = targetManager.DistanceToClosestTarget(arrow.position());
            info.setDistance(distance);
            // This could hinder the model learning process or speed it up 50:50
            if(distance > 100){
                toRemove.put(arrow, info);
                continue;
            }

            BlockPos hit = targetManager.IsHit(arrow.position());
            boolean hitStatus = hit != null;
            trackedArrows.put(arrow, new TrackedArrowInfo(
                    info.distance,
                    hitStatus,
                    closestTarget)); // Update the distance and hit status
            if (hitStatus) {
                System.out.println("Hit: " + hit + " distance: " + distance);
                for (ServerPlayer player : ServerLifecycleHooks.getCurrentServer().getPlayerList().getPlayers()) {
                    player.sendSystemMessage(Component.literal("Hit: " + hit + " distance: " + distance));
                }
                targetManager.RemoveOldSpawnNew(hit);
            }

        }
        for (AbstractArrow arrow : toRemove.keySet()) {
            var value = trackedArrows.get(arrow);
            grpcClient.ResultSubmission(value.hit, value.distance);
            if(value.position != null){
                targetManager.RemoveOldSpawnNew(value.position);
            }
            trackedArrows.remove(arrow);
        }
    }

    // Nested class to hold arrow tracking information
    private static class TrackedArrowInfo {
        private double distance;
        private boolean hit;
        private BlockPos position; // Add a BlockPos field

        public TrackedArrowInfo(double distance, boolean hit, BlockPos position) {
            this.distance = distance;
            this.hit = hit;
            this.position = position; // Initialize the BlockPos field
        }

        public double getDistance() {
            return distance;
        }

        public boolean isHit() {
            return hit;
        }

        public BlockPos getPosition() { // Add a getter for BlockPos
            return position;
        }

        public void setDistance(double distance) {
            // Only update distance if the new value is smaller
            if (distance < this.distance) {
                this.distance = distance;
            }
        }

        public void setHit(boolean hit) {
            this.hit = hit;
        }

        public void setPosition(BlockPos position) { // Add a setter for BlockPos
            this.position = position;
        }
    }
}
