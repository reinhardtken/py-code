import os


DUMP_CMD = '/usr/bin/mongodump'
BACKUP_DIR = '/home/ken/workspace/data/mongodb_backup/'

sample = '/usr/bin/mongodump -d %s -o %s'%('house-trend', BACKUP_DIR)

if __name__ == "__main__":
  dbList = [
    'house',
    'house-cj',
    'house-trend',
    'house-zf'
  ]
  for one in dbList:
    os.system('/usr/bin/mongodump -d %s -o %s'%(one, BACKUP_DIR))