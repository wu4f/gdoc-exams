from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

def get_drive_client():
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.appdata']

    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return discovery.build('drive', 'v3', http=creds.authorize(Http()))

def make_copy_in_drive(DRIVE, exam_googledoc_id, student_email, student_name):
    body = {
        'name': f'Exam for {student_name}'
    }
    drive_response = DRIVE.files().copy(fileId=exam_googledoc_id, body=body).execute()
    exam_copy_id = drive_response.get('id')

    batch = DRIVE.new_batch_http_request()
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': student_email
    }
    batch.add(DRIVE.permissions().create(
            fileId=exam_copy_id,
            body=user_permission,
            fields='id',
    ))
    batch.execute()
    return exam_copy_id

students = {
    'cyberdiscoverypdxvol@gmail.com' : 'CyberDiscovery PDX',
    'pwnlandiactf@gmail.com' : 'Pwnlandia CTF'
}

exam_googledoc_id = '1hCCQz7BnaF6JO8BtIyLyFEZpSsRaycJjTS0S75V4YZs'

DRIVE = get_drive_client()

for student in students:
    copy_id = make_copy_in_drive(DRIVE, exam_googledoc_id, student, students[student])
    print(f'copy: {copy_id}  student email: {student}  student name:{students[student]}')