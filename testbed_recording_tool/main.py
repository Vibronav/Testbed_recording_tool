import argparse
from datetime import datetime

from .config import config
from .recorder import record_with_config


def parse_args():
    parser = argparse.ArgumentParser(description="Tool for testbed recording via Raspberry Pi")
    parser.add_argument(
        "--config",
        required=True,
        help="Path to json config file",
    )
    parser.add_argument(
        "--data-folder",
        required=True,
        help="Folder containing reference/*.wav and receiving audio/*.wav",
    )
    parser.add_argument(
        "--output-filename",
        required=True,
        help="Filename for recorded wavfile. Defaults to recording_<timestamp>.wav",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    output_filename = _timestamped_output_filename(args.output_filename)

    config.load_from_json(args.config)
    recording_path = record_with_config(args.data_folder, output_filename)
    print(f"Recorded wavfile: {recording_path}")
    return 0


def _timestamped_output_filename(output_filename):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if output_filename.lower().endswith(".wav"):
        return f"{output_filename[:-4]}_{timestamp}.wav"
    return f"{output_filename}_{timestamp}.wav"


if __name__ == "__main__":
    raise SystemExit(main())
