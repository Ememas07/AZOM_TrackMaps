# Let's inspect PersistantTrackerPlugin methods in SimHub.Plugins.dll using IL or metadata
import subprocess

cmd = r'''
$asm = [System.Reflection.Assembly]::LoadFrom("C:\Program Files (x86)\SimHub\SimHub.Plugins.dll")
$type = $asm.GetType("SimHub.Plugins.DataPlugins.PersistantTracker.PersistantTrackerPlugin")
$methods = $type.GetMethods([System.Reflection.BindingFlags]"Public,NonPublic,Static,Instance")
foreach ($m in $methods) {
    if ($m.Name -like "*Map*") {
        Write-Host "$($m.ReturnType.Name) $($m.Name)($([string]::Join(', ', ($m.GetParameters() | ForEach-Object { $_.ParameterType.Name }))))"
    }
}
'''

r = subprocess.run([
    r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
    "-Command", cmd
], capture_output=True, text=True)

print("STDOUT:\n", r.stdout)
print("STDERR:\n", r.stderr)

