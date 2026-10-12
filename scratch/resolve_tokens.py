import subprocess

cmd = r'''
$asm = [System.Reflection.Assembly]::LoadFrom("C:\Program Files (x86)\SimHub\SimHub.Plugins.dll")
$module = $asm.ManifestModule
$tokens = @(0x06004F74, 0x06000DF8, 0x0A000330, 0x06000DFA, 0x0A001864, 0x06004F72, 0x06004F88)
foreach ($t in $tokens) {
    try {
        $mb = $module.ResolveMethod($t)
        Write-Host ("0x{0:X8}: {1}.{2}" -f $t, $mb.DeclaringType.Name, $mb.Name)
    } catch {
        Write-Host ("0x{0:X8}: err {1}" -f $t, $_.Exception.Message)
    }
}
'''

r = subprocess.run([
    r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe",
    "-Command", cmd
], capture_output=True, text=True)

print("STDOUT:\n", r.stdout)

