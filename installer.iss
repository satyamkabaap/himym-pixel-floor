; Inno Setup script for HIMYM Harness
; Version 7.0.0
#define MyAppName "HIMYM Harness"
#define MyAppVersion "9.0.0"
#define MyAppPublisher "HIMYM Project"
#define MyAppURL "http://example.com/"
#define MyAppExe "director.py"

[Setup]
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputBaseFilename=HIMYMHarness-7.0.0
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "director.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "himym_data\*"; DestDir: "{app}\himym_data"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dashboard.html"; DestDir: "{app}"; Flags: ignoreversion
Source: "floor_day.png"; DestDir: "{app}"; Flags: ignoreversion
Source: "floor_night.png"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExe}"
Name: "{commondesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExe}"; Tasks: desktopicon

[Run]
Filename: "{app}\\{#MyAppExe}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent