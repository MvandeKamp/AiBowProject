package de.mvdk.aibowproject;

import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.item.BowItem;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.Rotation;
import net.minecraft.world.phys.Vec2;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.common.Mod.EventBusSubscriber;
import net.minecraftforge.fml.common.Mod.EventBusSubscriber.Bus;

@EventBusSubscriber(value = Dist.CLIENT)
public class PlayerMovementHandler {

    private int fireWait = 5;
    private boolean fired = false;
    public boolean shouldFire = false;
    public Vec2 aimPos = new Vec2(0, 0);
    public int fireTicks = 20;
    @SubscribeEvent
    public void onClientTick(TickEvent.ClientTickEvent event) {
        if(!shouldFire){
            return;
        }


        Minecraft mc = Minecraft.getInstance();
        if (mc.level == null || mc.player == null) {
            return; // Ensure world and player are not null
        }

        LocalPlayer player = mc.player;
        ItemStack heldItem = player.getMainHandItem();

        if (heldItem.getItem() instanceof BowItem) {
            // Set the player's look direction (example: looking straight up)
            player.setYRot(aimPos.y); // -90 is straight up, 90 is straight down
            player.setXRot(aimPos.x); // 0 is north, 90 is east, 180 is south, -90 is west
            if(fired && fireWait > 0) {
                --fireWait;
                return;
            } else {
                fired = false;
                fireWait = 5;
            }

            // Simulate the bow drawing action
            if (shouldFire && player.getTicksUsingItem() == 0) {
                KeyMapping.set(Minecraft.getInstance().options.keyUse.getKey(), true);
            }

            // Simulate the bow release after holding it for some ticks
            if (player.getTicksUsingItem() >= fireTicks) {
                fired = true;
                shouldFire = false;
                KeyMapping.set(Minecraft.getInstance().options.keyUse.getKey(), false);;
            }
        }
    }
}
