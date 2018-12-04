import re
import parallel_sent_to_m2 as ps2m2

no_change_indicator = "A -1 -1|||noop|||-NONE-|||REQUIRED|||-NONE-|||"

def m2actions_to_sentence(src, m2actions):  # for single reference
    new_tokens = []
    last_pointer = 0
    orig_tokens = src.split()
    if len(m2actions) == 0:
        return src
    for action in m2actions:
        l = action
        if l.startswith(no_change_indicator):
            return src
        attr = l.split('|||')
        # err_type = attr[1]
        # if err_type in bad_type:
        #     continue
        correct_content = attr[2]
        offset = attr[0].split()[1:]
        if int(offset[0]) > last_pointer:
            new_tokens += orig_tokens[last_pointer:int(offset[0])]
        new_tokens += [correct_content]
        last_pointer = int(offset[1])
    if last_pointer < len(src):
        new_tokens += orig_tokens[last_pointer:len(src)]
        # if True == False and (len(new_tokens) < 3 or new_tokens[-1] not in eos_char_set or 'http' in new_tokens):
        #     orig_sent = ''
        #     new_sent = ''
        #     last_pointer = 0
        #     continue
        new_sent = ' '.join(new_tokens)
        new_sent = new_sent.strip()
        new_sent = re.sub(r'[ ]+', ' ', new_sent)
        new_sent = new_sent.strip()
        if src != new_sent:
            if new_sent != '':
                return new_sent
            else:
                return ''
        else:
            return src
    else:
        return src


def test():
    src = 'I ddid it .'
    tgt = 'I did them .'
    actions = ps2m2.extract(src,tgt)
    print actions
    tgt1 = m2actions_to_sentence(src, actions)
    print tgt1
    print tgt == tgt1


test()