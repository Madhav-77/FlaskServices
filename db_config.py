from app import app
from flaskext.mysql import MySQL

mysql = MySQL()

# local MySQL configurations 
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'shop_bridge'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'

# prod MySQL configurations 
app.config['MYSQL_DATABASE_USER'] = 'sql12366947'
app.config['MYSQL_DATABASE_PASSWORD'] = 'GGX6Kf1rwz'
app.config['MYSQL_DATABASE_DB'] = 'sql12366947'
app.config['MYSQL_DATABASE_HOST'] = 'sql12.freemysqlhosting.net'

mysql.init_app(app)