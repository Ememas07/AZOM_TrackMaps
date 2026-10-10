using System;
using MozaPlugin.Devices.Motion;
using MozaPlugin.Protocol;

namespace MozaPlugin.Integration.Motion
{
    /// <summary>
    /// SimHub's final pose (6DOF bypass geometry) → the controller's mode-1 telemetry frame.
    ///
    /// PROVISIONAL until the Phase 0 characterization (tools/hma150-characterize.ps1)
    /// measures how the controller's own cueing responds to each field. Until then:
    /// pitch and roll go into the attitude fields f0/f1 (rad) with the pitch/roll slots at
    /// full intensity and no smoothing, every other slot and road detail off, all other
    /// fields at rest. Heave is not mapped — the controller has no position-like heave
    /// field identified yet. Signs follow the handover bridge, whose SimHub inputs matched
    /// Motion Manager's stream: SimHub pose pitch is −OrientationPitch, the bridge sent
    /// +OrientationPitch; the bridge sent −OrientationRoll.
    /// </summary>
    internal static class MozaHma150PoseMapping
    {
        private const double DegToRad = Math.PI / 180.0;

        public const int FrameIntervalMs = 30;

        public static MotionEngageConfig EngageConfig()
        {
            var c = new MotionEngageConfig { FrameIntervalMs = FrameIntervalMs };
            c.Slots.Add((MozaMotionProtocol.SlotPitch, 1f, 0f));
            c.Slots.Add((MozaMotionProtocol.SlotRoll, 1f, 0f));
            c.Slots.Add((MozaMotionProtocol.SlotHeave, 0f, 0f));
            c.Slots.Add((MozaMotionProtocol.SlotAccelPitch, 0f, 0f));
            c.Slots.Add((MozaMotionProtocol.SlotAccelRoll, 0f, 0f));
            c.RoadDetailIntensity = 0f;
            c.RoadDetailSmoothness = 0f;
            return c;
        }

        public static MotionTelemetryFrame ToFrame(double pitchDegrees, double rollDegrees)
        {
            var f = MotionTelemetryFrame.Neutral(inGame: true);
            f.Fields[0] = (float)(-pitchDegrees * DegToRad);
            f.Fields[1] = (float)(-rollDegrees * DegToRad);
            return f;
        }
    }
}
