#Requires AutoHotkey v2.0
#SingleInstance Force

; everything after semicolon is a comment

; `+a` = Shift+A
; `^s` = Ctrl+S
; `#d` = Win+D (Win shortcuts are buggy sometimes though)
; `!v` = Alt+V
; `Numpad1` = Numpad's 1 key

Numpad1::Run("D:\\Projects\\ava\\LAUNCH.vbs output 0") ; group 1 of outputs from config.py
Numpad2::Run("D:\\Projects\\ava\\LAUNCH.vbs output 1") ; group 2 of outputs
Numpad3::Run("D:\\Projects\\ava\\LAUNCH.vbs input") ; all inputs groups combined