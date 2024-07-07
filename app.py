import json, fitz
import shutil
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, render_template, url_for, redirect, request, flash,send_file
from flask_login import login_required, logout_user, LoginManager, current_user, login_user
from function.connect import db
from function.models import User,Folder,File
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
from script.convert_txt_to_csv import convert_to_csv
import os, io, base64
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a secrect key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Account.db'
folder_data_dir = '../folder_data'
os.environ['R_HOME'] = 'C:\Program Files\R\R-4.4.0'

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def start():
    return redirect(url_for('homepage'))
@app.route('/demo')
def demo():
    return render_template('demo.html')
@app.route('/pipeline')
def pipeline():
    return render_template('pipeline.html')
@app.route('/homepage')
def homepage():
    current_user.role=0
    return render_template('index.html')
@app.route('/ourstory')
def ourstory():
    return render_template('ourstory.html')
@app.route("/aboutus")
def about_us():
    return render_template('about_us.html')


@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form["email"]
        users = User.query.filter_by(email = email).first()
        if users:
            return redirect(url_for('reset_password', email=email))
        else:
            flash("The email does not match", category= 'error')
            return render_template('forgot.html')
    
    return render_template('forgot.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                role=user.role
                if role==2 or role==3:
                        flash('Logged in successfully!', category='success')
                        login_user(user, remember=False)
                        return redirect(url_for('home'))
                elif role==1:
                    login_user(user,remember=False)
                    return redirect(url_for("admin"))
            else:
                flash('Incorrect password! Try again!', category='error')
        else:
            flash('User does not exist!', category='error')
    # return render_template("login.html")

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re-password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character', category='error')
        elif password != re_password:
            flash('Passwords do not match!', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            folder_path = f"{folder_data_dir}/{username}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()
           
            flash('Sign up successful!', category='success')
            return redirect(url_for('homepage'))
    return redirect(url_for('homepage'))

@app.route('/home')
@login_required
def home():
    folders = Folder.query.filter_by(user_id=current_user.id).all()
    files = File.query.filter_by(user_id = current_user.id).all()
    return render_template("home.html",folders = folders, user = current_user, files = files)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Log out success")
    return redirect(url_for('homepage'))

@app.route('/folder', methods = ['POST'])
@login_required
def folder():
    if request.method == 'POST':
        if 'folderName' in request.form:
            folder_name = request.form['folderName']
            if folder_name == '':
                flash('No folder name provied!', category= 'error')
            else:
                folder_path = f"{folder_data_dir}/{current_user.username}/{folder_name}"
                folder=Folder.query.filter_by(path=folder_path).first()
                if folder==None:

                    # Add folder to database
                    new_folder = Folder(path = folder_path,name= folder_name, user_id = current_user.id)
                    db.session.add(new_folder)
                    db.session.commit()
                    flash("Folder create successfully", category= 'success')
                else:
                    flash("Folder already exists",category='error')
                
    return redirect(url_for('home'))

@app.route('/folder/<folder_id>', methods=['GET', 'POST'])
@login_required
def get_folder(folder_id):
    folder = Folder.query.get_or_404(folder_id)
    file = File.query.filter_by(folder_id=folder.id).first()
    if request.method == 'POST':

        if 'inputFile1' in request.files:
            sub_file = request.files['inputFile1']
            
            if sub_file.filename != '':
                if sub_file.filename.endswith(".hmp.txt"):
                    file_name=f"{folder.name}.hmp.txt"
                elif sub_file.filename.endswith(".csv") or sub_file.filename.endswith("xlsx"):
                    file_name=f"{folder.name}.xlsx"
                path=f"{folder_data_dir}/{current_user.username}"
                path+=f"/{file_name}"
                file=File.query.filter_by(path=path).first()
                if file==None:
                    # Save the uploaded file to the specified path
                    sub_file.save(path)

                    # Add the file to the database
                    new_file = File(name=file_name, path=path, user_id=current_user.id, folder_id=folder.id)
                    db.session.add(new_file)
                    db.session.commit()

                    flash('Subfile uploaded successfully!', category='success')

        if 'inputFile2' in request.files:
            sub_file = request.files['inputFile2']
            
            if sub_file.filename != '':
                file_name=f"{folder.name}_2.fastq.gz"
                path=f"{folder_data_dir}/{current_user.username}"
                path+=f"/{file_name}"
                file=File.query.filter_by(path=path).first()
                if file==None:
                    # Save the uploaded file to the specified path
                    sub_file.save(path)

                    # Add the file to the database
                    new_file = File(name=file_name, path=path, user_id=current_user.id, folder_id=folder.id)
                    db.session.add(new_file)
                    db.session.commit()

                    flash('Subfile uploaded successfully!', category='success')

    if os.path.exists(f"{folder.path}_input"):
        if os.path.exists("Rplots.pdf"):
            shutil.copy2("Rplots.pdf",f"{folder_data_dir}/{current_user.username}")
            os.remove("Rplots.pdf")

        file=File.query.filter_by(name="Rplots.pdf").first()
        if file == None:
            new_file = File(name="Rplots.pdf", path=f"{folder_data_dir}/{current_user.username}/Rplots.pdf",user_id=current_user.id, folder_id=folder.id)
            db.session.add(new_file)
            db.session.commit()

        files = [file for file in os.listdir(f"{folder.path}_input")]
        for file in files:
            check_file = File.query.filter_by(name=file).first()
            if check_file==None:
                new_file = File(name=file, path=f"{folder.path}_input/{file}",user_id=current_user.id, folder_id=folder.id)
                db.session.add(new_file)
                db.session.commit()

    files = [file for file in os.listdir(f"{folder_data_dir}/{current_user.username}")]
    for file in files:
        if file.endswith("significant SNPs.txt"):
            convert_to_csv(f"{folder_data_dir}/{current_user.username}/{file}", f"{folder_data_dir}/{current_user.username}/List of all significant SNPs.csv")
            check_file = File.query.filter_by(name="List of all significant SNPs.csv").first()
            if check_file == None:
                new_file = File(name="List of all significant SNPs.csv", path=f"{folder_data_dir}/{current_user.username}/List of all significant SNPs.csv",user_id=current_user.id, folder_id=folder.id)
                db.session.add(new_file)
                db.session.commit()

    subfolders = Folder.query.filter_by(parent_folder_id=folder.id).all()
    subfiles = File.query.filter_by(folder_id=folder.id).all()
    snps=[]
    preprocess=[]
    files=[]
    for file in subfiles:
        if file.name.endswith(".csv") or file.name.startswith("r.") or file.name.endswith("pdf") or file.name.startswith("List "):
            if file.name.endswith(".csv") and file.name!="Rplots.pdf":
                snps.append(file)
            else:
                preprocess.append(file)
        else:
            files.append(file)
    return render_template('folder.html', folder=folder, subfolders=subfolders, file = file, subfiles = files, preprocess=preprocess, snps=snps, user = current_user)

@app.route('/file/<file_id>', methods = ['GET', 'POST'])
@login_required
def get_file(file_id):
    file = File.query.get_or_404(file_id)
    file_path = file.path

    if file.name.endswith(".pdf"):
        pdf_path = f"{folder_data_dir}/{current_user.username}/Rplots.pdf"
        doc = fitz.open(pdf_path)
        images = []
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes(output="png")))
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            images.append(img_str)

        return render_template('view_pdf.html', images=images)

    df = pd.read_csv(file_path)
    if file.name.endswith(".txt"):
        with open(file_path, 'r') as file:
            file_content = file.read()
            return file_content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    
    if request.method == 'POST':
        # Take requests from form
        selected_columns = request.form.getlist('columns')
        
        # Create dataframe for all the columns have choosed
        selected_df=df[selected_columns]
        temp_file_path = f'{folder_data_dir}/{current_user.username}/temp_selected_data.csv'
        selected_df.to_csv(temp_file_path, index=False)
        selected_df=selected_df.head(20)

        # Conver dataframe to html
        table_html=selected_df.to_html(classes='table table-striped', index=False)

        # Send data to user
        return render_template('display_columns.html', table_html=table_html, columns=df.columns, user=current_user, file=file)
    return render_template('select_columns.html', columns=df.columns,user = current_user)
    
@app.route('/delete-subfile', methods=['POST'])
@login_required
def delete_subfile():
    try:
        event = json.loads(request.data)
        file_id = event['Id']
        file = File.query.filter_by(id=file_id, user_id=current_user.id).first()

        if file:
            if file.user_id == current_user.id:
                folder = Folder.query.get(file.folder_id)
                if folder and is_file_in_folder(file, folder):
                    file_to_delete = file.path
                    if os.path.exists(file_to_delete):
                        os.remove(file_to_delete)
                        flash('File deleted from folder successfully',category='success')
                        db.session.delete(file)
                        db.session.commit()
                    else:
                        flash('File not found in folder',category='error')
                else:
                    flash('File not found in folder',category='error')
            else:
                flash('You do not have permission to delete this file',category='error')
        else:
            raise ValueError('File not found')

        return jsonify({})
    except Exception as e:
        flash(f"Error deleting file: {e}",category='error')
        return jsonify({'Status': 'Error occurred while deleting the file.'}), 500
    
@app.route('/delete-folder', methods=['POST'])
@login_required
def delete_folder():
    try:
        event = json.loads(request.data)
        folder_id = event['Id']
        delete_folder_recursive(folder_id)
        flash('Delete successfully',category='success')
        return jsonify({'Status':'Success to delete folder'})
    except Exception as e:
        flash(f"Error deleting folder: {e}",category='error')
        return jsonify({'Status': 'Error occurred while deleting the folder.'}), 500

@app.route('/reset',methods=['POST','GET'])
@login_required
def reset():
    if request.method=='POST':
        password=request.form["password"]
        user=User.query.filter_by(username=current_user.username).first()
        if check_password_hash(user.password, password):
            return redirect(url_for('reset_password', email=user.email))
    return render_template("reset.html")

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')
    
    if request.method == 'POST':
        # Handle the password reset form submission
        password = request.form['password']
        re_password = request.form['re-password']
        
        # Validate the password and re_password
        if password != re_password:
            flash('Passwords do not match!', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            # Update the user's password in the database
            user = User.query.filter_by(email=email).first()
            if user:
                hashed_password = generate_password_hash(password)
                user.password = hashed_password
                db.session.commit()
                flash("Your password has been reset successfully.", category='success')
                return redirect(url_for('login'))
            else:
                flash("User not found.", category='error')
    
    return render_template('reset_password.html', email=email)

@app.route('/download/<file_id>',methods=['GET'])
@login_required
def download_file(file_id):
    return send_file(path_or_file=f"{folder_data_dir}/{current_user.username}/temp_selected_data.csv", as_attachment=True, mimetype="text/csv")
    
@app.route('/execute', methods = ['POST'])
@login_required
def execute_fatsq():
    from executing import execute_file
    event=json.loads(request.data)
    id=event['Id']
    folder=Folder.query.filter_by(id = id).first()
    try:
        execute_file(folder, current_user)
        return jsonify({"Status":"True"})
    except:
        return jsonify({"Status":"False"})

# Admin
@app.route('/admin', methods=['POST','GET'])
@login_required
def admin():
    admin=User.query.filter(User.role!=1).all()
    return render_template('admin.html',user=admin)

@app.route('/create_user',methods=['POST','GET'])
@login_required
def create_user():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re-password')

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character', category='error')
        elif password != re_password:
            flash('Passwords do not match!', category='error')
        elif len(password) < 7:
            flash('Password must be greater than 7 characters', category='error')
        else:
            folder_path = f"{folder_data_dir}/{username}"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password, method='pbkdf2:sha256')
            )
            db.session.add(new_user)
            db.session.commit()

        return redirect(url_for('admin'))

    return render_template('add_user.html', user=current_user)

@app.route("/change_role", methods=["POST"])
@login_required
def change_role():
    try:
        user_data=json.loads(request.data)
        user_id=user_data['userId']
        user=User.query.filter_by(id=user_id).first()
        if user.role==2:
            user.role=3
        elif user.role==3:
            user.role=2
        db.session.commit()
        flash("Update successfully", category='Success')
        return redirect(url_for("admin"))
    except Exception as e:
        flash(f"Error removing user: {e}", category='error')
        return redirect(url_for("admin"))

@app.route('/delete-user', methods=['POST'])
@login_required
def rm_user():
    try:
        user_data = json.loads(request.data)
        rm_user = user_data['userId']
        user_to_delete=User.query.filter_by(id=rm_user).first()
        file_to_delete=File.query.filter_by(user_id=rm_user).all()
        folder_to_delete=Folder.query.filter_by(user_id=rm_user).all()
        if user_to_delete:
            for file_obj in file_to_delete:
                db.session.delete(file_obj)
            for folder_obj in folder_to_delete:
                db.session.delete(folder_obj)
            db.session.delete(user_to_delete)
            db.session.commit()
            shutil.rmtree(f"{folder_data_dir}/{user_to_delete.username}")
            flash("Deleted successfully", category='success')
            return redirect(url_for("admin"))
        else:
            raise ValueError(f"User with id {rm_user} not found")
    except Exception as e:
        flash("Error removing user: {e}",category='error')
        return redirect(url_for("/admin"))

def is_file_in_folder(file, folder):
    # Check if the file's folder matches the specified folder or any of its subfolders
    if file.folder_id == folder.id:
        return True
    elif folder.subfolders:
        for subfolder in folder.subfolders:
            if is_file_in_folder(file, subfolder):
                return True
    return False

def delete_folder_recursive(folder_id):
    folder = Folder.query.filter_by(id=folder_id).first()
    if folder is None:
        return jsonify({"Status":"Fail"})

    # Delete files in the current folder
    delete_files_in_folder(folder.id)

    # Delete the current folder
    db.session.delete(folder)
    db.session.commit()

def delete_files_in_folder(folder_id):
    files = File.query.filter_by(folder_id=folder_id).all()
    for file in files:
        os.remove(file.path)
        db.session.delete(file)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
