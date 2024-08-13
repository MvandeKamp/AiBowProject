package de.mvdk.aibowproject;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.event.entity.player.PlayerEvent;
import net.minecraftforge.server.ServerLifecycleHooks;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class TargetManager {
    private static final int RADIUS = 35;

    private Player player;
    private ServerLevel world;
    private List<BlockPos> targets = new ArrayList<BlockPos>();
    private GrpcClient grpcClient;

    public TargetManager(GrpcClient comClient) {
        grpcClient = comClient;
    }

    public boolean Start(PlayerEvent.PlayerLoggedInEvent event) {
        player = (Player) event.getEntity();
        world = ServerLifecycleHooks.getCurrentServer().overworld();
        SpawnNewTarget();
        return true;
    }

    public double DistanceToClosestTarget(Vec3 pos) {
        BlockPos closestTargetBlock = GetClosestTargetPos(pos, true);
        double distance = DistanceToCenter(pos, closestTargetBlock);
        return distance;
    }
    private double DistanceToCenter(Vec3 pos, BlockPos target) {
        return pos.distanceTo(new Vec3(target.getX() + 0.5, target.getY() + 0.5, target.getZ() + 0.5));
    }
    public BlockPos GetClosestTargetPos(Vec3 pos, boolean test) {
        BlockPos closestTargetBlock = new BlockPos(0, 0, 0);
        double closestDistance = 10000;
        for(BlockPos target : targets) {
            double distance = DistanceToCenter(pos, closestTargetBlock);
            if(distance <= closestDistance) {
                closestTargetBlock = target;
                closestDistance = distance;
            }
        }
        return closestTargetBlock;
    }

    public BlockPos IsHit(Vec3 pos) {
        BlockPos closestTargetBlock = GetClosestTargetPos(pos, true);
        double distance = DistanceToClosestTarget(pos);
        System.out.println("distance: " + distance);
        // Could calulate center of block but an offset should be precise enough
        if(distance < 1.35) {
            return closestTargetBlock;
        }
        return null;
    }

    public BlockPos RemoveOldSpawnNew(BlockPos pos) {
        world.setBlockAndUpdate(pos, Blocks.AIR.defaultBlockState());
        targets.remove(pos);
        return SpawnNewTarget();
    }

    public void RemoveAll(){
        for(BlockPos target : targets) {
            world.setBlockAndUpdate(target, Blocks.AIR.defaultBlockState());
        }
    }

    private BlockPos SpawnNewTarget(){
        Vec3 playerPos = player.getPosition(0f);
        Random random = new Random();

        int x = (int)playerPos.x() + random.nextInt(2 * RADIUS + 5) - RADIUS;
        int y = (int)playerPos.y() + random.nextInt(2 * RADIUS + 5) - RADIUS;
        int z = (int)playerPos.z() + random.nextInt(2 * RADIUS + 5) - RADIUS;
        if(y < 60){
            y = 60;
        }
        BlockPos targetPos = new BlockPos(x, y, z);
        targets.add(targetPos);
        boolean isEmpty = world.isEmptyBlock(targetPos);

        if (isEmpty) {
            world.setBlockAndUpdate(targetPos, Blocks.TARGET.defaultBlockState());
        }
        grpcClient.TargetRequest(new Vec3(x,y,z));
        return targetPos;
    }
}
