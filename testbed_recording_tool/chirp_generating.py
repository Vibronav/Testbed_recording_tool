import argparse
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import chirp


STEP_EDGE_FADE_SAMPLES = 2048


def generate_log_chirp(duration, start_freq, end_freq, sample_rate):
    t = np.linspace(0, duration, int(duration * sample_rate), endpoint=False)
    return chirp(t, f0=start_freq, f1=end_freq, t1=duration, method="logarithmic")


def generate_step_wise_faded_chirp(steps, duration, start_freq, end_freq, sample_rate):
    frequencies = np.linspace(start_freq, end_freq, steps)
    step_duration = duration / steps
    step_samples = int(step_duration * sample_rate)
    t = np.arange(step_samples) / sample_rate
    fade_samples = min(STEP_EDGE_FADE_SAMPLES, step_samples // 2)

    signal_steps = []
    for frequency in frequencies:
        step_signal = np.sin(2 * np.pi * frequency * t)
        if fade_samples > 0:
            fade = np.linspace(0, 1, fade_samples)
            step_signal[:fade_samples] *= fade
            step_signal[-fade_samples:] *= fade[::-1]
        signal_steps.append(step_signal)

    return np.concatenate(signal_steps)


def generate_step_wise_chirp(steps, duration, start_freq, end_freq, sample_rate):
    frequencies = np.linspace(start_freq, end_freq, steps)
    step_duration = duration / steps
    step_samples = int(step_duration * sample_rate)
    t = np.arange(step_samples) / sample_rate

    signal_steps = []
    for frequency in frequencies:
        step_signal = np.sin(2 * np.pi * frequency * t)
        signal_steps.append(step_signal)

    return np.concatenate(signal_steps)


def default_output_filename(args):
    start_freq = format_frequency(args.start_freq)
    end_freq = format_frequency(args.end_freq)
    if args.mode == "log":
        return f"log_chirp_{start_freq}-{end_freq}_fs{args.sample_rate}_dur{args.duration}s.wav"
    elif args.mode == "step-wise-faded":
        return (
            f"step_wise_faded_chirp_{start_freq}-{end_freq}_fs{args.sample_rate}_"
            f"steps{args.steps}_dur{args.duration}s.wav"
        )
    return (
        f"step_wise_chirp_{start_freq}-{end_freq}_fs{args.sample_rate}_steps{args.steps}_dur{args.duration}s.wav"
    )


def format_frequency(frequency):
    return f"{frequency:g}Hz"


def validate_args(args):
    if args.start_freq <= 0 or args.end_freq <= 0:
        raise ValueError("Frequencies must be greater than zero")
    if args.sample_rate <= 0:
        raise ValueError("Sample rate must be greater than zero")
    if args.end_freq > args.sample_rate / 2:
        raise ValueError("End frequency cannot be greater than Nyquist frequency")
    if not 0 < args.amplitude <= 1:
        raise ValueError("Amplitude must be in range (0, 1]")
    if args.duration <= 0:
        raise ValueError("Duration must be greater than zero")
    if args.mode in ("step-wise", "step-wise-faded") and args.steps <= 0:
        raise ValueError("Steps must be greater than zero")

def parse_args():
    parser = argparse.ArgumentParser(description="Generate chirp wavfiles")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["log", "step-wise", "step-wise-faded"],
        help="Chirp generation mode (available: log, step-wise, step-wise-faded)",
    )
    parser.add_argument("--start-freq", type=float, required=True, help="Start frequency in Hz")
    parser.add_argument("--end-freq", type=float, required=True, help="End frequency in Hz")
    parser.add_argument("--sample-rate", type=int, default=48000, help="Sample rate in Hz")
    parser.add_argument("--duration", type=float, default=1.0, help="Chirp duration in seconds")
    parser.add_argument("--steps", type=int, default=10, help="Number of frequency steps for step-wise mode")
    parser.add_argument("--amplitude", type=float, default=0.8, help="Signal amplitude in range 0-1")
    parser.add_argument("--output-filename", help="Output wav filename")
    return parser.parse_args()


def main():
    args = parse_args()
    validate_args(args)

    if args.mode == "log":
        signal = generate_log_chirp(args.duration, args.start_freq, args.end_freq, args.sample_rate)
    elif args.mode == "step-wise-faded":
        signal = generate_step_wise_faded_chirp(
            args.steps,
            args.duration,
            args.start_freq,
            args.end_freq,
            args.sample_rate,
        )
    else:
        signal = generate_step_wise_chirp(
            args.steps,
            args.duration,
            args.start_freq,
            args.end_freq,
            args.sample_rate,
        )

    signal = (signal * args.amplitude).astype(np.float32)
    output_path = Path(args.output_filename or default_output_filename(args))
    wavfile.write(output_path, args.sample_rate, signal)
    print(f"Saved chirp to: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
