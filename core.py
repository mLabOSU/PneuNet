#!/usr/bin/python3
"""
    Author: Gabriel Kulp
    Created: 1/19/2017

    This module holds global variables and the functions most fundamental to this program.
"""

import time
from collections import namedtuple

# Make data structure used for each interval in the timeline
Interval = namedtuple("Interval", "start duration amplitude")

# Global setting for time granularity
STEPS_IN_TIMELINE = 10

# runs through one cycle of the timeline
def do_cycle(timeline, total_time):
    """
    Runs through one cycle of the gait.
        :param timeline: is the 2D array of intervals to read.
        :param total_time: is the time it should take to complete the cycle.
    """

    # set the index on each channel to 0
    curr_index = [0] * len(timeline)

    # run through timeline
    for curr_time in range(0, STEPS_IN_TIMELINE):
        # start row with time stamp
        print(curr_time, "\t", sep='', end='')

        amplitudes = []

        # find value of each channel
        for chan in range(0, len(timeline)):
            # return value and update channel's current index
            amp, curr_index[chan] = read_channel(timeline, chan, curr_index[chan], curr_time)
            amplitudes.append(amp)

        # set all values at once
        write_out(amplitudes)

        time.sleep(total_time/STEPS_IN_TIMELINE)


# return value on the selected channel given the time
def read_channel(timeline, channel_id, curr_index, curr_time):
    """
    Returns the current amplitude specified in the timeline.
        :param timeline: is the 2D array of intervals to read.
        :param channel_id: is the ID number of the pneumatic valve channel.
        :param curr_index: is the index in the timeline to start reading from.
        :param curr_time: is the time on the timeline to evaluate.
    """
    # while not past last interval
    while curr_index < len(timeline[channel_id]):

        # get interval to check
        curr_interval = timeline[channel_id][curr_index]

        # if we're past the starting point
        if curr_time >= curr_interval.start:
            # if currently in the interval's duration
            if curr_time - curr_interval.start < curr_interval.duration:

                # return the interval's amplitude and index (since it might have incremented)
                return (curr_interval.amplitude, curr_index)

            else: # not in duration

                # finished one interval; check next interval
                curr_index = curr_index + 1

                # start at the top of the while loop again,
                # but fetching a different interval to test
                continue
        else: # not past the starting point
            # between intervals
            return 0, curr_index

    # after last interval in timeline
    return 0, curr_index

# will eventually change PWM pin values
def write_out(value):
    """
    Prints stuff to the console and writes to Arduino/Pi pins if available.
        :param value: the stuff to print.
    """
    print(value, sep='')