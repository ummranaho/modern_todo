; ============================================
; Modern To-Do App Installer Script
; ============================================

#define MyAppName "Modern To-Do"
#define MyAppVersion "1.0"
#define MyAppPublisher "Your Name"
#define MyAppExeName "modern_todo.exe"
#define MyAppURL "https://yourwebsite.com"

[Setup]
AppId={{F4E2C8D1-9B23-4A3B-8F21-ABCDE1234567}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=installer_output
OutputBaseFilename=ModernToDo_Setup
SetupIconFile=assets\icon\strawberry.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}

; Require admin privileges for installation
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
; Main EXE file
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Optional: Include additional files if needed (e.g., data files)
; Source: "dist\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

; Include icon file in app folder (optional)
Source: "assets\icon\strawberry.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcut
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\strawberry.ico"

; Desktop shortcut
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon; IconFilename: "{app}\strawberry.ico"

[Run]
; Launch app after install
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Remove leftover task file if exists
Type: files; Name: "{app}\tasks.json"
