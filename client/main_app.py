from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QFileDialog
from PyQt5.QtCore import pyqtSlot
from app.login import Ui_LoginWindow
from app.menu import Ui_MenuWindow
from app.search import Ui_SearchWindow
from app.push_data import Ui_PushWindow
from app.update_data import Ui_UpdateWindow
from app.view import Ui_ViewWindow
from urllib.parse import urljoin
import requests
import os

from abe_core import SelfAES, ABE, objectToBytes, bytesToObject
from base64 import b64encode, b64decode

TRUSTED_AUTHORITY = "https://as9116.duckdns.org"
CLOUD_DOMAIN = "https://cloud9116.duckdns.org"

session = requests.Session()

class MainWindow(QMainWindow, Ui_LoginWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        if not hasattr(self, 'username_textbox') or self.username_textbox is None:
            return
        if not hasattr(self, 'password_textbox') or self.password_textbox is None:
            return
        
        try:
            username = self.username_textbox.text()
            password = self.password_textbox.text()
        except (RuntimeError, AttributeError):
            return

        data = {
            'username': username,
            'password': password
        }
        response = session.post(urljoin(TRUSTED_AUTHORITY, '/login'), data=data)

        if response.status_code == 200:
            data = response.json()
            
            self.uid_text = str(data['ID'])
            
            self.show_menu()
            self.init_keys(data)
        else:
            self.popup(response.text)

    def show_menu(self):
        self.clear_widget_references()
        w = Ui_MenuWindow()
        w.setupUi(self)
        w.text_label.setText("UID: " + self.uid_text)
    
    def clear_widget_references(self):
        """Clear references to widgets from previous screens"""
        # Login screen widgets
        if hasattr(self, 'username_textbox'):
            self.username_textbox = None
        if hasattr(self, 'password_textbox'):
            self.password_textbox = None
        if hasattr(self, 'pushButton'):
            self.pushButton = None
        
        # Upload screen widgets
        if hasattr(self, 'push_uid'):
            self.push_uid = None
        if hasattr(self, 'push_name'):
            self.push_name = None
        if hasattr(self, 'file_name'):
            self.file_name = None
        if hasattr(self, 'combo_box'):
            self.combo_box = None
        if hasattr(self, 'browse_btn'):
            self.browse_btn = None
        
        # Update screen widgets
        if hasattr(self, 'update_uid'):
            self.update_uid = None
        if hasattr(self, 'update_name'):
            self.update_name = None
        if hasattr(self, 'update_file_name'):
            self.update_file_name = None
        if hasattr(self, 'update_combo_box'):
            self.update_combo_box = None
        if hasattr(self, 'update_browse_btn'):
            self.update_browse_btn = None
        
        # Search screen widgets
        if hasattr(self, 'search_combo_box'):
            self.search_combo_box = None
        if hasattr(self, 'search_userid'):
            self.search_userid = None
        if hasattr(self, 'search_name'):
            self.search_name = None
        
        # View screen widgets
        if hasattr(self, 'view_uid'):
            self.view_uid = None
        if hasattr(self, 'view_combo_box'):
            self.view_combo_box = None
        
    def init_keys(self, data):
        response = session.post(urljoin(TRUSTED_AUTHORITY, '/token'), json=data)
        self.token = response.text
        self.attribute = data['attribute']
        
        temp = []
        for attr in self.attribute:
            if attr == 'ent' or attr.lower() == 'patient':
                temp.append('PATIENT'+str(data['ID']))
            else:
                temp.append(attr)
        self.attribute = [attr.upper().replace('_', '') for attr in temp]
        
        print(f"DEBUG - Initialized user attributes: {self.attribute}")
        
        response = session.post(urljoin(TRUSTED_AUTHORITY, '/get_keys'), json={'attribute': str(self.attribute)})
        keys = response.json()
        self.dk_key = keys['dk_key']
        self.pk_key = keys['pk_key']


    @pyqtSlot()
    def on_search_button_clicked(self):
        self.show_search()
    
    def show_search(self):
        self.clear_widget_references()
        w = Ui_SearchWindow()
        w.setupUi(self)
        self.search_combo_box = w.combo_box
        self.search_userid = w.userid_textbox
        self.search_name = w.name_textbox
    
    @pyqtSlot()
    def on_search_api_button_clicked(self):
        headers = {'Authorization': self.token}
        data = {
            'uid': self.search_userid.text(),
            'patient_name': self.search_name.text(),
            'collection_name': self.search_combo_box.currentText()
        }
        
        response = session.post(urljoin(CLOUD_DOMAIN, '/api/search_record'), json=data, headers=headers)
    
        data = response.json()
        if response.status_code != 200:
            self.popup(data['error'])
        else:
            if len(data) == 0:
                self.popup("No records found matching your search criteria.", title="INFO")
            else:
                self.popup_table(data)
        
    def popup_table(self, data):
        window = QDialog(self)
        window.setWindowTitle("Search Results")
        window.resize(600, 400)

        table = QTableWidget()
        if data and len(data) > 0:
            table.setColumnCount(len(data[0])) 
            table.setRowCount(len(data))

            headers = list(data[0].keys())
            table.setHorizontalHeaderLabels(headers)

            for row_num, row_data in enumerate(data):
                for col_num, col_data in enumerate(row_data.values()):
                    item = QTableWidgetItem(str(col_data))
                    table.setItem(row_num, col_num, item)

        layout = QVBoxLayout()
        layout.addWidget(table)
        window.setLayout(layout)
        window.exec()
 
    @pyqtSlot()
    def on_view_button_clicked(self):
        self.show_view()
    
    def show_view(self):
        self.clear_widget_references()
        w = Ui_ViewWindow()
        w.setupUi(self)
        self.view_uid = w.UID
        self.view_combo_box = w.collection
    
    @pyqtSlot()
    def on_view_api_button_clicked(self):
        headers = {'Authorization': self.token}
        data = {
            'uid': self.view_uid.text(),
            'collection_name': self.view_combo_box.currentText()
        }
        response = session.post(urljoin(CLOUD_DOMAIN, '/api/view_patient_record'), json=data, headers=headers)
        
        data = response.json()
        if response.status_code != 200:
            self.popup(data['error'])
        else:
            try:
                if data['patient_data'] == []:
                    raise Exception('None')

                patient_data = data['patient_data'][0]
                
                file_id = patient_data.get('file_id')
                if not file_id:
                    self.popup("No file associated with this record")
                    return
                
                download_response = session.get(
                    urljoin(CLOUD_DOMAIN, f'/api/download_file/{file_id}'),
                    headers=headers
                )
                
                if download_response.status_code == 200:
                    enc_data = download_response.content
                    plain, msg = self.decrypt_file(enc_data)
                    
                    if plain:
                        DOWNLOAD_PATH = './download/'
                        os.makedirs(DOWNLOAD_PATH, exist_ok=True)
                        file_name = patient_data['file_name']
                        with open(DOWNLOAD_PATH+file_name, 'wb') as file:
                            file.write(plain)  
                            
                        msg = "UID: " + patient_data['uid'] + '\n' + \
                            "Patient Name: " + patient_data['patient_name'] + '\n' + \
                            "Attachment Name: " + patient_data['file_name'] + \
                            '\nThe attachment has been downloaded successfully in "download/"'
                                
                        self.popup(msg, title="SUCCESS")
                    elif plain == False:
                        self.popup(msg)
                else:
                    self.popup("Failed to download file from server")
            except Exception as e:
                if str(e) == 'None':
                    self.popup("There's no data with the provided UID.\nPlease generate a profile for it.")    
                else:
                    print(e)
                    
    @pyqtSlot()
    def on_upload_button_clicked(self):
        self.show_push()
    
    def show_push(self):
        self.clear_widget_references()
        w = Ui_PushWindow()
        w.setupUi(self)
        self.push_uid = w.UID
        self.push_name = w.NAME
        self.file_name = w.FileName
        self.combo_box = w.collection
        self.browse_btn = w.browse_button
    
    @pyqtSlot()
    def on_browse_button_clicked(self):
        # Handle both upload and update browse buttons
        if hasattr(self, 'file_name') and self.file_name is not None:
            try:
                file_path, _ = QFileDialog.getOpenFileName(
                    self,
                    "Select File",
                    "",
                    "All Files (*);;PDF Files (*.pdf);;Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
                )
                if file_path:
                    self.file_name.setText(file_path)
            except RuntimeError:
                # Widget has been deleted, ignore
                pass
        elif hasattr(self, 'update_file_name') and self.update_file_name is not None:
            try:
                file_path, _ = QFileDialog.getOpenFileName(
                    self,
                    "Select File",
                    "",
                    "All Files (*);;PDF Files (*.pdf);;Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
                )
                if file_path:
                    self.update_file_name.setText(file_path)
            except RuntimeError:
                # Widget has been deleted, ignore
                pass
    
    @pyqtSlot()
    def on_push_button_clicked(self):
        file_path = self.file_name.text()
        if not file_path:
            self.popup("Please select a file first!")
            return
        if os.path.isfile(file_path):
            headers = {'Authorization': self.token}
            
            UPDATE_POLICIES = {
                'health_record': ['doctor', 'nurse', 'patient'],
                'medicine_record': ['doctor', 'pharmacist', 'patient'],
                'financial_record': ['financial'],
                'research_record': ['doctor', 'researcher'],
            }    
                    
            POLICY = UPDATE_POLICIES[self.combo_box.currentText()]        
            user_attr = [attr.lower() for attr in self.attribute]
            final_policy = self.convert_policy(POLICY, user_attr, self.push_uid.text())
            
            with open(file_path, 'rb') as file:
                file_data = file.read()
            
            enc_data = self.encrypt_file_to_bytes(final_policy, file_data)
            
            files = {'encrypted_file': ('encrypted.json', enc_data, 'application/json')}
            form_data = {
                'uid': self.push_uid.text(),
                'patient_name': self.push_name.text(),
                'file_name': file_path.split('/')[-1],
                'collection_name': self.combo_box.currentText()
            }
            
            response = session.post(urljoin(CLOUD_DOMAIN, '/api/upload_patient_record'), 
                                  data=form_data, files=files, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.popup(data.get('message', 'Upload successful'), title="SUCCESS")
            else:
                try:
                    data = response.json()
                    self.popup(data.get('error', 'Upload failed'))
                except:
                    self.popup(f"Upload failed: {response.text}")
        else:
            self.popup("The file is not exist.\nPlease check the path again!")
    
    
    @pyqtSlot()
    def on_update_button_clicked(self):
        self.show_update()

    def show_update(self):
        self.clear_widget_references()
        w = Ui_UpdateWindow()
        w.setupUi(self)
        self.update_uid = w.UID
        self.update_name = w.NAME
        self.update_file_name = w.FileName
        self.update_combo_box = w.collection
        self.update_browse_btn = w.browse_button

    @pyqtSlot()
    def on_update_api_button_clicked(self):
        file_path = self.update_file_name.text()
        if not file_path:
            self.popup("Please select a file first!")
            return
        if os.path.isfile(file_path):
            headers = {'Authorization': self.token}
                    
            data = {
                'uid': self.update_uid.text(),
                'collection_name': self.update_combo_box.currentText()
            }
            response = session.post(urljoin(CLOUD_DOMAIN, '/api/view_patient_record'), json=data, headers=headers)
            
            data = response.json()
            if response.status_code != 200:
                self.popup(data['error'])
            else:
                patient_data = data['patient_data'][0]
                
                file_id = patient_data.get('file_id')
                if not file_id:
                    self.popup("No file associated with this record")
                    return
                
                download_response = session.get(
                    urljoin(CLOUD_DOMAIN, f'/api/download_file/{file_id}'),
                    headers=headers
                )
                
                if download_response.status_code == 200:
                    enc_data = download_response.content
                    plain, msg = self.decrypt_file(enc_data)
                    
                    if plain is not False:
                        UPDATE_POLICIES = {
                            'health_record': ['doctor', 'nurse', 'patient'],
                            'medicine_record': ['doctor', 'pharmacist', 'patient'],
                            'financial_record': ['financial'],
                            'research_record': ['doctor', 'researcher'],
                        }    
                        
                        POLICY = UPDATE_POLICIES[self.update_combo_box.currentText()]        
                        user_attr = [attr.lower() for attr in self.attribute]
                        final_policy = self.convert_policy(POLICY, user_attr, self.update_uid.text())
                        
                        with open(file_path, 'rb') as file:
                            file_data = file.read()
                        
                        enc_data = self.encrypt_file_to_bytes(final_policy, file_data)
                        
                        files = {'encrypted_file': ('encrypted.json', enc_data, 'application/json')}
                        form_data = {
                            'uid': self.update_uid.text(),
                            'patient_name': self.update_name.text(),
                            'file_name': file_path.split('/')[-1],
                            'collection_name': self.update_combo_box.currentText()
                        }
                        
                        response = session.post(urljoin(CLOUD_DOMAIN, '/api/update_patient_record'), 
                                              data=form_data, files=files, headers=headers)
                        
                        if response.status_code == 200:
                            data = response.json()
                            self.popup(data.get('message', 'Update successful'), title="SUCCESS")
                        else:
                            try:
                                data = response.json()
                                self.popup(data.get('error', 'Update failed'))
                            except:
                                self.popup(f"Update failed: {response.text}")
                    else:
                        self.popup("You don't have permission to update the data!")
        else:
            self.popup("The file is not exist.\nPlease check the path again!")
    
    def convert_policy(self, policy, user_attr, text):

        final_policy = []
        for p in policy:
            tmp = 0
            for p2 in user_attr:
                if p in p2:
                    final_policy.append(p2)
                    tmp = 1
                    continue
            if p == 'patient':
                p = "{}_{}".format(p, text)
            if tmp == 0:
                final_policy.append(p)       

        final_policy = [p.replace('_', '').lower() for p in list(set(final_policy))]
        final_policy = ' or '.join(final_policy)
        
        print(f"DEBUG - Policy created: {final_policy}")
        print(f"DEBUG - User attributes: {user_attr}")
        
        return final_policy
    
    def encrypt_file_to_bytes(self, final_policy, file_data):
        import json
        from io import BytesIO
        aes = SelfAES(); abe = ABE()
        
        enc_file_data = aes.encrypt(file_data)
        key = aes.getKey()
        
        ct_dict = abe.encrypt(self.pk_key.encode(), key, final_policy)
        ct_bytes = objectToBytes(ct_dict['ct'], abe.group)
        enc_key_bytes = ct_dict['enc_key']
        
        encrypted_package = {
            'ct': b64encode(ct_bytes).decode(),
            'enc_key': b64encode(enc_key_bytes).decode(),
            'enc_data': b64encode(enc_file_data).decode()
        }
        
        json_data = json.dumps(encrypted_package)
        return BytesIO(json_data.encode())
    
    def encrypt_and_save_file(self, final_policy, file_data, original_filename):
        import json
        aes = SelfAES(); abe = ABE()
        
        enc_file_data = aes.encrypt(file_data)
        key = aes.getKey()
        
        ct_dict = abe.encrypt(self.pk_key.encode(), key, final_policy)
        ct_bytes = objectToBytes(ct_dict['ct'], abe.group)
        enc_key_bytes = ct_dict['enc_key']
        
        encrypted_package = {
            'ct': b64encode(ct_bytes).decode(),
            'enc_key': b64encode(enc_key_bytes).decode(),
            'enc_data': b64encode(enc_file_data).decode()
        }
        
        UPLOAD_PATH = './upload/'
        os.makedirs(UPLOAD_PATH, exist_ok=True)
        
        enc_filename = f"enc_{original_filename}.json"
        enc_file_path = os.path.join(UPLOAD_PATH, enc_filename)
        
        with open(enc_file_path, 'w') as f:
            json.dump(encrypted_package, f)
        
        return enc_file_path
    
    def decrypt_file(self, enc_file_content):
        import json
        aes = SelfAES(); abe = ABE()
        
        try:
            encrypted_package = json.loads(enc_file_content.decode())
            
            ct_bytes = b64decode(encrypted_package['ct'])
            enc_key_bytes = b64decode(encrypted_package['enc_key'])
            enc_data = b64decode(encrypted_package['enc_data'])
            
            ct_obj = bytesToObject(ct_bytes, abe.group)
            ct_dict = {'ct': ct_obj, 'enc_key': enc_key_bytes}
            
            print(f"DEBUG - User attributes: {self.attribute}")
            print(f"DEBUG - Attempting decryption...")
            
            key = abe.decrypt(self.pk_key.encode(), self.dk_key.encode(), ct_dict)
            
            if key is None:
                print("DEBUG - Decryption failed: User attributes don't match the policy")
                return False, "You don't have permission to access this file. Your attributes don't match the access policy."
            
            plain = aes.decrypt(enc_data, key)
            
            return plain, "SUCCESS"
        except Exception as e:
            print(f"Decryption error: {e}")
            import traceback
            traceback.print_exc()
            return False, "Failed to decrypt the file. You may not have permission."
    
    def encrypt_phase(self, final_policy, file_data):
        import json
        aes = SelfAES() ; abe = ABE()
        enc = b64encode(aes.encrypt(file_data))
        key = aes.getKey()
        
        ct_dict = abe.encrypt(self.pk_key.encode(), key, final_policy)
        ct_bytes = objectToBytes(ct_dict['ct'], abe.group)
        enc_key_bytes = ct_dict['enc_key']
        
        ct_len = len(ct_bytes).to_bytes(4, 'big')
        enc_data = ct_len + ct_bytes + enc_key_bytes + abe.sign + enc
        
        return enc_data
    
    def decrypt_phase(self, enc_data):
        aes = SelfAES(); abe = ABE()
        
        ct_len = int.from_bytes(enc_data[:4], 'big')
        ct_bytes = enc_data[4:4+ct_len]
        
        remaining = enc_data[4+ct_len:]
        parts = remaining.split(abe.sign)
        enc_key_bytes = parts[0]
        enc = parts[1]
        
        try:
            ct_obj = bytesToObject(ct_bytes, abe.group)
            ct_dict = {'ct': ct_obj, 'enc_key': enc_key_bytes}
            
            key = abe.decrypt(self.pk_key.encode(), self.dk_key.encode(), ct_dict)
            
            try:
                plain = aes.decrypt(b64decode(enc), key)   
                return plain, "SUCCESS"
            except:
                return False, "Failed to decrypt the data. Please try again"
        except:
            return False, "You don't have permission to decrypt the data!"
            
    
    @pyqtSlot()
    def on_back_button_clicked(self):
        self.show_menu()
    
    @pyqtSlot()
    def on_logout_button_clicked(self):
        reply = QMessageBox.question(
            self,
            'Logout Confirmation',
            'Are you sure you want to logout?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Clear session data
            session.cookies.clear()
            
            # Clear user data
            if hasattr(self, 'token'):
                delattr(self, 'token')
            if hasattr(self, 'attribute'):
                delattr(self, 'attribute')
            if hasattr(self, 'dk_key'):
                delattr(self, 'dk_key')
            if hasattr(self, 'pk_key'):
                delattr(self, 'pk_key')
            if hasattr(self, 'uid_text'):
                delattr(self, 'uid_text')
            
            # Clear all widget references
            self.clear_widget_references()
            
            # Recreate login screen properly
            w = Ui_LoginWindow()
            w.setupUi(self)
            
            # Show success message after UI is ready
            QMessageBox.information(self, "Success", "Logged out successfully")
    
    def popup(self, message, title="ERROR"):
        window = QMessageBox(self)
        window.setWindowTitle(title)
        window.setText(message)
        window.exec()


if __name__ == "__main__":
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()