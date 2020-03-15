# Google Doc exams

This script uses the Google Drive API to issue exams to a list of students.
The script takes the Google Doc id of the exam (exam_googledoc_id) and a
dictionary of students (students), then makes an individual copy of the
exam with the student's name in the title and gives the student
Editor permissions on the copy.

Requires that the first 6 steps of this [codelab](https://codelabs.developers.google.com/codelabs/gsuite-apis-intro) be completed.

A subsequent script to remove Editor permissions when the exam is over is
in progress.