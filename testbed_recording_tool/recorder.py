import posixpath
import shlex
import time
from pathlib import Path

import paramiko

from .chirp import get_wav_sample_rate, prepare_output_folder
from .config import config


RECORD_DEVICE = "dmic_sv_shared"
CHANNELS = 1
SAMPLE_FORMAT = "S32_LE"
RECORD_WARMUP_SECONDS = 0.2
POST_PLAYBACK_PADDING_SECONDS = 0.2

ssh: paramiko.SSHClient = None


def is_ssh_connected():
    global ssh
    return ssh is not None and ssh.get_transport() and ssh.get_transport().is_active()


def ssh_connect(hostname, port, username, password):
    global ssh
    try:
        ssh = paramiko.SSHClient()
        print(config["connection"])
        print("Connecting to RaspberryPi...")
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, int(port), username, password, timeout=10)

        if not ssh.get_transport() or not ssh.get_transport().is_active():
            ssh = None
            raise RuntimeError("SSH transport is not active")

        print("CONNECTED TO RASPBERRYPI")
    except Exception:
        ssh = None
        raise


def close_ssh():
    global ssh
    if ssh is not None:
        ssh.close()
    ssh = None


def record_with_config(data_folder, output_filename):
    connection = config["connection"]
    remote_dir = config["remote_dir"]

    if not is_ssh_connected():
        ssh_connect(*connection)
        time.sleep(1)

    try:
        return record_test(data_folder, output_filename, remote_dir)
    finally:
        close_ssh()


def record_test(data_folder, output_filename, remote_dir):
    data_path = Path(data_folder)
    local_chirp = prepare_output_folder(data_path)
    sample_rate = get_wav_sample_rate(local_chirp)

    if not output_filename.lower().endswith(".wav"):
        output_filename = f"{output_filename}.wav"

    audio_path = data_path / "audio"
    local_recording = audio_path / output_filename

    remote_base = posixpath.join(remote_dir, data_path.name)
    remote_reference_dir = posixpath.join(remote_base, "reference")
    remote_audio_dir = posixpath.join(remote_base, "audio")
    remote_chirp = posixpath.join(remote_reference_dir, local_chirp.name)
    remote_recording = posixpath.join(remote_audio_dir, output_filename)

    ensure_remote_directories(remote_reference_dir, remote_audio_dir)
    upload_file(local_chirp, remote_chirp)
    start_recording_and_play_chirp(remote_chirp, remote_recording, sample_rate)
    download_file(remote_recording, local_recording)

    return local_recording


def ensure_remote_directories(*paths):
    command = "mkdir -p " + " ".join(shlex.quote(path) for path in paths)
    exec_remote(command)


def upload_file(local_path, remote_path):
    with ssh.open_sftp() as sftp:
        sftp.put(str(local_path), remote_path)


def download_file(remote_path, local_path):
    with ssh.open_sftp() as sftp:
        sftp.get(remote_path, str(local_path))


def start_recording_and_play_chirp(remote_chirp, remote_recording, sample_rate):
    arecord_parts = [
        "arecord", "-D", RECORD_DEVICE, "-c", str(CHANNELS), "-r", str(sample_rate),
        "-f", SAMPLE_FORMAT, "-t", "wav", "-v", remote_recording,
    ]
    aplay_parts = [
        "aplay", remote_chirp,
    ]
    arecord_command = " ".join(shlex.quote(part) for part in arecord_parts)
    aplay_command = " ".join(shlex.quote(part) for part in aplay_parts)
    exec_remote(f"rm -f {shlex.quote(remote_recording)}")

    record_pid = exec_remote(f"{arecord_command} >/tmp/testbed_arecord.log 2>&1 & echo $!")
    time.sleep(RECORD_WARMUP_SECONDS)
    exec_remote(f"{aplay_command} >/tmp/testbed_aplay.log 2>&1")
    time.sleep(POST_PLAYBACK_PADDING_SECONDS)
    exec_remote(f"kill -INT {record_pid}")
    time.sleep(0.5)


def exec_remote(command):
    if not is_ssh_connected():
        raise RuntimeError("SSH is not connected")

    stdin, stdout, stderr = ssh.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()
    stdout_text = stdout.read().decode("utf-8", errors="replace").strip()
    stderr_text = stderr.read().decode("utf-8", errors="replace").strip()

    if exit_status != 0:
        details = "\n".join(part for part in (stdout_text, stderr_text) if part)
        raise RuntimeError(f"Remote command failed ({exit_status}): {command}\n{details}")

    return stdout_text
