Set objShell = WScript.CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
command = objFSO.BuildPath(scriptDir, ".venv\Scripts\python.exe") & " " & objFSO.BuildPath(scriptDir, "main.py")

objShell.CurrentDirectory = scriptDir

objShell.Run command, 0, True