using System;
using MozaPlugin.Devices.Motion;

namespace MozaPlugin
{
    /// <summary>
    /// MOZA Motion Controller (HMA150 platform) lane: owned for the life of the plugin
    /// instance, connected from the 5 s reconnect tick whenever the controller is present.
    /// The SimHub Motion output attaches to it through <see cref="MotionController"/>.
    /// </summary>
    public partial class MozaPlugin
    {
        private MozaMotionController? _motionController;

        internal MozaMotionController? MotionController => _motionController;

        /// <summary>Whether SimHub Motion has the HMA150 output in its active setup (status banner).</summary>
        internal Integration.Motion.MotionSetupStatus MotionSetupStatus
            => Integration.Motion.MotionIntegration.GetSetupStatus(_pluginManager);

        private void InitMotionLane()
        {
            _motionController = new MozaMotionController(() => IsShuttingDown);
            if (!string.IsNullOrEmpty(_settings.LastMotionPort))
                _motionController.LastPortName = _settings.LastMotionPort;
            if (!string.IsNullOrEmpty(_settings.LastMotionDeviceId))
                _motionController.LastDeviceId = _settings.LastMotionDeviceId;
        }

        /// <summary>Reconnect-tick hook; same authoritative-device-source gate as the other dedicated lanes.</summary>
        private void TryConnectMotion()
        {
            var lane = _motionController;
            if (lane == null || lane.IsConnected || IsShuttingDown) return;
            if (!lane.TryConnect()) return;

            bool dirty = false;
            string port = lane.LastPortName ?? "";
            if (port.Length != 0 && _settings.LastMotionPort != port) { _settings.LastMotionPort = port; dirty = true; }
            string id = lane.LastDeviceId ?? "";
            if (_settings.LastMotionDeviceId != id) { _settings.LastMotionDeviceId = id; dirty = true; }
            if (dirty) ScheduleSave();

            // Presets only once a controller has been seen, so other users get no entry.
            Integration.Motion.MotionPresetDeployer.Deploy();
        }

        private void DisposeMotionLane()
        {
            try { _motionController?.Dispose(); } catch { }
            _motionController = null;
        }
    }
}
