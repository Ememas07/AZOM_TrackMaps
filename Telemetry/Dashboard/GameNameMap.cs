using System;
using System.Collections.Generic;
using System.IO;
using MozaPlugin.Diagnostics;

namespace MozaPlugin.Telemetry.Dashboard
{
    /// <summary>
    /// Maps SimHub's game code (<c>PluginManager.GameName</c>, e.g.
    /// "AssettoCorsaCompetizione") to the short string MOZA PitHouse publishes
    /// on the <c>patch/GameName</c> channel ("ACC"). Wheel dashboards branch
    /// on the PitHouse strings — verified against the FSR2 "LD - Marco" /
    /// "Lovely Dashboard FSR2" dashes, whose layout logic compares
    /// <c>patch/GameName</c> against "AC", "ACC", "Automobilista 2" and
    /// "rFactor 2".
    ///
    /// Only those four games are remapped — they are the ones with ground
    /// truth from real dashboards. Any other game passes its SimHub code
    /// through unchanged: that is informative and clearly the plugin's own
    /// value, never a fabricated PitHouse short-code we have no capture for.
    /// </summary>
    internal static class GameNameMap
    {
        private static readonly Dictionary<string, string> ToMoza =
            new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
            {
                ["AssettoCorsa"]             = "AC",
                ["AssettoCorsaCompetizione"] = "ACC",
                ["Automobilista2"]           = "Automobilista 2",
                ["rFactor2"]                 = "rFactor 2",
            };

        /// <summary>
        /// MOZA <c>patch/GameName</c> string for a SimHub game code, or the
        /// code itself when unmapped. Empty string when no game is running.
        /// </summary>
        internal static string Resolve(string? simHubGameName)
        {
            if (string.IsNullOrEmpty(simHubGameName)) return "";
            return ToMoza.TryGetValue(simHubGameName!, out var moza) ? moza : simHubGameName!;
        }

        // MOZA track-map identifier "<gameprefix>/<track>" for patch/TrackName —
        // the key the wheel uses to load the track's map background. Confirmed
        // from AC captures: "ac/imola", "ac/spa". The prefix is the lowercased
        // MOZA short code from the same ToMoza dictionary used by Resolve
        // (AC → "ac", ACC → "acc"); only AC is capture-verified. Unknown games
        // fall through to the bare track name (no worse than before the prefix).
        // For games with distinct track layouts/configs (e.g. iRacing Nürburgring
        // GP vs Nordschleife vs Combined, or Indianapolis Road vs Oval), matches
        // against PitHouse's bundled .mztrack names so the wheel displays the
        // correct track circuit map.
        internal static string TrackPath(string? simHubGameName, string? trackName, string? trackConfig = null, string? trackCode = null)
        {
            if (string.IsNullOrEmpty(trackName) && string.IsNullOrEmpty(trackCode)) return "";
            string prefix = Resolve(simHubGameName).ToLowerInvariant();
            string resolvedTrack = ResolveTrackNameForWheel(prefix, trackName, trackConfig, trackCode);
            return prefix.Length == 0 ? resolvedTrack : prefix + "/" + resolvedTrack;
        }

        private static readonly object s_trackDataLock = new object();
        private static readonly Dictionary<string, Dictionary<string, string>> s_gameTracksCased
            = new Dictionary<string, Dictionary<string, string>>(StringComparer.OrdinalIgnoreCase);

        private static string ResolveTrackNameForWheel(string gamePrefix, string? trackName, string? trackConfig, string? trackCode)
        {
            EnsureTrackDataLoaded(gamePrefix);

            string t = (trackName ?? "").Trim();
            string cfg = (trackConfig ?? "").Trim();
            string code = (trackCode ?? "").Trim();

            if (s_gameTracksCased.TryGetValue(gamePrefix, out var tracksMap) && tracksMap.Count > 0)
            {
                // Try candidate matches in priority order
                var candidates = new List<string>();
                if (!string.IsNullOrEmpty(t) && !string.IsNullOrEmpty(cfg))
                {
                    candidates.Add($"{t} {cfg}");
                    candidates.Add($"{t}{cfg}");
                }
                if (!string.IsNullOrEmpty(code))
                    candidates.Add(code);
                if (!string.IsNullOrEmpty(t))
                    candidates.Add(t);

                foreach (var cand in candidates)
                {
                    string candClean = cand.ToLowerInvariant();
                    if (tracksMap.TryGetValue(candClean, out var match))
                        return match;
                }

                // If no exact match, try prefix / substring match
                if (!string.IsNullOrEmpty(t))
                {
                    string tLower = t.ToLowerInvariant();
                    string cfgLower = cfg.ToLowerInvariant();
                    foreach (var kv in tracksMap)
                    {
                        if (kv.Key.StartsWith(tLower, StringComparison.OrdinalIgnoreCase))
                        {
                            if (!string.IsNullOrEmpty(cfgLower) && kv.Key.Contains(cfgLower))
                                return kv.Value;
                        }
                    }
                    foreach (var kv in tracksMap)
                    {
                        if (kv.Key.StartsWith(tLower, StringComparison.OrdinalIgnoreCase))
                            return kv.Value;
                    }
                }
            }

            // Fallback when PitHouse TrackData not available on disk or uncatalogued
            if (!string.IsNullOrEmpty(t) && !string.IsNullOrEmpty(cfg)
                && !t.EndsWith(cfg, StringComparison.OrdinalIgnoreCase))
            {
                return $"{t} {cfg}";
            }
            return !string.IsNullOrEmpty(t) ? t : code;
        }

        private static void EnsureTrackDataLoaded(string gamePrefix)
        {
            if (s_gameTracksCased.ContainsKey(gamePrefix)) return;
            lock (s_trackDataLock)
            {
                if (s_gameTracksCased.ContainsKey(gamePrefix)) return;
                var map = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

                string[] searchRoots = new[]
                {
                    Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "MOZA Pit House", "bin", "GameConfigs", "TrackData"),
                    Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "MOZA Pit House", "bin", "GameConfigs", "TrackData"),
                    Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "pithouse2", "bin", "GameConfigs", "TrackData"),
                };

                foreach (var root in searchRoots)
                {
                    string dir = Path.Combine(root, gamePrefix);
                    if (Directory.Exists(dir))
                    {
                        try
                        {
                            foreach (var f in Directory.GetFiles(dir, "*.mztrack"))
                            {
                                string baseName = Path.GetFileNameWithoutExtension(f);
                                map[baseName.ToLowerInvariant()] = baseName;
                            }
                            if (map.Count > 0)
                            {
                                MozaLog.Info($"[AZOM] loaded {map.Count} wheel track names for '{gamePrefix}' from '{dir}'");
                                break;
                            }
                        }
                        catch { }
                    }
                }

                s_gameTracksCased[gamePrefix] = map;
            }
        }
    }
}
