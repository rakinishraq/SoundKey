Set objShell = WScript.CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)
command = objFSO.BuildPath(scriptDir, ".venv\Scripts\pythonw.exe") & " " & objFSO.BuildPath(scriptDir, "main.py")

' Append each command line argument to the command string
For Each arg In WScript.Arguments
    command = command & " " & arg
Next

objShell.CurrentDirectory = scriptDir

objShell.Run command, 0, True