import cx_Oracle

#create connection
conn = cx_Oracle.connect('CISEServer/cameronkeene@//oracle.cise.ufl.edu:1521/orcl')
print(conn.version)
