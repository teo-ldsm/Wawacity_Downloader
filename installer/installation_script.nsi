!include "MUI2.nsh"

Function .onInit
    ; Vérifier les privilèges administrateur
    UserInfo::GetAccountType
    Pop $0
    StrCmp $0 "admin" skipAdminCheck
        MessageBox MB_ICONEXCLAMATION|MB_OK "Vous devez exécuter ce programme en tant qu'administrateur."
        SetErrorLevel 740 ; ERROR_ELEVATION_REQUIRED
        Quit
    skipAdminCheck:
FunctionEnd

!define MUI_PAGE_CUSTOMFUNCTION_PRE SelectDirectoryPageInit
!insertmacro MUI_PAGE_DIRECTORY
Var INSTALL_DIR

Function SelectDirectoryPageInit
    StrCpy $INSTALL_DIR "$EXEDIR"
FunctionEnd

!insertmacro MUI_PAGE_INSTFILES


; TODO Changer les noms des fichiers

Section "Install"
    SetOutPath "$INSTALL_DIR\Wawacity_Downloader_v1.1.3"
    File "main.exe"
    SetOutPath "$INSTALL_DIR\Wawacity_Downloader_v1.1.3\Chrome"
    File /r "Chrome\*.*"
SectionEnd

Function .onInstSuccess
    ClearErrors
    ExecShell "open" "$INSTDIR"
FunctionEnd

Function .onGUIEnd
    ; Supprimer les répertoires temporaires
    RMDir /r "$TEMP"
FunctionEnd
