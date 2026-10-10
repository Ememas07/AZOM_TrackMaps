using System;
using System.Collections.Generic;
using MozaPlugin.Protocol;

namespace MozaPlugin.Devices.Motion
{
    /// <summary>Where the motion lane is in its connect / engage lifecycle.</summary>
    public enum MotionLanePhase
    {
        Disconnected,
        Enrolling,
        Ready,
        SelfChecking,
        EnteringGame,
        Game,
        Disengaging,
        PortSelfTest,
        Faulted,
    }

    /// <summary>
    /// Effect-slot values pushed on engage. The pose-injection pass-through values come
    /// from Phase 0 characterization; until then the caller supplies them.
    /// </summary>
    public sealed class MotionEngageConfig
    {
        public readonly List<(byte Slot, float Intensity, float Smoothness)> Slots
            = new List<(byte, float, float)>();
        public float RoadDetailIntensity;
        public float RoadDetailSmoothness;
        public int FrameIntervalMs = 30;
    }

    public enum MotionConfigIssueKind
    {
        NotConnected,
        Enrolling,
        PortUnassigned,
        PortDuplicate,
        ActuatorsMissing,
        PortConfigPending,
    }

    /// <summary>A problem that blocks an engage. <see cref="Value"/> is the port, or the actuator count.</summary>
    public readonly struct MotionConfigIssue
    {
        public readonly MotionConfigIssueKind Kind;
        public readonly int Value;
        public readonly int Expected;
        public readonly MotionCorner Corner;

        public MotionConfigIssue(MotionConfigIssueKind kind, int value = 0, MotionCorner corner = MotionCorner.None, int expected = 0)
        {
            Kind = kind;
            Value = value;
            Corner = corner;
            Expected = expected;
        }

        public override string ToString() => Kind switch
        {
            MotionConfigIssueKind.PortUnassigned => $"port {Value} has no corner",
            MotionConfigIssueKind.PortDuplicate => $"port {Value} duplicates {Corner}",
            MotionConfigIssueKind.ActuatorsMissing => $"{Value} of {Expected} actuators",
            _ => Kind.ToString(),
        };
    }

    public sealed class MotionPortSnapshot
    {
        public int Port;
        public bool? Present;
        public byte Slave;
        public MotionCorner? Role;
        public uint StatusWord;
    }

    /// <summary>Point-in-time copy of the lane state for UI, diagnostics and properties.</summary>
    public sealed class MotionControllerSnapshot
    {
        public bool Connected;
        public string? PortName;
        public MotionLanePhase Phase;
        public string? FaultReason;

        public string ModelName = string.Empty;
        public string HardwareId = string.Empty;
        public string HardwareRevision = string.Empty;
        public string FirmwareVersion = string.Empty;
        public string HardwareVersion = string.Empty;
        public string Uid = string.Empty;

        public int SupportedActuators;
        public int PortCount;

        public int ModeTarget = -1;
        public int ModeCurrent = -1;
        public byte Flags;
        public int RunState = -1;
        public int ActuatorsPresent;
        public int ActuatorsEnrolled;
        public bool SelfCheckPassed;
        public IReadOnlyList<int> ActiveErrorCodes = Array.Empty<int>();

        public float? MaxStroke;
        public float? HapticIntensity;
        public float? RigLengthMm;
        public float? RigWidthMm;

        public MotionPortSnapshot[] Ports = Array.Empty<MotionPortSnapshot>();
        public long FramesSent;
        public IReadOnlyList<string> RecentLog = Array.Empty<string>();
    }
}
