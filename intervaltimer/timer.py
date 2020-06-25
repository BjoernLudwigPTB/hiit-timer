#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import argparse
import sys
import wave
from pathlib import PurePath
from time import localtime, sleep, strftime, time
from typing import Dict

import simpleaudio as sa
from simpleaudio import WaveObject


class Timer:
    @staticmethod
    def _add_arguments():
        # Execute the time with provided command line parameters.
        parser = argparse.ArgumentParser(description="A timer for interval training.")
        parser.add_argument(
            "-w",
            "--wait",
            default=10,
            type=int,
            help="Seconds before first and in between exercises.",
        )
        parser.add_argument(
            "exercises",
            nargs="+",
            type=int,
            help="Space separated list of durations for exercises.",
        )
        parser.add_argument(
            "-n",
            "--names",
            nargs="*",
            help="Space separated list of Names for the exercises.",
        )
        parser.add_argument(
            "-r",
            "--reps",
            nargs="*",
            default=6,
            type=int,
            help="Single number of repetitions to be used for all exercises or space "
            "separated list of repetitions to be used for the according exercises.",
        )
        parser.add_argument(
            "-d",
            "--delays",
            nargs="*",
            type=int,
            help="Single delay to be used for breaks in between repetitions or space "
            "separated list of delays each to be used for the according exercises.",
        )
        return parser.parse_args()

    def __init__(self):
        # Set audio files' path.
        audio_files_paths = {
            "beep": ".//intervaltimer//audio//clock.wav",
            "ignition": ".//intervaltimer//audio//rocket.wav",
            "running": ".//intervaltimer//audio//human-heartbeat-daniel_simon.wav",
            "end": ".//intervaltimer//audio//boxing_bell.wav",
            "finish": ".//intervaltimer//audio//applause2_x.wav",
        }

        self.audio_files: Dict[str, WaveObject] = {}
        # Prepare the audio files.
        for purpose, path in audio_files_paths.items():
            self.audio_files[purpose] = self._prepare_audio(path)

        self.args = self._add_arguments()

        exercises = self._prepare_args()

        duration = 0
        for exercise in exercises:
            duration += (
                self.args.wait
                + exercise["reps"] * (exercise["duration"] + exercise["delay"])
                - exercise["delay"]
            )

        # Perform the actual training.
        print(f"The exercise will take approximately {duration} seconds.")

        # Start the timer
        begin_time = time()

        for exercise in exercises:
            print(f"{exercise['name']} starts in...")
            self.verbose_countdown(self.args.wait)
            for rep_minus_one in range(exercise["reps"]):
                repetition = rep_minus_one + 1
                self.audio_files["ignition"].play()
                start_audio = self.audio_files["running"].play()
                print(f"{repetition}. {exercise['name']} for...")
                self.verbose_countdown(exercise["duration"])
                start_audio.stop()
                end_audio = self.audio_files["end"].play()
                if repetition < exercise["reps"]:
                    print("Relax for...")
                    self.verbose_countdown(exercise["delay"])

        finish_audio = self.audio_files["finish"].play()

        print(
            f"Set completed in {strftime('%S', localtime(time() - begin_time))} seconds."
        )
        while finish_audio.is_playing():
            pass
        sys.exit(0)

    def _prepare_args(self):
        # Check if number of names and exercises match in case we provided names.
        try:
            if len(self.args.names) != len(self.args.exercises):
                raise ValueError(
                    f"Number of names for exercises is expected to match "
                    f"number of exercises but {len(self.args.exercises)} exercises "
                    f"and {len(self.args.names)} names were given."
                )
            else:
                exercises = [
                    {"name": name, "duration": duration}
                    for name, duration in zip(self.args.names, self.args.exercises)
                ]
        except TypeError:
            # We specified no name, so we just count the exercises.
            exercises = [
                {"name": f"Exercise {index}", "duration": duration}
                for index, duration in enumerate(self.args.exercises)
            ]
        # Check if number of delays and exercises match in case we provided delays or
        # use
        # the one specified delay for all exercises.
        try:
            if len(self.args.delays) != len(self.args.exercises):
                if len(self.args.delays) != 1:
                    # We provided an unequal number of delays compared to the number of
                    # exercises and not only one, which can be used for all exercises.
                    raise ValueError(
                        f"Number of delays for exercises ist expected to match "
                        f"number of exercises or to be just one to be used for all "
                        f"exercises but we have {len(self.args.exercises)} exercises "
                        f"and {len(self.args.delays)} delays."
                    )
                else:
                    for exercise in exercises:
                        exercise["delay"] = self.args.delays[0]
            else:
                # So we have an equal number of delays and exercises.
                for exercise, delay in zip(exercises, self.args.delays):
                    exercise["delay"] = delay
        except TypeError:
            for exercise in exercises:
                exercise["delay"] = exercise["duration"]
        # Check if number of repetitions and exercises match in case we provided
        # repetitions or use the one specified number of repetitions for all exercises.
        try:
            if len(self.args.reps) != len(self.args.exercises):
                if len(self.args.reps) != 1:
                    # We provided an unequal number of delays compared to the number of
                    # exercises and not only one, which can be used for all exercises.
                    raise ValueError(
                        f"Number of repetitions for exercises ist expected to match "
                        f"number of exercises or to be just one to be used for all "
                        f"exercises but we have {len(self.args.exercises)} exercises "
                        f"and {len(self.args.reps)} repetitions."
                    )
                else:
                    for exercise in exercises:
                        exercise["reps"] = self.args.reps[0]
            else:
                # So we have an equal number of repetitions and exercises.
                for exercise, reps in zip(exercises, self.args.reps):
                    exercise["reps"] = reps
        except TypeError:
            # So we have no number of repetitions specified.
            for exercise in exercises:
                exercise["reps"] = self.args.reps
        return exercises

    @staticmethod
    def _prepare_audio(path_to_file: str) -> WaveObject:
        """Prepare an audio file from a specific path to be played by simpleaudio

        Parameters
        ----------
        path_to_file : str
            path to the file relative to the working directory or absolute
        Returns
        -------
        WaveObject
            the audio file to be played by simpleaudio's WaveObject's `play()`
        """
        wave_read = wave.open(str(PurePath(path_to_file)), "rb",)
        audio_data = wave_read.readframes(wave_read.getnframes())
        num_channels = wave_read.getnchannels()
        bytes_per_sample = wave_read.getsampwidth()
        sample_rate = wave_read.getframerate()
        return sa.WaveObject(audio_data, num_channels, bytes_per_sample, sample_rate)

    def verbose_countdown(self, duration: int):
        # Print indented the remaining time of a countdown every second.

        for wait_for in range(duration, 0, -1):
            print(f"    {wait_for}")
            if wait_for < 4:
                self.audio_files["beep"].play()
            sleep(1)


if __name__ == "__main__":
    Timer()
