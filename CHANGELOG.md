# Changelog

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).


## [1.0.0] - 2026-05-14
### Added
- Added CLI recording flow for Raspberry Pi testbed acquisition.
- Added JSON configuration with `connection` and `remote_dir`.
- Added transfer of the single chirp wavfile from `<data-folder>/reference` to Raspberry Pi.
- Added download of recorded wavfiles to `<data-folder>/audio`.
- Added timestamp suffix to recorded output filenames.
- Added start recording and playing chirp on RPI