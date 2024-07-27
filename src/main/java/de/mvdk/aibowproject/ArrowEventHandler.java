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

import java.util.ArrayList;
import java.util.List;

@Mod.EventBusSubscriber
public class ArrowEventHandler {
    private static final List<AbstractArrow> trackedArrows = new ArrayList<>();
    private TargetManager targetManager;


    public ArrowEventHandler(TargetManager targetManager){
        this.targetManager = targetManager;
    }

    @SubscribeEvent
    public void onArrowShot(EntityJoinLevelEvent event) {

        if (event.getEntity() instanceof AbstractArrow arrow) {
            trackedArrows.add(arrow);
            System.out.println("Arrow shot! Tracking arrow: " + arrow);
        }
    }

    @SubscribeEvent
    public void onTick(TickEvent.ServerTickEvent event) {
        ServerLevel level = event.getServer().overworld();
        List<AbstractArrow> toRemove = new ArrayList<AbstractArrow>();
        for (AbstractArrow arrow : trackedArrows) {
            if (!arrow.isAlive()) {
                toRemove.add(arrow);
                continue;
            }
            double distance = targetManager.DistanceToClosestTarget(arrow.position());
            BlockPos hit = targetManager.IsHit(arrow.position());
            if(hit != null){
                System.out.println("Hit: " + hit + " distance: " + distance);
                for (ServerPlayer player : ServerLifecycleHooks.getCurrentServer().getPlayerList().getPlayers()) {
                    player.sendSystemMessage(Component.literal("Hit: " + hit + " distance: " + distance));
                }
                targetManager.RemoveOldSpawnNew(hit);
            }
            //System.out.println("Arrow position: " + arrow.position() + " " + arrow.tickCount);
        }
        trackedArrows.removeAll(toRemove);
    }
}