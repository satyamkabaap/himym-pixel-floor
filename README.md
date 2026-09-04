# himym-pixel-floor

A multi-agent harness that runs the HIMYM gang as your autonomous studio — real deliverables, pixel-art floor, zero telemetry.

## Features

- **Multi-agent simulation**: Ted, Barney, Marshall, Lily, and Robin as autonomous agents.
- **Pixel-art floor**: Dynamic day/night cycle with pixel-art aesthetics.
- **Integrated engines**: Automation Engine (v3) and Episode Engine (v4) unified.
- **Friendship system**: Agents review each other's work and build friendships.
- **Episode-triggered work**: Episodes spawn follow-up tasks.
- **Shared achievements and collaboration graph**.
- **Zero telemetry**: Everything runs locally, no data leaves your machine.
- **Installer-ready**: Includes Inno Setup script for one-click Windows installation.

## Quick Start

1. Download the latest release from the [Releases page](https://github.com/YOURNAME/himym-pixel-floor/releases).
2. Run the installer (`himym-harness-installer.exe`).
3. Launch the application from the Start menu or desktop shortcut.
4. Watch the agents collaborate in real-time via the dashboard at `http://localhost:8000/dashboard.html`.

## Configuration

To enable the local LLM (FreeLLMAPI on port 3001), create a file `himym_data/llm_key.txt` containing your API key.
The app will automatically pick it up. If the file is missing, the agents will use built-in quips for dialogue.

## Building from Source

### Prerequisites

- Python 3.8+
- [Inno Setup](https://jrsoftware.org/isinfo.php) (for building the installer)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/YOURNAME/himym-pixel-floor.git
   cd himym-pixel-floor
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the simulation:
   ```bash
   python director.py
   ```
4. Open the dashboard:
   ```
   http://localhost:8000/dashboard.html
   ```

### Building the Installer

Run the provided batch script:
```bash
build_installer.bat
```
This will produce `himym-harness-installer.exe` in the `installer_output/` directory.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the television show *How I Met Your Mother*.
- Pixel art floor by [LimeZu](https://limezu.com/) (adapted).
- Special thanks to the open-source community.
