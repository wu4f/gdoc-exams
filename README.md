# Google Doc exams

This script uses the Google Drive API to issue exams to a list of students.
The script takes the Google Doc id of the exam (exam_googledoc_id), a
dictionary of students (students), and an exam duration in seconds (duration),
then makes an individual copy of the exam with the student's name in the title and
gives the student Editor permissions on the copy.  The student will receive an
e-mail notifying them of their exam that they can then edit in Google Docs.
After the exam duration finishes, the script then removes their permissions leaving
the instructor with copies of the completed exams.

Run in a virtual environment to avoid conflicts in your Python installation. On Ubuntu,
```
apt install -y python3-pip virtualenv
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
```
Requires that the first 6 steps of this [codelab](https://codelabs.developers.google.com/codelabs/gsuite-apis-intro) be completed.
