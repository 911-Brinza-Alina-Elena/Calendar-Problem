def find_free_time(schedule, time_range):
    """
    Given a booked calendar of a person and the time range in which that person can have meetings, we find all the time
    intervals in which they are available.
    :param schedule: booked calendar of the person
    :param time_range: time range for meetings
    :return: a list of free time intervals
    """
    # zfill is used to make sure that the time strings have the same format, hh:mm
    day_start = time_range[0]
    day_end = time_range[1]
    free_time_slots = []
    current_time = day_start
    # sorting by the starting booked time, we make sure that the array is ordered chronologically
    schedule.sort(key=lambda x: x[0].zfill(5))
    # we go through all the time intervals that are booked and if the current time is earlier than the starting booked
    # time, we add to the free time intervals the period between the current time and starting booked time
    for booked_time in schedule:
        if current_time.zfill(5) < booked_time[0].zfill(5):
            free_time_slots.append((current_time, booked_time[0]))
        # we update the current time to be the end of the booked time
        current_time = booked_time[1].zfill(5)
    # since we know that the list is ordered chronologically, there's a possibility to have another free interval
    # between the end of the last booked interval and the end of the range for meetings
    last_booked = schedule[-1]
    if last_booked[1].zfill(5) < day_end.zfill(5):
        free_time_slots.append((last_booked[1], day_end))
    free_time_slots.sort(key=lambda x: x[0].zfill(5))
    return free_time_slots


def check_duration(time_interval, duration):
    """
    Compute the duration of a time interval and compare it with the meeting duration
    :param time_interval: possible time interval
    :param duration: meeting duration
    :return: True if the duration of the time interval is greater or equal than the meeting duration, false otherwise
    """
    # we assume that the strings for time have a correct format, which means hh:mm or h:mm
    [hour1, minute1] = time_interval[0].split(":")
    [hour2, minute2] = time_interval[1].split(":")
    # we compute the total time in minutes
    total = (int(hour2) - int(hour1)) * 60 + (int(minute2) - int(minute1))
    if total >= duration:
        return True
    else:
        return False


def find_meeting_possibilities(free_time1, free_time2, duration):
    """
    Compute the intersection between the free time intervals of the two calendars
    :param free_time1: free times for the first person
    :param free_time2: free times for the second person
    :param duration: time duration for a meeting
    :return:
    """
    meetings = []
    for possibility1 in free_time1:
        for possibility2 in free_time2:
            # we only try to compute a possible meeting interval if an intersection is possible between them
            # we have an intersection if end2 >= start1 and end1 >= start2
            if possibility2[1].zfill(5) >= possibility1[0].zfill(5) and possibility1[1].zfill(5) >= possibility2[0].zfill(5):
                # the start of the interval is the maximum between the starts of the two free intervals
                if possibility1[0].zfill(5) > possibility2[0].zfill(5):
                    start = possibility1[0]
                else:
                    start = possibility2[0]

                # the end of the interval is the minimum between the ends of the two free intervals
                if possibility1[1].zfill(5) < possibility2[1].zfill(5):
                    end = possibility1[1]
                else:
                    end = possibility2[1]
                meetings.append((start, end))
    # filter the meetings by their total duration, which should be greater or equal than the given duration
    meetings = list(filter(lambda x: check_duration(x, duration), meetings))
    return meetings


def main():
    booked_calendar1 = [("9:00", "10:30"), ("12:00", "13:00"), ("16:00", "18:00")]
    range_person1 = ("9:00", "20:00")

    booked_calendar2 = [("10:00", "11:30"), ("12:30", "14:30"), ("14:30", "15:00"), ("16:00", "17:00")]
    range_person2 = ("10:00", "18:30")

    duration = 30
    free_time_person1 = find_free_time(booked_calendar1, range_person1)
    free_time_person2 = find_free_time(booked_calendar2, range_person2)

    meetings = find_meeting_possibilities(free_time_person1, free_time_person2, duration)
    print("Possible meeting intervals: {}".format(meetings))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
