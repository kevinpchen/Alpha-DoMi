import mido
import time

class MidiNote(object):
    start_timing = 0
    duration = 0
    end_timing = 0

    note = 0
    note_name = ''

    score = 0
    timing_interval = 0.3
    note_interval = 1

    time_score = 0

    def __init__(self, note=0, note_name='', start=0, duration=0, ):
        self.note = note
        self.note_name = note_name
        self.start_timing = start
        self.duration = duration
        self.end_timing = start + duration

    def duration_append(self, duration):
        self.duration += duration
        self.end_timing = self.start_timing + duration

    def compare(self, target_note, curr_timing):
        isMatch = 0
        if target_note == self.note:
            self.score = 1
        # if curr_timing < self.start_timing - self.timing_interval * 2 or curr_timing > self.start_timing + self.timing_interval * 2:
        #     return 0
        # if target_note < self.note - self.note_interval * 2 or target_note > self.note + self.note_interval * 2:
        #     return 0
        # newScore = self.note_interval * 3 - abs(target_note - self.note)
        # if newScore > self.score:
        #     self.score = newScore
        return self.score


    def in_time(self, target_time, target_end_time=None, thres=0.1):
        if target_end_time is not None:
            return   not(self.end_timing < target_time or self.start_timing > target_end_time)
        return self.start_timing - thres < target_time < self.end_timing + thres

    def __str__(self):
        return "note_name={}[note={}]\tstart_timing={}\tend_timing={}\t[score={}]".format(self.note_name, self.note,
                                                                                          round(self.start_timing, 3),
                                                                                          round(self.end_timing, 3),
                                                                                          self.score)


class IvyMidi(object):
    secPerTick = 0
    secPerBeat = 0
    tempo = 0
    tickPerBeat = 0
    curr_note = set()
    mid = None
    noteNames = []
    noteDicts = {}
    note_list = []

    curr_timing = 0
    start_timing = 0
    end_timeing = 0

    ivy_notes = []

    scores = {}
    score = 0

    def __init__(self):
        self.midi_labels()

    def __len__(self):
        return len(self.ivy_notes)

    def score_init(self):
        self.scores = {'all': 0, 'perfect': 0, 'good': 0, 'fail': 0}
        self.score = 0

    def midi_labels(self):

        note_name1 = ['C', 'C', 'D', 'D', 'E', 'F', 'F', 'G', 'G', 'A', 'A', 'B']
        note_name2 = ['', '#', '', '#', '', '', '#', '', '#', '', '#', '']
        note_name_level = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

        for n in range(21, 109):
            level = n // 12 - 1
            noteIndex = n % 12
            nn1 = note_name1[noteIndex]
            nnL = note_name_level[level]
            nn2 = note_name2[noteIndex]
            noteString = nn1 + nn2 + nnL
            self.noteNames.append(noteString)
            self.noteDicts[n] = noteString

        print(self.noteNames)
        print(self.noteDicts)

    def open(self, file_name='./music/canon.mid'):
        self.mid = mido.MidiFile(file_name)
        self.tickPerBeat = self.mid.ticks_per_beat

        for msg in self.mid.tracks[0]:
            if msg.type == 'set_tempo':
                self.tempo = msg.tempo
                break

        self.secPerTick = 1 * (self.tempo * 1e-6 / self.tickPerBeat)
        self.secPerBeat = self.secPerTick * self.tickPerBeat

        for i, track in enumerate(self.mid.tracks):
            print(track.name)

        print(self)

        t = 0
        c_notes = {}
        self.ivy_notes.clear()
        for i, track in enumerate(self.mid.tracks):
            if 'cello' in track.name.lower() or 'solo' in track.name.lower():
                print('Track {}: {} msg count: {}'.format(i, track.name,len(track)))
                for msg in track:
                    if msg.type == 'note_on':
                        # print(self.noteDicts[msg.note])
                        time_duration = msg.time * self.secPerTick
                        if msg.velocity > 0 and not c_notes.__contains__(msg.note):
                            c_notes[msg.note] = MidiNote(msg.note, self.noteDicts[msg.note], t, 0)
                            self.ivy_notes.append(c_notes[msg.note])
                        # 统计音符延长
                        for n in c_notes.values():
                            n.end_timing = n.end_timing+time_duration
                        # print(c_notes)
                        if msg.velocity == 0:
                            c_notes.pop(msg.note)
                        t += time_duration
                        if t > self.end_timeing:
                            self.end_timeing = t
                    if msg.type == 'note_off':
                        pass
                        # self.mid.curr_note.remove(msg.note)
            print('ivy_notes length---------', len(self.ivy_notes))
            for n in self.ivy_notes:
                print(n)

    def compare(self, note):
        self.score = 0
        for n in self.note_list:
            n.compare(note, time.time() - self.start_timing)
            self.score += n.score

    def get_curr_notes(self, target_time):
        res = []
        for n in self.ivy_notes:
            if n.in_time(target_time):
                res.append(n)
        return res

    def get_nearby_notes(self,target_time,secs=5):
        res = []
        for n in self.ivy_notes:
            if n.in_time(target_time, target_time+secs):
                res.append(n)
        return res

    def __str__(self):
        return "{}[{}] {}-{}".format(self.tempo, self.secPerTick, self.secPerBeat, self.note_list)


if __name__ == '__main__':
    mid = IvyMidi()
    #mid.open()
    print(mid)
    # for n in mid.ivy_notes:
    #     print(n)

    # for i, track in enumerate(mid.mid.tracks):
    #     print(track.name)
    #
    # for i, track in enumerate(mid.mid.tracks):
    #     if 'cello' in track.name.lower():
    #         print('Track {}: {}'.format(i, track.name))
    #         for msg in track:
    #             print(msg)
    #             #            print(msg.type)
    #             if msg.type == 'note_on':
    #                 #                print('----note=',msg.note)
    #                 #                print('----velocity=',msg.velocity)
    #                 print(mid.noteDicts[msg.note])
    #
    #                 if msg.velocity > 0:
    #                     mid.curr_note.add(msg.note)
    #                 elif msg.velocity == 0:
    #                     mid.curr_note.remove(msg.note)
    #             #            if len(curr_note)>0:
    #             #                print('{',curr_note,'}')
    #             if msg.type == 'note_off':
    #                 mid.curr_note.remove(msg.note)
