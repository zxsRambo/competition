import sys
planFile = "data/plan/signal_plan.txt"

plan = open(planFile)
phases = plan.readlines()
current_phase = phases[1].strip('\n')
flag = True
error_info = ''
yellow_time = 0

# get first green phase and check
last_green_phase = '*'
if phases[1].strip('\n') == '0':
    flag = False
    error_info = 'Yellow light is not allowed to appear in the beginning'
else:
    for next_phase in phases[2:]:
        next_phase = next_phase.strip('\n')

        # check phase itself
        if next_phase not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '']:
            flag = False
            error_info = 'Phase must be in [0, 1, 2, 3, 4, 5, 6, 7, 8]'
            break
        if next_phase == '':
            continue

        # check changing phase
        if next_phase != current_phase and next_phase != '0' and current_phase != '0':
            flag = False
            error_info = '5 seconds of yellow time must be inserted between two different phase'
            break

        # check unchangeable phase
        if next_phase != '0' and next_phase == last_green_phase:
            flag = False
            error_info = 'No yellow light is allowed between the same phase'
            break

        # check yellow time
        if next_phase != '0' and yellow_time != 0 and yellow_time != 5:
            flag = False
            error_info = 'Yellow time must be 5 seconds'
            break

        # normal
        if next_phase == '0':
            yellow_time += 1
            if current_phase != '0':
                last_green_phase = current_phase
        else:
            yellow_time = 0
        current_phase = next_phase

print(flag)
if not flag:
    print(error_info)