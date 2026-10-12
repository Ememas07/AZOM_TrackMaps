import subprocess

cmd = r'''
$asm = [System.Reflection.Assembly]::LoadFrom("C:\Program Files (x86)\SimHub\SimHub.Plugins.dll")
$type = $asm.GetType("SimHub.Plugins.DataPlugins.PersistantTracker.PersistantTrackerPlugin")
$m = $type.GetMethod("GetMap", [System.Reflection.BindingFlags]"Public,Static", $null, @([bool]), $null)
$bytes = $m.GetMethodBody().GetILAsByteArray()
Write-Host ($bytes | ForEach-Object { "{0:X2}" -f $_ }) -separator " "
'''

r = subprocess.run([
    r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
    "-Command", cmd
], capture_output=True, text=True)

print("STDOUT:\n", r.stdout)

