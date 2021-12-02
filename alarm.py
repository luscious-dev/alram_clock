from datetime import datetime, time, timedelta
import csv
import pygame


class alarm:
    fmt = '%H:%M:%S'

    def __init__(self):
        pass

    def is_valid_time(self, time):
        """To validate time"""
        meridian = time[-2:].lower().strip()

        if meridian in ['am', 'pm']:
            hours, mins = time.strip(time[-2:]).split(':')

            if (int(hours) > 12) and (meridian == 'am'):
                return False
            elif((int(hours) >= 24) or int(mins) >= 60):
                return False
            else:
                return True

        if not meridian in ['am', 'pm']:
            hours, mins = time.split(':')
            if((int(hours) >= 24) or int(mins) >= 60):
                return False
            else:
                return True

    def string_to_time(self, time):
        """This formats strings from the users into date time"""
        hours = 0
        minutes = 0

        meridian = time[-2:].strip().lower()
        temp = time.strip(time[-2:])
        t_hours, t_minutes = temp.split(':')

        t_hours = int(t_hours)
        t_minutes = int(t_minutes)

        is_am = meridian == 'am'

        if (not is_am) and (t_hours < 12):
            t_hours += 12

        hours = t_hours
        minutes = t_minutes

        datetime_time = '{}:{}:00'.format(hours, minutes)
        return datetime.strptime(datetime_time, self.fmt).time()

    def hours_to_alarm(self, time):
        """This tells the user the time remaining for the next alarm to be triggered"""
        now = datetime.now()
        picked_time = self.string_to_time(time)
        now = datetime.now()
        hours = now.hour
        minutes = now.minute
        seconds = now.second
        current_time_str = '{}:{}:{}'.format(hours, minutes, seconds)
        current_time = datetime.strptime(current_time_str, self.fmt)

        time_diff = (picked_time - current_time) + timedelta(days=1)
        seconds = time_diff.seconds
        hours = seconds // 3600
        minutes = (seconds // 60) % 60
        text = '{0} hour{1}, {2} minutes to {3}'.format(
            hours, 's' if hours > 1 else '', minutes, time)
        return text

    def alarm_name_validation(self):
        alarm_names = []
        with open('./alarms.csv', 'r') as f:
            csv_reader = csv.reader(f)
            csv_reader.__next__()
            for line in csv_reader:
                alarm_names.append(line[0])

        alarm_name = input('Enter a name for the alarm: ')

        if alarm_name in alarm_names:
            alarm_name = input('Name already exists, Pick another: ')

        return alarm_name

    def set_time(self):
        # What is the name of the alarm
        alarm_name = self.alarm_name_validation()

        repeat = False
        is_repeat = input('Should the alarm repeat itself? [Y/N]')
        if is_repeat.lower() in ['y', 'yes']:
            repeat = True

        # What time should the alarm be triggered
        alarm_time = ''
        time = input('Enter a time for the alarm (HH:MM(pm/am)): ')
        if self.is_valid_time(time):
            alarm_time = time
        else:
            print('Not a valid time, Try again')
            self.set_time()

        # Trying to format the time before storing
        if len(alarm_time) <= 5 and not alarm_time[-2:].lower() in ['am', 'pm']:
            hours, minutes = alarm_time.split(':')
            if int(hours) >= 12 and int(minutes) >= 1:
                alarm_time += 'pm'
            else:
                alarm_time += 'am'

        with open('./alarms.csv', 'a+', newline='') as f:
            csv_writer = csv.writer(f, lineterminator='\n')
            csv_writer.writerow([alarm_name, alarm_time, repeat])

    def delete_alarm(self, alarm):
        alarm_names = []
        with open('./alarms.csv', 'r') as f:
            csv_reader = csv.reader(f)
            csv_reader.__next__()
            for line in csv_reader:
                alarm_names.append(line[0])
        if not alarm in alarm_names:
            print('No such alarm exists!')
        else:
            with open('./alarms.csv', 'r') as f:
                csv_reader = csv.reader(f)
                lines = []
                for line in csv_reader:
                    lines.append(line)
                lines = [line for line in lines if line[0] != alarm]
                with open('./alarms.csv', 'w') as f:
                    csv_writer = csv.writer(f, lineterminator='\n')
                    csv_writer.writerows(lines)
            print('Alarm deleted successfully')
            print()

    def display_alarms(self):
        with open('./alarms.csv', 'r') as f:
            csv_reader = csv.reader(f)
            fmt = '| {:<15s}|{:^10s}|{:^10s}|'
            print('-'*39)
            print(fmt.format('Alarm Name', 'Time', 'Repeat'))
            print('-'*39)
            csv_reader.__next__()
            for line in csv_reader:
                print(fmt.format(line[0], line[1], line[2]))
            print('-'*39)
            print()

    pygame.mixer.init()
    pygame.mixer.music.load('./blank_space.mp3')

    def play_song(self):
        pygame.mixer.music.play()
        pygame.time.wait(10000)
        pygame.mixer.music.stop()

    def preview_song(self):
        pygame.mixer.music.play(loops=0)
        # pygame.mixer.music.get_busy()

        pygame.time.wait(5000)
        stop = input('Stop preview? [Y]: ')
        print()
        try:
            if stop.lower() in ['Y', 'y']:
                pygame.mixer.music.stop()
            else:
                print('Alright!')
        except ValueError:
            print('Invalid response')
            pygame.mixer.music.stop()

    def check_alarm_status(self):
        alarms = []
        with open('./alarms.csv', 'r') as f:
            csv_reader = csv.DictReader(f)
            for line in csv_reader:
                alarms.append(line)
        while True:
            for alarm in alarms:
                current_day = datetime.now()
                current_time = datetime.strftime(current_day, '%H:%M:00')
                if current_time == self.string_to_time(alarm['time']):
                    print('fire')
                    self.play_song()
                    break

        # self.play_song()


def choice():
    print('What do you want to do?')
    options = ['Set an alarm', 'Delete an alarm',
               'View all alarms', 'Preview alarm song', 'Quit']

    for index, option in enumerate(options):
        print('{0}. {1}'.format(index+1, option))
    print()

    choice = 0

    while not choice in range(1, len(options)+1):
        try:
            choice = int(input('What\'s your pick? '))
        except ValueError:
            print('Invalid choice')
            continue

    return choice


fmt = '| {0:^32s}|'
print('-'*35)
print(fmt.format('Alarm Clock'))
print('-'*35)
print()


def main():
    # The meat of the program
    test_alarm = alarm()

    picked = choice()
    # print('Enter a time in the format (12:33PM)')
    if picked == 1:
        test_alarm.set_time()
        print()
        print('Alarm set successfully!!!')
        print()
        test_alarm.display_alarms()
    elif picked == 2:
        test_alarm.display_alarms()
        alarm_to_del = input(
            'What alarm do you want to delete. Specify name: ')
        test_alarm.delete_alarm(alarm_to_del)
        test_alarm.display_alarms()
    elif picked == 3:
        test_alarm.display_alarms()
    elif picked == 4:
        test_alarm.preview_song()
    else:
        print('Thank you')
        quit()


if __name__ == '__main__':
    while True:
        main()
        proceed = input('Continue? (Y/N)')
        if proceed.lower() == 'n':
            break
