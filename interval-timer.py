#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import sys

from time import localtime, sleep, strftime, time


def main():
    # Execute the time with provided command line parameters.
    parser = argparse.ArgumentParser(description="A timer for interval training.")
    parser.add_argument(
        "-w",
        "--wait",
        default=10,
        type=int,
        help="Seconds before first and in between exercise.",
    )
    parser.add_argument(
        "-e",
        "--exercises",
        dest="exercises",
        nargs="+",
        type=int,
        help="Duration of exercises.",
    )
    parser.add_argument(
        "-n", "--names", nargs="*", help="Names for the exercises to be performed."
    )
    parser.add_argument(
        "-r",
        "--reps",
        nargs="*",
        default=6,
        type=int,
        help="Number of repetitions for exercises.",
    )
    parser.add_argument(
        "-d",
        "--delays",
        nargs="*",
        type=int,
        help="Delay or delays between exercises.",
    )
    args = parser.parse_args()

    # Check if number of names and exercises match in case we provided names.
    try:
        if len(args.names) != len(args.exercises):
            raise ValueError(
                f"Number of names for exercises is expected to match "
                f"number of exercises but {len(args.exercises)} exercises "
                f"and {len(args.names)} names were given."
            )
        else:
            exercises = [
                {"name": name, "duration": duration}
                for name, duration in zip(args.names, args.exercises)
            ]
    except TypeError:
        # We specified no name, so we just count the exercises.
        exercises = [
            {"name": f"Exercise {index}", "duration": duration}
            for index, duration in enumerate(args.exercises)
        ]

    # Check if number of delays and exercises match in case we provided delays or use
    # the one specified delay for all exercises.
    try:
        if len(args.delays) != len(args.exercises):
            if len(args.delays) != 1:
                # We provided an unequal number of delays compared to the number of
                # exercises and not only one, which can be used for all exercises.
                raise ValueError(
                    f"Number of delays for exercises ist expected to match "
                    f"number of exercises or to be just one to be used for all "
                    f"exercises but we have {len(args.exercises)} exercises "
                    f"and {len(args.delays)} delays."
                )
            else:
                for exercise in exercises:
                    exercise["delay"] = args.delays[0]
        else:
            # So we have an equal number of delays and exercises.
            for exercise, delay in zip(exercises, args.delays):
                exercise["delay"] = delay
    except TypeError:
        for exercise in exercises:
            exercise["delay"] = exercise["duration"]

    # Check if number of repetitions and exercises match in case we provided
    # repetitions or use the one specified number of repetitions for all exercises.
    try:
        if len(args.reps) != len(args.exercises):
            if len(args.reps) != 1:
                # We provided an unequal number of delays compared to the number of
                # exercises and not only one, which can be used for all exercises.
                raise ValueError(
                    f"Number of repetitions for exercises ist expected to match "
                    f"number of exercises or to be just one to be used for all "
                    f"exercises but we have {len(args.exercises)} exercises "
                    f"and {len(args.reps)} repetitions."
                )
            else:
                for exercise in exercises:
                    exercise["reps"] = args.reps[0]
        else:
            # So we have an equal number of repetitions and exercises.
            for exercise, reps in zip(exercises, args.reps):
                exercise["reps"] = reps
    except TypeError:
        # So we have no number of repetitions specified.
        for exercise in exercises:
            exercise["reps"] = args.reps

    begin_time = time()

    for exercise in exercises:
        print(f"{exercise['name']} starts in...")
        verbose_countdown(args.wait)
        for rep_minus_one in range(exercise["reps"]):
            repetition = rep_minus_one + 1
            print(f"{repetition}. {exercise['name']} for...")
            verbose_countdown(exercise["duration"])
            if repetition < exercise["reps"]:
                print("Relax for...")
                verbose_countdown(exercise["delay"])

    print(f"Set completed in {strftime('%S', localtime(time() - begin_time))} seconds.")
    sys.exit(0)


def verbose_countdown(duration: int):
    # Print indented the remaining time of a countdown every second.
    for wait_for in range(duration, 0, -1):
        print(f"    {wait_for}")
        sleep(1)


if __name__ == "__main__":
    main()
