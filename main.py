import pymysql
import uuid
from app import app
from db_config import mysql
from flask import jsonify
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory, abort
from werkzeug.utils import secure_filename
import os


# file uploads config
app.config["UPLOADS_FOLDER"] = "C:/Users/madha/Angular/FlaskServices3/uploads"
app.config["ALLOWED_EXTENSIONS"] = ["png", "jpg", "jpeg"]

#checks file extension  
def check_extensions(filename):
	if not "." in filename:
		return False

	extension = filename.rsplit(".", 1)[1].lower()

	if extension in app.config["ALLOWED_EXTENSIONS"]:
		return True
	else:
		return False

# validates file
def file_check(image):
	# check for empty file name
	if image.filename == "":
		print("File must have file name")
		return False

	# check for valid extensions
	if not check_extensions(image.filename):
		print("File extension not allowed")
		return False

	return True

# adds data received to database
@app.route('/add', methods=['POST', 'GET'])
def add_user():
	try:
		# getting req from a form
		_form = request.form
		_name = _form['name']
		_description = _form['description']
		_price = _form['price']
		_image = request.files["image"]
		_imagePath = app.config["UPLOADS_FOLDER"]

		# validate the received values
		if _name and _description and _price and request.method == 'POST':
			    			
			# validate file
			if file_check(_image):

				# updating file name with uuid4 
				filename = str(uuid.uuid4())
				filename += "."
				filename += _image.filename.split(".")[1]
				
				# securing file name for avoiding injections
				filename_secure = secure_filename(filename)
				_image.save(os.path.join(app.config["UPLOADS_FOLDER"], filename_secure))
				
				# save edits
				sql = "INSERT INTO inventory(name, description, price, image, image_path) VALUES(%s, %s, %s, %s, %s)"
				data = (_name, _description, _price, filename_secure, _imagePath,)
				conn = mysql.connect()
				cursor = conn.cursor()
				cursor.execute(sql, data)
				conn.commit()
				resp = jsonify('User added successfully!')
				resp.status_code = 200
				return resp
			else:
				return not_found()
		else:
			redirect(request.url)
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

# get image from the api
@app.route('/get-image/<filename>')
def display_image(filename):
	try:
		return send_from_directory(
			app.config["UPLOADS_FOLDER"], 
			filename=filename, 
			as_attachment = False #True will enable downloading file 
		)
	except FileNotFoundError:
		abort(404)

# fetches all the data from the database
@app.route('/items')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM inventory")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

# fetches signgle item data from the db  
@app.route('/item/<int:id>')
def user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM inventory WHERE id=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

# updates item on the data base
@app.route('/update', methods=['PUT'])
def update_user():
	""" _json = request.json
	_id = _json['id']
	print(_json['id'])
	return request.json """
	try:
		_form = request.form
		_id = _form['id']
		_name = _form['name']
		_description = _form['description']
		_price = _form['price']
		_imagePath = app.config["UPLOADS_FOLDER"]

		# file request check
		if request.files.get('image', None):
			print("image")
			_image = request.files["image"]
		else:
			print("no image")
			_image = False

		# validate the received values
		if _name and _description and _price and _id and request.method == 'PUT':

			if _image:
		
				# validate file
				if file_check(_image):
		
					# updating file name with uuid4 
					filename = str(uuid.uuid4())
					filename += "."
					filename += _image.filename.split(".")[1]
					
					# securing file name for avoiding injections
					filename_secure = secure_filename(filename)
					_image.save(os.path.join(app.config["UPLOADS_FOLDER"], filename_secure))
				
					# save edits
					sql = "UPDATE inventory SET name=%s, description=%s, price=%s, image=%s, image_path=%s WHERE id=%s"
					data = (_name, _description, _price, filename_secure, _imagePath, _id)
				else:
					return not_found()
			else:
				sql = "UPDATE inventory SET name=%s, description=%s, price=%s WHERE id=%s"
				data = (_name, _description, _price, _id)
			
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
# deletes item from the db
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM inventory WHERE id=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
# handles page not found err (404) 
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp
		 
if __name__ == "__main__":
    app.run()