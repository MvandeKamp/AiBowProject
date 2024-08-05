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
            trackedArrows.put(arrow, new TrackedArrowInfo(Double.MAX_VALUE, false)); // Initializing with a high distance and hit status as false
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
            double distance = targetManager.DistanceToClosestTarget(arrow.position());
            BlockPos hit = targetManager.IsHit(arrow.position());
            boolean hitStatus = hit != null;
            trackedArrows.put(arrow, new TrackedArrowInfo(distance, hitStatus)); // Update the distance and hit status
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
            trackedArrows.remove(arrow);
        }
    }

    // Nested class to hold arrow tracking information
    private static class TrackedArrowInfo {
        private double distance;
        private boolean hit;

        public TrackedArrowInfo(double distance, boolean hit) {
            this.distance = distance;
            this.hit = hit;
        }

        public double getDistance() {
            return distance;
        }

        public boolean isHit() {
            return hit;
        }

        public void setDistance(double distance) {
            this.distance = distance;
        }

        public void setHit(boolean hit) {
            this.hit = hit;
        }
    }
}
