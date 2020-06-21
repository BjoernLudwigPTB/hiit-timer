# Interval timer

A little script that I use to time my interval workouts. Based on the work of
Adam J. Forster in the upstream repository
[github.com/adamjforster/hiit-timer](https://github.com/adamjforster/hiit-timer).

Requires Python 3.6+.

## Usage help

usage: interval-timer.py [-h] [-w WAIT] [-n [NAMES [NAMES ...]]] [-r [REPS [REPS ...]]] [-d [DELAYS [DELAYS ...]]] exercises [exercises ...]

A timer for interval training.

positional arguments:

- exercises:
  Space separated list of durations for exercises.

optional arguments:

- -h, --help:
  show this help message and exit
- -w WAIT, --wait WAIT:
  Seconds before first and in between exercises.
- -n, --names [NAMES [NAMES ...]]:
  Space separated list of Names for the exercises.
- -r, --reps [REPS [REPS ...]]:
  Single number of repetitions to be used for all exercises or space separated list of
  repetitions to be used for the according exercises.
- -d, --delays [DELAYS [DELAYS ...]]:
  Single delay to be used for breaks in between repetitions or space separated list of
  delays each to be used for the according exercises.

## Example usage

    ./interval-timer.py 6 12 6 --names crunch T dip
