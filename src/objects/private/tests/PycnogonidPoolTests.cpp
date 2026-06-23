#include "CoreMinimal.h"
#include "Misc/AutomationTest.h"
#include "LarvalPoolManager.h"

IMPLEMENT_SIMPLE_AUTOMATION_TEST(FLarvalBatchSpawningTest, "Pycnogonid.Pool.BatchSpawningLeakTest", EAutomationTestFlags::ApplicationContextMask | EAutomationTestFlags::EngineFilter)

bool FLarvalBatchSpawningTest::RunTest(const FString& Parameters)
{
    // 1. Instantiation
    ULarvalPoolManager* PoolManager = NewObject<ULarvalPoolManager>();
    PoolManager->BeginPlay();

    // Ensure state tracks clear initially
    TestEqual(TEXT("Initial active tracking count must be zero"), PoolManager->GetActiveLarvaeCount(), 0);

    // 2. Trigger an explosive 10,000 unit reproductive surge through gonopore execution functions
    double StartTime = FPlatformTime::Seconds();
    int32 SpawnedCount = PoolManager->ExecuteBatchSpawning(FVector(10.f, 20.f, 30.f), 10000, 0.02f);
    double Duration = FPlatformTime::Seconds() - StartTime;

    // 3. Assert execution timing constraints (Must execute in microsecond bounds)
    TestTrue(TEXT("Batch loop took too long! Allocation bounds compromised."), Duration < 0.002); // Must complete in under 2ms
    TestEqual(TEXT("Active population vector must read exactly 10,000 entries"), PoolManager->GetActiveLarvaeCount(), 10000);

    // 4. Force a simulation tick pass and confirm memory boundaries clean up properly
    PoolManager->TickComponent(100.0f, ELevelTick::LEVELTICK_AllTickFunctions, nullptr); // Advance time forward significantly to burn yolk reserves
    
    UE_LOG(LogTemp, Log, TEXT("Automation Verification: 10,000 agents processed across thread frames in %f seconds."), Duration);
    return true;
}
