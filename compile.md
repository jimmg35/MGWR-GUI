# MGWR-GUI Build & Installer Guide

This guide shows how to regenerate the standalone executable with PyInstaller and wrap it in an NSIS installer on Windows.

## 1. Prerequisites
- Windows 10/11 with PowerShell.
- [Anaconda](https://www.anaconda.com/) installed (the project expects it).
- NSIS installed at the default path `C:\Program Files (x86)\NSIS`.

## 2. Prepare the Conda Environment
From the project root (`c:\Users\jim60\workspace\.sdsc\.fork\MGWR-GUI`):

```powershell
conda env create -f environment.yml
```

> Already have the environment? Update it instead:
>
> ```powershell
> conda env update -f environment.yml --prune
> ```

## 3. Activate the Build Environment
```powershell
conda activate mgwr-gui-compile-py310
```

If you use a different env name, substitute it here and in later commands.

## 4. Clean Previous Builds (optional but recommended)
```powershell
Remove-Item build,dist -Recurse -Force -ErrorAction SilentlyContinue
```

## 5. Build the PyInstaller Bundle
```powershell
& "C:\Users\jim60\anaconda3\envs\mgwr-gui-compile-py310\python.exe" -m PyInstaller --clean --noconfirm build.spec
```

Key outputs:
- `dist\MGWR-GUI\MGWR-GUI.exe` ? the GUI launcher.
- `dist\MGWR-GUI\_internal\` ? packaged resources and libraries.
- `build\` ? PyInstaller intermediates (safe to delete after packaging).

## 6. (Optional) Test the Executable
Run the executable directly to verify the splash screen, icons, and main workflows before creating the installer.

```powershell
& "dist\MGWR-GUI\MGWR-GUI.exe"
```

## 7. Build the NSIS Installer
```powershell
& "C:\Program Files (x86)\NSIS\makensis.exe" installer.nsi
```

The installer is emitted to `dist\MGWR-GUI-Setup.exe`.

## 8. Validate the Installer
1. Launch `dist\MGWR-GUI-Setup.exe` on a test machine.
2. Confirm the program files install under `C:\Program Files\MGWR-GUI` (default).
3. Ensure desktop and Start Menu shortcuts carry the custom icon and launch the app.
4. Run the uninstaller from ?Apps & features? or the Start Menu to verify cleanup.

## 9. Export Environment Updates (optional)
If you add packages to the build env, refresh `environment.yml` for version control:

```powershell
conda env export > environment.yml
```

---
Need to tweak the bundle (new assets, spec changes, etc.)? Repeat steps 5?8 after editing.
