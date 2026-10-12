using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
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
        // Always lowercased because the wheel firmware runs embedded Linux
        // (aarch64) where /home/moza/resource/maps/ has case-sensitive lowercase files.
        internal static string TrackPath(string? simHubGameName, string? trackName, string? trackConfig = null, string? trackCode = null)
        {
            if (string.IsNullOrEmpty(trackName) && string.IsNullOrEmpty(trackCode)) return "";
            string prefix = Resolve(simHubGameName).ToLowerInvariant();
            string resolvedTrack = ResolveTrackNameForWheel(prefix, trackName, trackConfig, trackCode).ToLowerInvariant();
            return prefix.Length == 0 ? resolvedTrack : prefix + "/" + resolvedTrack;
        }

        private static readonly object s_trackDataLock = new object();
        private static readonly Dictionary<string, Dictionary<string, string>> s_gameTracksCased
            = new Dictionary<string, Dictionary<string, string>>(StringComparer.OrdinalIgnoreCase);

        private static readonly (string Alias, string Canonical)[] TrackSynonyms = new[]
        {
            ("nordschleife", "nurburgring"),
            ("nords", "nurburgring"),
            ("redbullring", "spielberg"),
            ("mountpanorama", "bathurst"),
            ("weathertech", "lagunaseca"),
            ("circuitoftheamericas", "cota"),
            ("josecarlospace", "interlagos"),
        };

        internal static string Clean(string? s)
        {
            if (string.IsNullOrWhiteSpace(s) || s == null) return "";
            var sb = new StringBuilder(s.Length);
            foreach (char c in s)
            {
                if (char.IsLetterOrDigit(c))
                    sb.Append(char.ToLowerInvariant(c));
            }
            return sb.ToString();
        }

        internal static string ResolveTrackNameForWheel(string gamePrefix, string? trackName, string? trackConfig, string? trackCode)
        {
            EnsureTrackDataLoaded(gamePrefix);

            string t = (trackName ?? "").Trim();
            string cfg = (trackConfig ?? "").Trim();
            string code = (trackCode ?? "").Trim();

            if (s_gameTracksCased.TryGetValue(gamePrefix, out var tracksMap) && tracksMap.Count > 0)
            {
                // Generate candidates in priority order
                var candidates = new List<string>();

                // Special handling for Nürburgring / Nordschleife layout variants
                string combinedSearch = $"{t} {cfg} {code}".ToLowerInvariant();
                if (combinedSearch.Contains("nords") || combinedSearch.Contains("nurburg"))
                {
                    if (combinedSearch.Contains("tourist"))
                        candidates.Add("nurburgring nordschleifetourist");
                    if (combinedSearch.Contains("shortb") || combinedSearch.Contains("short b"))
                        candidates.Add("nurburgring combinedshortb");
                    if (combinedSearch.Contains("shorta") || combinedSearch.Contains("short a"))
                        candidates.Add("nurburgring combinedshorta");
                    if (combinedSearch.Contains("long"))
                        candidates.Add("nurburgring combinedlong");
                    if (combinedSearch.Contains("combined"))
                        candidates.Add("nurburgring combined");
                    if (combinedSearch.Contains("nords") && !combinedSearch.Contains("combined") && !combinedSearch.Contains("short") && !combinedSearch.Contains("long"))
                        candidates.Add("nurburgring nordschleife");
                }

                if (!string.IsNullOrEmpty(t) && !string.IsNullOrEmpty(cfg))
                {
                    candidates.Add($"{t} {cfg}");
                    candidates.Add($"{t}{cfg}");
                }
                if (!string.IsNullOrEmpty(code))
                {
                    candidates.Add(code);
                    candidates.Add(code.Replace("-", " ").Replace("_", " "));
                }
                if (!string.IsNullOrEmpty(t))
                {
                    candidates.Add(t);
                    candidates.Add(t.Replace("-", " ").Replace("_", " "));
                }

                // Add synonym-expanded versions of candidates
                int count = candidates.Count;
                for (int i = 0; i < count; i++)
                {
                    string candLower = candidates[i].ToLowerInvariant();
                    foreach (var syn in TrackSynonyms)
                    {
                        if (candLower.Contains(syn.Alias))
                        {
                            candidates.Add(candLower.Replace(syn.Alias, syn.Canonical));
                        }
                    }
                }

                // 1. Exact clean match (alphanumerics only)
                foreach (var cand in candidates)
                {
                    string candClean = Clean(cand);
                    if (string.IsNullOrEmpty(candClean)) continue;
                    if (tracksMap.TryGetValue(candClean, out var match))
                        return match;
                }

                // 2. Token-based overlap match against known PitHouse tracks
                string bestMatch = "";
                int bestScore = 0;
                var queryTokens = ExtractTokens(combinedSearch);

                foreach (var kv in tracksMap)
                {
                    string trackClean = kv.Key; // already Clean
                    string trackVal = kv.Value;

                    int score = 0;
                    bool hasBaseMatch = false;

                    // Base track match check
                    foreach (var syn in TrackSynonyms)
                    {
                        if (queryTokens.Contains(syn.Alias) && trackClean.Contains(syn.Canonical))
                            hasBaseMatch = true;
                    }

                    foreach (var token in queryTokens)
                    {
                        if (trackClean.Contains(token))
                        {
                            hasBaseMatch = true;
                            score += (token.Length > 2) ? 10 : 5;
                        }
                    }

                    if (hasBaseMatch && score > bestScore)
                    {
                        bestScore = score;
                        bestMatch = trackVal;
                    }
                }

                if (!string.IsNullOrEmpty(bestMatch))
                    return bestMatch;
            }

            // Fallback when PitHouse TrackData not available on disk or uncatalogued
            string fallback = "";
            if (!string.IsNullOrEmpty(t) && !string.IsNullOrEmpty(cfg)
                && !t.EndsWith(cfg, StringComparison.OrdinalIgnoreCase))
            {
                fallback = $"{t} {cfg}";
            }
            else
            {
                fallback = !string.IsNullOrEmpty(t) ? t : code;
            }

            // Apply synonyms to fallback as well
            string fbLower = fallback.ToLowerInvariant();
            foreach (var syn in TrackSynonyms)
            {
                if (fbLower.Contains(syn.Alias))
                    fbLower = fbLower.Replace(syn.Alias, syn.Canonical);
            }
            return fbLower;
        }

        private static HashSet<string> ExtractTokens(string s)
        {
            var set = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            var sb = new StringBuilder();
            foreach (char c in s)
            {
                if (char.IsLetterOrDigit(c))
                {
                    sb.Append(char.ToLowerInvariant(c));
                }
                else
                {
                    if (sb.Length > 0)
                    {
                        set.Add(sb.ToString());
                        sb.Clear();
                    }
                }
            }
            if (sb.Length > 0)
                set.Add(sb.ToString());
            return set;
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
                    Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "pithouse2", "bin", "GameConfigs", "TrackData"),
                    Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "pithouse2", "bin", "GameConfigs", "TrackData"),
                    Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "MOZA Pit House", "bin", "GameConfigs", "TrackData"),
                    Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "MOZA Pit House", "bin", "GameConfigs", "TrackData"),
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
                                string clean = Clean(baseName);
                                if (!string.IsNullOrEmpty(clean) && !map.ContainsKey(clean))
                                {
                                    map[clean] = baseName.ToLowerInvariant();
                                }
                            }
                        }
                        catch { }
                    }
                }

                if (map.Count > 0)
                {
                    MozaLog.Info($"[AZOM] loaded {map.Count} wheel track names for '{gamePrefix}'");
                }

                s_gameTracksCased[gamePrefix] = map;
            }
        }
    }
}
