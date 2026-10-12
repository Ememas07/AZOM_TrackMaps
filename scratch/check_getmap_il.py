import subprocess

cmd = r'''
$asm = [System.Reflection.Assembly]::LoadFrom("C:\Program Files (x86)\SimHub\SimHub.Plugins.dll")
$type = $asm.GetType("SimHub.Plugins.DataPlugins.PersistantTracker.PersistantTrackerPlugin")
$m = $type.GetMethod("GetMap", [System.Reflection.BindingFlags]"Public,Static", $null, [System.Type]::EmptyTypes, $null)
$body = $m.GetMethodBody()
Write-Host "GetMap IL size: $($body.GetILAsByteArray().Length)"

$m2 = $type.GetMethod("GetMap", [System.Reflection.BindingFlags]"Public,Static", $null, @([bool]), $null)
$body2 = $m2.GetMethodBody()
Write-Host "GetMap(bool) IL size: $($body2.GetILAsByteArray().Length)"
'''

r = subprocess.run([
    r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
    "-Command", cmd
], capture_output=True, text=True)

print("STDOUT:\n", r.stdout)
print("STDERR:\n", r.stderr)

