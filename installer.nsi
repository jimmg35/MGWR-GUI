Name "MGWR-GUI"
OutFile "dist\MGWR-GUI-Setup.exe"
InstallDir "$PROGRAMFILES64\MGWR-GUI"
InstallDirRegKey HKCU "Software\MGWR-GUI" "InstallDir"
RequestExecutionLevel admin

Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "dist\MGWR-GUI\*"

  CreateDirectory "$SMPROGRAMS\MGWR-GUI"
  CreateShortcut "$SMPROGRAMS\MGWR-GUI\MGWR-GUI.lnk" "$INSTDIR\MGWR-GUI.exe"
  CreateShortcut "$DESKTOP\MGWR-GUI.lnk" "$INSTDIR\MGWR-GUI.exe"

  WriteUninstaller "$INSTDIR\Uninstall.exe"
  WriteRegStr HKCU "Software\MGWR-GUI" "InstallDir" "$INSTDIR"
SectionEnd

Section "Uninstall"
  Delete "$DESKTOP\MGWR-GUI.lnk"
  Delete "$SMPROGRAMS\MGWR-GUI\MGWR-GUI.lnk"
  RMDir "$SMPROGRAMS\MGWR-GUI"

  Delete "$INSTDIR\Uninstall.exe"
  RMDir /r "$INSTDIR"

  DeleteRegKey HKCU "Software\MGWR-GUI"
SectionEnd
