from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from time import sleep

def get_drive_client():
    SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.appdata']

    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return discovery.build('drive', 'v3', http=creds.authorize(Http()))

def make_copy_in_drive(DRIVE, exam_googledoc_id, student_email, student_name):
    body = {
        'name': f'Exam for {student_name}'
    }
    drive_response = DRIVE.files().copy(fileId=exam_googledoc_id, body=body).execute()
    exam_copy_id = drive_response.get('id')

    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': student_email
    }

    drive_response = DRIVE.permissions().create(
            fileId=exam_copy_id,
            body=user_permission,
            fields='id',
    ).execute()
    permission_id = drive_response.get('id')
    return exam_copy_id, permission_id

def remove_permissions(DRIVE, copyId, permissionId):
    DRIVE.permissions().delete(
            fileId=copyId,
            permissionId=permissionId
    ).execute()


# Must be replaced with your student's e-mail addresses and names
students = {
    'cyberdiscoverypdxvol@gmail.com' : 'CyberDiscovery PDX',
    'pwnlandiactf@gmail.com' : 'Pwnlandia CTF'
}

# Must be replaced with the Google Doc ID of your exam
exam_googledoc_id = '1hCCQz7BnaF6JO8BtIyLyFEZpSsRaycJjTS0S75V4YZs'

# Must be replaced with the duration of your exam (in seconds)
duration = 60

DRIVE = get_drive_client()
permissions = dict()
for student in students:
    copyId, permissionId = make_copy_in_drive(DRIVE, exam_googledoc_id, student, students[student])
    print(f'Exam copy {copyId}  Permission {permissionId}  Student {student}, Student name {students[student]}')
    permissions[copyId] = permissionId

for cnt in range(duration,-1, -1):
    print(f'Seconds left: {cnt}   \r', end='')
    sleep(1)

for id in permissions:
    print(f'Removing permission {permissions[id]} on copyId {id}')
    remove_permissions(DRIVE,id,permissions[id])