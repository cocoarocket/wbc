__author__ = 'phoenix_aka_cocoarocket'
import re, os, urllib, httplib, sqlite3
from datetime import datetime
#import encodings

if __name__ == '__main__':
  params = urllib.urlencode({'spam': 1, 'eggs': 2, 'bacon': 0})
  headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
  conn = httplib.HTTPConnection("junona.org")
  conn.request("GET", "/modules.php?name=Sonnic", params, headers)
  response = conn.getresponse()

  print response.status, response.reason
  data = response.read()
  conn.close()

  regex1 = '<a href="(modules\.php\?name=Sonnic&pa=alphabet&letter=[\W\w\S\s]+?)">[\W\w\S\s]+?<\/a>'
  regex2 = '(?<=modules\.php\?name=Sonnic&pa=alphabet&letter=)[\W\w\S\s]+'
  regex3 = 'modules\.php\?name=Sonnic&pa=alphabet&letter=([\W\w\S\s]+)'

  s1 = re.compile(regex1,re.IGNORECASE | re.MULTILINE)
  s2 = re.compile(regex2,re.IGNORECASE)
  s3 = re.compile(regex3,re.IGNORECASE)

  f1 = s1.findall(data)
  
  connect_db = sqlite3.connect('dreams.db')
  sql = connect_db.cursor()

  #sql.execute("SELECT count(name) FROM sqlite_master where name='tablename'") 
  #rq = sql.fetchone()
  
  #ID INTEGER PRIMARY KEY AUTOINCREMENT
  sql.execute("CREATE TABLE IF NOT EXISTS 'dreams_alpabet' (\
    'pid' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
    'flink' varchar(255) NOT NULL,\
    'alpha' varchar(4) NOT NULL)")
  
  #sql.execute("SELECT * FROM dreams_alpabet")
  #rq = sql.fetchall()
  #for t in rq:
    #print t
  
  for i, t in enumerate(f1):
    f3 = s3.findall(t)
    v = (f3[0],)
    sql.execute("SELECT pid FROM dreams_alpabet WHERE alpha = ?",v)
    rq = sql.fetchall()
    if rq == []:
      v = (t,f3[0])
      sql.execute("INSERT INTO dreams_alpabet (flink,alpha) VALUES (?,?)",v)
    else:
      print '[record %s] exist' % t
  
  sql.connection.commit()
  sql.close()
  
    #file.write('%s\n' % t)
  #file.close()
    
    #t = s2.sub(f3[0].decode('hex'),t)
    #print f3[0] #alpha
    #print t #flink
  
    #print f3[0].decode('hex')
    
    #ch1 = f3[0][0:2].upper()
    #ch2 = f3[0][2:4].upper()
    #f3[0] = urllib.unquote('%%%s%%%s' % (ch1, ch2))      
    #s = f3[0].decode('unicode_escape')
    #s = bytes.fromhex(f3[0]).decode('utf-8')
    #print 'index {0}\{1} {2}'.format(i, f3, t)    
