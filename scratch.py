def Practice():
    print('Practice Run')
    messages = (('During the stimulation a fixation cross will appear on '
                 'the screen.\nPlease relax, and focus on the cross when '
                 'it is on the screen.\nAn example of the cross is on the '
                 'next screen.'),
                ('After the Heat Stimulus, a rating scale will appear on '
                    'the screen.\nClick on the line with the mouse, and drag '
                    'the marker to change your selection.\nClick on the '
                    'button to confirm your answer.'),
                ('You are now experiencing no pain, '
                    'please use the scale to indicate this.'),
                ('You are now experiencing mild pain, '
                    'please use the scale to indicate this.'),
                ('You are now experiencing extreme pain, '
                 'please use the scale to indicate this.'))
    stim = ('+', 'rt', 'rt', 'rt', 'rt')
    print(stim, messages)
