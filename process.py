import sys
import json

def qualify(application, answers):

    questions = application.get('Questions')

    if len(questions) == 0:
        # Applicant answered no questions
        return 'rejected'

    # Flag that we encountered unknown question during check
    saw_unknown = False

    for question in questions:

        qid = question.get('Id')
        app_answer = question.get('Answer')

        # Flag that question applicant answered is found in the list of known correct answers
        q_found = False

        for answer in answers:
            aid = answer.get('Id')
            chk_answer = answer.get('Answer')

            if aid == qid:
                q_found = True
                if app_answer != chk_answer:
                    return 'rejected'

        if not q_found:
            saw_unknown = True

    if saw_unknown:
        # Applicant answered unknown question
        return 'weird'

    return 'accepted'

apps_to_process_file = sys.argv[1]
correct_answers_file = sys.argv[2]

with open(apps_to_process_file) as apps_file:
    applications = json.load(apps_file)

with open(correct_answers_file) as answ_file:
    answers = json.load(answ_file)

accepted_file = open('applications_accepted.json', 'w')
accepted_file.truncate()
# Flag that at least one accepted application was encountered
a_found = False

rejected_file = open('applications_rejected.json', 'w')
rejected_file.truncate()
# Flag that at least one rejected application was encountered
r_found = False

weird_file = open('applications_weird.json', 'w')
weird_file.truncate()
# Flag that at least one weird application was encountered
w_found = False

for application in applications:

    result = qualify(application, answers)
    app_json = json.dumps(application)

    if result == 'accepted':
        if not a_found:
            a_found = True
            accepted_file.write('[\n')
            accepted_file.write(app_json)
        else:
            accepted_file.write(',\n')
            accepted_file.write(app_json)
    elif result == 'rejected':
        if not r_found:
            r_found = True
            rejected_file.write('[\n')
            rejected_file.write(app_json)
        else:
            rejected_file.write(',\n')
            rejected_file.write(app_json)
    elif result == 'weird':
        if not w_found:
            w_found = True
            weird_file.write('[\n')
            weird_file.write(app_json)
        else:
            weird_file.write(',\n')
            weird_file.write(app_json)

if a_found:
    accepted_file.write('\n]')

if r_found:
    rejected_file.write('\n]')

if w_found:
    weird_file.write('\n]')

accepted_file.close()
rejected_file.close()
weird_file.close()
