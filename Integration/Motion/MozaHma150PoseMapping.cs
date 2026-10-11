using System;
using MozaPlugin.Devices.Motion;
using MozaPlugin.Protocol;

namespace MozaPlugin.Integration.Motion
{
    /// <summary>
    /// SimHub's final pose (6DOF bypass geometry) → the controller's mode-1 telemetry frame.
    ///
    /// PROVISIONAL until the Phase 0 characterization (tools/hma150-characterize.ps1)
    /// measures how the controller's own cueing responds to each field.
    ///
    /// Pitch and roll go into the attitude fields f0/f1 (rad), which the controller applies
    /// directly (its logged pitch/roll equal f0/f1). Signs follow the handover bridge, whose
    /// SimHub inputs matched Motion Manager's stream: SimHub pose pitch is −OrientationPitch,
    /// the bridge sent +OrientationPitch; the bridge sent −OrientationRoll.
    ///
    /// Game mode has no heave position field: the controller builds heave from the four
    /// suspension deflections (f8–f11) through the Heave slot, and road texture from the
    /// same fields through Road Detail. Pose heave is therefore sent as a common-mode
    /// offset on all four shocks. Sign and gain come from Motion Manager's game captures
    /// (12 Output Displacement snapshots: platform heave ≈ −0.58 mm per mm of high-passed
    /// mean deflection at Heave 0.30, so ≈ −1.9 at 1.0; Manual Input heave −1 gave +13.4 mm,
    /// so negative displacement is up) — compression lifts the platform. The controller
    /// appears to wash a held offset out over 1–10 s.
    /// </summary>
    internal static class MozaHma150PoseMapping
    {
        private const double DegToRad = Math.PI / 180.0;

        public const int FrameIntervalMs = 30;

        // Shock-deflection mm per mm of pose heave (provisional, see above).
        private const double HeaveToShock = 0.5;

        public static MotionEngageConfig EngageConfig()
        {
            var c = new MotionEngageConfig { FrameIntervalMs = FrameIntervalMs };
            c.Slots.Add((MozaMotionProtocol.SlotPitch, 1f, 0f));
            c.Slots.Add((MozaMotionProtocol.SlotRoll, 1f, 0f));
            c.Slots.Add((MozaMotionProtocol.SlotHeave, 1f, 0f));
            // Acceleration cueing would add tilt on top of SimHub's pose; f4/f5 stay 0.
            c.Slots.Add((MozaMotionProtocol.SlotAccelPitch, 0f, 0f));
            c.Slots.Add((MozaMotionProtocol.SlotAccelRoll, 0f, 0f));
            c.RoadDetailIntensity = 1f;
            c.RoadDetailSmoothness = 0f;
            return c;
        }

        public static MotionTelemetryFrame ToFrame(double pitchDegrees, double rollDegrees, double heaveMm)
        {
            var f = MotionTelemetryFrame.Neutral(inGame: true);
            f.Fields[0] = (float)(-pitchDegrees * DegToRad);
            f.Fields[1] = (float)(-rollDegrees * DegToRad);
            float shock = (float)(heaveMm * HeaveToShock);
            for (int i = 0; i < 4; i++)
                f.Fields[8 + i] += shock;
            return f;
        }
    }
}
