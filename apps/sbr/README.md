# SBR (Self-Balancing Robot)

Contain code to manage a self-balancing robot.

## Layout

This directory contains the main application (main.cc).
It can instantiate `/hw_services/` and defines the `system/` that is utilized
when constructing the application.

## Usage

### Run as Host Simulator

```
bazel run //apps/sbr:simulator_sbr

# Separate window

bazel run //apps/sbr:simulator_console
```

### Run on device

```
# Flash
bazel run //apps/sbr:flash_rp2040

# Console
bazel run //apps/sbr:rp2040_console
```
