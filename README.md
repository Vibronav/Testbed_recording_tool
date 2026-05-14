# Testbed_recording_tool

Tool for recording wavfiles of the testbed

# Installation

1. Create folder for tool and enter it
2. open commandline in this folder, then type command to create environment:
```commandline
python -m venv .tsb
```
3. Enter environment

On windows:
Can be required:
```commandline
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```
Then:
```commandline
.tsb/Scripts/Activate.ps1
```

On linux:
```commandline
source .tsb/bin/activate
```

4. Then for both operating systems to install tool:

```commandline
python -m pip install https://github.com/Vibronav/Testbed_recording_tool/archive/master.zip
```

Or if you want specific version:

```commandline
python -m pip install https://github.com/Vibronav/Testbed_recording_tool/archive/refs/tags/<version>.zip
```

# Configuration

Create `config.json`:

```json
{
  "connection": [
    "hostname",
    "port_number",
    "username",
    "password"
  ],
  "remote_dir": "path_to_data_on_remote_system"
}
```

# Usage

Create test folder manually inside folder with tool installed:

```text
test1/
  reference/
    chirp.wav
```

The chirp can have any `.wav` filename, but it must be the only file in `reference`.

Run recording:

```commandline
testbed-recording-tool --config config.json --data-folder test1 --output-filename dobot_mg400_black_needle_40-20khz_05.wav
```

The tool uploads the chirp from `test1/reference` to Raspberry Pi, starts:

```commandline
arecord -D dmic_sv -c2 -r 44100 -f S32_LE -t wav -V stereo -v <output.wav>
```

then plays the chirp with:

```commandline
aplay <chirp.wav>
```

After playback finishes, the recording is stopped and downloaded to:

```text
test1/audio/<output.wav>
```
