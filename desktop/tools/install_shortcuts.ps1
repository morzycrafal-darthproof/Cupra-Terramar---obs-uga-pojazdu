# Tworzy skróty "Cupra Terramar" w Menu Start i na pulpicie (pythonw, bez okna konsoli).
# Skróty mają ten sam AppUserModelID co okno programu, więc przypięcie do paska zadań
# (także z działającego okna) uruchamia program z właściwą ikoną.
#
#   powershell -ExecutionPolicy Bypass -File desktop\tools\install_shortcuts.ps1

$ErrorActionPreference = "Stop"
$AppId = "CupraTerramar.Dziennik"   # = SetCurrentProcessExplicitAppUserModelID w cupra_terramar_gui.py
$Name = "Cupra Terramar"

$desktopDir = Split-Path -Parent $PSScriptRoot
$script = Join-Path $desktopDir "cupra_terramar_gui.py"
$icon = Join-Path $desktopDir "assets\app.ico"
$python = (& py -c "import sys; print(sys.executable)").Trim()
$pythonw = Join-Path (Split-Path -Parent $python) "pythonw.exe"
if (-not (Test-Path $pythonw)) { throw "Nie znaleziono pythonw.exe obok $python" }

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Runtime.InteropServices.ComTypes;
using System.Text;

namespace CupraShortcut {
  [ComImport, Guid("000214F9-0000-0000-C000-000000000046"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
  interface IShellLinkW {
    void GetPath([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder f, int cch, IntPtr fd, int flags);
    void GetIDList(out IntPtr pidl);
    void SetIDList(IntPtr pidl);
    void GetDescription([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder s, int cch);
    void SetDescription([MarshalAs(UnmanagedType.LPWStr)] string s);
    void GetWorkingDirectory([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder s, int cch);
    void SetWorkingDirectory([MarshalAs(UnmanagedType.LPWStr)] string s);
    void GetArguments([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder s, int cch);
    void SetArguments([MarshalAs(UnmanagedType.LPWStr)] string s);
    void GetHotkey(out short k);
    void SetHotkey(short k);
    void GetShowCmd(out int c);
    void SetShowCmd(int c);
    void GetIconLocation([Out, MarshalAs(UnmanagedType.LPWStr)] StringBuilder s, int cch, out int i);
    void SetIconLocation([MarshalAs(UnmanagedType.LPWStr)] string s, int i);
    void SetRelativePath([MarshalAs(UnmanagedType.LPWStr)] string s, int r);
    void Resolve(IntPtr hwnd, int flags);
    void SetPath([MarshalAs(UnmanagedType.LPWStr)] string s);
  }

  [StructLayout(LayoutKind.Sequential, Pack = 4)]
  struct PropertyKey { public Guid fmtid; public uint pid; }

  [StructLayout(LayoutKind.Explicit, Size = 24)]
  struct PropVariant { [FieldOffset(0)] public ushort vt; [FieldOffset(8)] public IntPtr p; }

  [ComImport, Guid("886D8EEB-8CF2-4446-8D02-CDBA1DBDCF99"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
  interface IPropertyStore {
    void GetCount(out uint n);
    void GetAt(uint i, out PropertyKey key);
    void GetValue(ref PropertyKey key, out PropVariant v);
    void SetValue(ref PropertyKey key, ref PropVariant v);
    void Commit();
  }

  public static class Lnk {
    static readonly PropertyKey AppUserModelId =
      new PropertyKey { fmtid = new Guid("9F4C2855-9F79-4B39-A8D0-E1D42DE1D5F3"), pid = 5 };

    public static void Create(string path, string target, string args, string workDir, string icon,
                              string description, string appId) {
      var link = (IShellLinkW)Activator.CreateInstance(Type.GetTypeFromCLSID(new Guid("00021401-0000-0000-C000-000000000046")));
      link.SetPath(target);
      link.SetArguments(args);
      link.SetWorkingDirectory(workDir);
      link.SetIconLocation(icon, 0);
      link.SetDescription(description);
      var store = (IPropertyStore)link;
      var key = AppUserModelId;
      var value = new PropVariant { vt = 31, p = Marshal.StringToCoTaskMemUni(appId) };  // VT_LPWSTR
      try { store.SetValue(ref key, ref value); store.Commit(); }
      finally { Marshal.FreeCoTaskMem(value.p); }
      ((IPersistFile)link).Save(path, true);
    }

    public static string ReadAppId(string path) {
      var link = (IShellLinkW)Activator.CreateInstance(Type.GetTypeFromCLSID(new Guid("00021401-0000-0000-C000-000000000046")));
      ((IPersistFile)link).Load(path, 0);
      var key = AppUserModelId;
      PropVariant v;
      ((IPropertyStore)link).GetValue(ref key, out v);
      return v.vt == 31 ? Marshal.PtrToStringUni(v.p) : null;
    }
  }
}
"@

$targets = @(
    (Join-Path ([Environment]::GetFolderPath("Programs")) "$Name.lnk"),   # Menu Start: tu Windows szuka skrótu do przypięcia
    (Join-Path ([Environment]::GetFolderPath("Desktop")) "$Name.lnk")
)
foreach ($lnk in $targets) {
    [CupraShortcut.Lnk]::Create($lnk, $pythonw, "`"$script`"", $desktopDir, $icon,
                                "Cupra Terramar — Dziennik pokładowy", $AppId)
    "{0}  (AppUserModelID: {1})" -f $lnk, [CupraShortcut.Lnk]::ReadAppId($lnk)
}
