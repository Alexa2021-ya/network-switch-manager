from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
import sys
import snmp
from db import *
from snmp import *

class DialogModel(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Модель')
        self.line_edit_name = QtWidgets.QLineEdit()
              
        form_layout = QtWidgets.QFormLayout()
        form_layout.addRow('Name:', self.line_edit_name)
        
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

class TableModel(QtSql.QSqlTableModel):
    def __init__(self):
        super(TableModel, self).__init__()
        self.list_vertical_header = ['Address Learning', 'Count Ports', 'Flow Control', 'Index Port', 'Link Status', 'MDIX', 'Medium Type', 'Speed', 'State Port']
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return ['ID', 'Наименование', 'Значение', 'Модель'][section]
            if orientation == QtCore.Qt.Vertical:
                return ['Address Learning', 'Count Ports', 'Flow Control', 'Index Port', 'Link Status', 'MDIX', 'Medium Type', 'Speed', 
                        'State Port'][section]

    def get_list_vertical_header(self):
        return self.list_vertical_header

    def rowCount(self, index):
        return len(self.list_vertical_header)

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.id_model = ''
        self.ip_device = ''
        self.list_devices_ports = []
        self.list_devices_device = []
        self.list_oids_device = []
        self.db = DB()
        self.db.createConnection()
        self.setupUi(self)
        self.fill_combobox_devices()
        self.fill_oids()

    def fill_combobox_settings_ports(self):
        self.combobox_state.setCurrentIndex(0)
        self.combobox_medium_type.setCurrentIndex(0)
        self.combobox_address_learning.setCurrentIndex(0)
        self.combobox_flow_control.setCurrentIndex(0)
        self.combobox_mdix.setCurrentIndex(0)
        self.combobox_speed.setCurrentIndex(0)
        self.combobox_from_port.setCurrentIndex(0)
        self.combobox_to_port.setCurrentIndex(0)

    def get_state_port(self):
        if (self.combobox_state.currentText() == 'Enabled'):
            return 3
        else:
            return 2

    def get_medium_type(self):
        if (self.combobox_medium_type.currentText() == 'copper'):
            return 1
        else:
            return 2

    def get_address_learning(self):
        if (self.combobox_address_learning.currentText() == 'Enabled'):
            return 3
        else:
            return 2

    def get_flow_control(self):
        if (self.combobox_flow_control.currentText() == 'Enabled'):
            return 3
        else:
            return 2

    def get_mdix(self):
        if (self.combobox_mdix.currentText() == 'auto'):
            return 1
        elif (self.combobox_mdix.currentText() == 'normal'):
            return 2
        else:
            return 3

    def get_speed(self):
        if (self.combobox_speed.currentText() ==  'nway-enabled'):
            return 2
        elif (self.combobox_speed.currentText() == 'nway-disabled-10Mbps-Half'):
            return 3
        elif (self.combobox_speed.currentText() == 'nway-disabled-10Mbps-Full'):
            return 4
        elif (self.combobox_speed.currentText() == 'nway-disabled-100Mbps-Half'):
            return 5
        elif (self.combobox_speed.currentText() == 'nway-disabled-100Mbps-Full'):
            return 6
        elif (self.combobox_speed.currentText() == 'nway-disabled-1Gigabps-Half'):
            return 7
        elif (self.combobox_speed.currentText() == 'nway-disabled-1Gigabps-Full'):
            return 8
        elif (self.combobox_speed.currentText() == 'nway-disabled-1Gigabps-Full-master'):
            return 9
        else:
            return 10

    def apply(self):
        try:
            id_device = self.get_id_combobox_ports_device()
            self.ip_device = self.db.get_ip_device(id_device)[0]
            self.id_model = self.db.get_id_model_device(id_device)[0]

            oids = self.db.get_oids(self.id_model)
            names_oids = self.db.get_names_oids(self.id_model)
            self.list_oids_device = self.get_dict(self.get_list_db(oids), self.get_list_db(names_oids))

            device = Device(self.ip_device)

            number1 = int(self.combobox_from_port.currentText())
            number2 = int(self.combobox_to_port.currentText())

            address_learning = self.get_address_learning()
            flow_control = self.get_flow_control()
            mdix = self.get_mdix()
            speed = self.get_speed()
            state = self.get_state_port()
            list_index = device.get_index_ports(self.list_oids_device['Index Port'])
            medium_type = ''
            oids_address_learning = []
            oids_flow_control = []
            oids_mdix = []
            oids_speed = []
            oids_state = []
            if (number1 == number2):
                medium_type = self.get_medium_type()
                oids_address_learning = device.change_type_list_oids([[self.list_oids_device['Address Learning'] + '.' + str(number1) + '.' +
                                                                      str(medium_type), address_learning]])
                oids_flow_control = device.change_type_list_oids([[self.list_oids_device['Flow Control'] + '.' + str(number1) + '.' +
                                                                      str(medium_type), flow_control]])
                oids_mdix = device.change_type_list_oids([[self.list_oids_device['MDIX'] + '.' + str(number1) + '.' +
                                                                      str(medium_type), mdix]])
                oids_speed = device.change_type_list_oids([[self.list_oids_device['Speed'] + '.' + str(number1) + '.' +
                                                                      str(medium_type), speed]])
                oids_state = device.change_type_list_oids([[self.list_oids_device['State Port'] + '.' + str(number1) + '.' +
                                                                      str(medium_type), state]])
                
                device.set_address_learning(oids_address_learning)
                device.set_flow_control(oids_flow_control)
                device.set_mdix(oids_mdix)
                device.set_speed(oids_speed)
                device.set_state_port(oids_state)
            else:
                medium_type = device.get_medium_types_ports(self.list_oids_device['Medium Type'])
                for port in range(list_index.index(number1), len(list_index)):
                    if (number2 < list_index[port]):
                        break
                    else:
                        oids_address_learning.append([self.list_oids_device['Address Learning'] + '.'
                                                                    + str(list_index[port]) + '.' + str(medium_type[port]), address_learning])
                        oids_flow_control.append([self.list_oids_device['Flow Control'] + '.'
                                                                    + str(list_index[port]) + '.' + str(medium_type[port]), flow_control])
                        oids_mdix.append([self.list_oids_device['MDIX'] + '.'
                                                                    + str(list_index[port]) + '.' + str(medium_type[port]), mdix])
                        oids_speed.append([self.list_oids_device['Speed'] + '.'
                                                                    + str(list_index[port]) + '.' + str(medium_type[port]), speed])
                        oids_state.append([self.list_oids_device['State Port'] + '.'
                                                                    + str(list_index[port]) + '.' + str(medium_type[port]), state])
                        
                oids_address_learning = device.change_type_list_oids(oids_address_learning)
                oids_flow_control = device.change_type_list_oids(oids_flow_control)
                oids_mdix = device.change_type_list_oids(oids_mdix)
                oids_speed = device.change_type_list_oids(oids_speed)
                oids_state = device.change_type_list_oids(oids_state)
                
                device.set_address_learning(oids_address_learning)
                device.set_flow_control(oids_flow_control)
                device.set_mdix(oids_mdix)
                device.set_speed(oids_speed)
                device.set_state_port(oids_state)

            self.fill_combobox_settings_ports()
            self.fill_ports()
        except:
            print("Error")

    def refresh(self):
        self.fill_ports()

    def fill_oids(self):
        id_model = self.get_id_combobox_devices_device()

        if (not self.db.get_oids(id_model)):
            list_vertical_header = self.model_sql_oid.get_list_vertical_header()
            for i in range(len(list_vertical_header)):
                self.db.add_oid(list_vertical_header[i], "", id_model)
            self.model_sql_oid.select()

    def get_list_db(self, data):
        list_db = []
        for i in range(len(data)):
            list_db.append(data[i][0])
        return list_db

    def get_dict(self, list1, list2):
        return dict(zip(list2, list1))

    def fill_combobox_devices(self):        
        devices_ports = self.db.get_list_devices()
        devices_ports = self.get_list_db(devices_ports)
        
        devices_device = self.db.get_list_models_devices()
        devices_device = self.get_list_db(devices_device)

        names_models = self.db.get_name_models_devices()
        
        for i in range(len(devices_ports)):
            if (names_models[i]):
                devices_ports[i] = devices_ports[i] + ' ' + names_models[i][0]
        id_device = self.db.get_id_devices()
        id_device = self.get_list_db(id_device)
    
        id_model = self.db.get_id_models()
        id_model = self.get_list_db(id_model)

        devices_ports = self.get_dict(devices_ports, id_device)
        devices_device = self.get_dict(devices_device, id_model)
        list1 = []
        list2 = []
        for i in range(len(devices_ports)):
            list1.append(i)

        for i in range(len(devices_device)):
            list2.append(i)
    
        self.list_devices_ports = self.get_dict(id_device, list1)
        self.list_devices_device = self.get_dict(id_model, list2)
        
        self.combobox_ports_device.clear()
        self.combobox_devices_device.clear()

        self.combobox_ports_device.addItems(devices_ports.values())
        self.combobox_devices_device.addItems(devices_device.values())

        self.signal_combobox_devices_device()

    def fill_ports(self):
        id_device = self.get_id_combobox_ports_device()
        self.ip_device = self.db.get_ip_device(id_device)[0]
        self.id_model = self.db.get_id_model_device(id_device)[0]
        oids = self.db.get_oids(self.id_model)
        names_oids = self.db.get_names_oids(self.id_model)
        self.list_oids_device = self.get_dict(self.get_list_db(oids), self.get_list_db(names_oids))
        
        try:
            device = Device(self.ip_device)
            data = list(set(device.get_index_ports(self.list_oids_device['Index Port'])))
            for i in range(len(data)):
                data[i] = str(data[i])
                
            self.combobox_from_port.addItems(data)
            self.combobox_to_port.addItems(data)
            count_ports = device.get_count_ports(self.list_oids_device['Count Ports'])
            self.table_ports.setRowCount(count_ports)
            #Порты
            list_ports = device.get_list_ports(self.list_oids_device['Index Port'],
                        self.list_oids_device['Medium Type'])
            for i in range(count_ports):
                item = QtWidgets.QTableWidgetItem()
                item.setText(list_ports[i])
                self.table_ports.setItem(i, 0, item)
            list_states = device.get_states_ports(self.list_oids_device['State Port'])
            for i in range(count_ports):
                item = QtWidgets.QTableWidgetItem()
                if (list_states[i] == 2):
                    item.setText('Disabled')
                else:
                    item.setText('Enabled')
                self.table_ports.setItem(i, 1, item)
            list_speeds = device.get_speeds_ports(self.list_oids_device['Speed'])
            for i in range(count_ports):
                item = QtWidgets.QTableWidgetItem()
                if (list_speeds[i] == 2):
                    item.setText('nway-enabled')
                elif (list_speeds[i] == 3):
                    item.setText('nway-disabled-10Mbps-Half')
                elif (list_speeds[i] == 4):
                    item.setText('nway-disabled-10Mbps-Full')
                elif (list_speeds[i] == 5):
                    item.setText('nway-disabled-100Mbps-Half')
                elif (list_speeds[i] == 6):
                    item.setText('nway-disabled-100Mbps-Full')
                elif (list_speeds[i] == 7):
                    item.setText('nway-disabled-1Gigabps-Half')
                elif (list_speeds[i] == 8):
                    item.setText('nway-disabled-1Gigabps-Full')
                elif (list_speeds[i] == 9):
                    item.setText('nway-disabled-1Gigabps-Full-master')
                elif (list_speeds[i] == 10):
                    item.setText('nway-disabled-1Gigabps-Full-slave')
                self.table_ports.setItem(i, 2, item)

            list_flow_control = device.get_flow_control_ports(self.list_oids_device['Flow Control'])
            for i in range(count_ports):
                item = QtWidgets.QTableWidgetItem()
                if (list_flow_control[i] == 2):
                    item.setText('Disabled')
                else:
                    item.setText('Enabled')
                self.table_ports.setItem(i, 3, item)

            list_address_learning = device.get_address_learning_ports(self.list_oids_device['Address Learning'])
            for i in range(count_ports):
                item = QtWidgets.QTableWidgetItem()
                if (list_address_learning[i] == 2):
                    item.setText('Disabled')
                else:
                    item.setText('Enabled')
                self.table_ports.setItem(i, 6, item)

            list_link_status = device.get_link_status_ports(self.list_oids_device['Link Status'])
            for i in range(count_ports):
                item = QtWidgets.QTableWidgetItem()
                if (list_link_status[i] == 2):
                    item.setText('link pass')
                else:
                    item.setText('link fail')
                self.table_ports.setItem(i, 4, item)
                list_mdix = device.get_mdix_ports(self.list_oids_device['MDIX'])
            for i in range(count_ports):
                item = QtWidgets.QTableWidgetItem()
                if (list_mdix[i] == 1):
                    item.setText('Auto')
                elif(list_mdix[i] == 2):
                    item.setText('Normal')
                else:
                    item.setText('Cross')
                self.table_ports.setItem(i, 5, item)
                
        except:
             msg = QtWidgets.QMessageBox.critical(self, 'Внимание', 'Не удаётся подключиться к оборудованию!')


    def add_model(self):
        inputDialog = DialogModel()
        rez = inputDialog.exec()
        if not rez:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
            return  
        name = inputDialog.line_edit_name.text()
        if not name:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
            return

        r = self.model_sql_models.record()
        r.setValue("model_name", name)
        self.model_sql_models.insertRecord(-1, r)
        self.model_sql_models.select()

        self.change_device()

    def delete_model(self):
        row = self.table_models.currentIndex().row()
        if row == -1:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Выберите запись для удаления.')
            return          

        name = self.model_sql_models.record(row).value(1)
        
        inputDialog = DialogModel()
        inputDialog.setWindowTitle('Удалить запись? Все связанные записи будут удалены.')
        inputDialog.line_edit_name.setText(name)
        
        rez = inputDialog.exec()
        if not rez:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
            return

        id_model = self.model_sql_models.index(self.table_models.currentIndex().row(), 0).data()
        self.db.delete_model(id_model)             
        self.model_sql_models.select()
        self.fill_combobox_devices()
        self.change_device()
        self.model_sql_device.select()
        self.model_sql_oid.select()
        
        msg = QtWidgets.QMessageBox.information(self, 'Успех', 'Запись удалена.')

    def change_model(self, row, record):
        self.model_sql_device.submitAll()
        self.model_sql_device.select()
        self.fill_combobox_devices()
        self.change_device()

    def add_device(self):
        r = self.model_sql_device.record()
        r.setValue("name", "")
        r.setValue("IP", "")
        self.model_sql_device.insertRecord(-1, r)
        self.model_sql_device.select()
        
        self.fill_combobox_devices()
 
    def change_device(self):
        self.model_sql_device.relationModel(3).select()
        self.fill_combobox_devices()

    def delete_device(self):
        row = self.table_device.currentIndex().row()
        if row == -1:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Выберите запись для удаления.')
            return          
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("Удалить запись ?")
        msg.setWindowTitle("Info")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        returnValue = msg.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            self.model_sql_device.removeRow(self.table_device.currentIndex().row())
            self.model_sql_device.select()

            msg = QtWidgets.QMessageBox.information(self, 'Успех', 'Запись удалена.')
        else:
            msg = QtWidgets.QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
            return
        self.fill_combobox_devices()

    def get_id_combobox_devices_device(self):
        list_keys = list(self.list_devices_device.keys())
        if (list_keys):
            return self.list_devices_device.get(list_keys[self.combobox_devices_device.currentIndex()])
        else:
            return None

    def get_id_combobox_ports_device(self):
        list_keys = list(self.list_devices_ports.keys())
        return self.list_devices_ports.get(list_keys[self.combobox_ports_device.currentIndex()])

    def settings_ports(self):
        number1 = self.combobox_from_port.currentIndex()
        number2 = self.combobox_to_port.currentIndex()

        if (number2 < number1):
            self.combobox_to_port.setCurrentIndex(number1)
            number2 = self.combobox_to_port.currentIndex()

        if (number1 == number2):
            device = Device(self.ip_device)
            if (device.is_combo_port(self.list_oids_device['Index Port'], self.combobox_from_port.currentText())):
                self.combobox_medium_type.clear()
                self.combobox_medium_type.addItems(['copper', 'fiber'])
        else:
            self.combobox_medium_type.clear()
            self.combobox_medium_type.addItems(['copper'])

    def setupUi(self, MainWindow):
        self.setObjectName("MainWindow")
        self.resize(876, 574)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_main = QtWidgets.QGridLayout()
        self.gridLayout_main.setObjectName("gridLayout_main")
        self.tab_devices_oids = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_devices_oids.setObjectName("tab_devices_oids")
        self.tab_devices = QtWidgets.QWidget()
        self.tab_devices.setObjectName("tab_devices")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_devices)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_21 = QtWidgets.QGridLayout()
        self.gridLayout_21.setObjectName("gridLayout_21")
        self.model_sql_device = QtSql.QSqlRelationalTableModel()
        self.model_sql_device.setEditStrategy(QtSql.QSqlRelationalTableModel.OnFieldChange)
        self.model_sql_device.setTable('Device')
        self.model_sql_device.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.model_sql_device.setHeaderData(2, QtCore.Qt.Horizontal, 'Наименование')
        self.model_sql_device.setHeaderData(3, QtCore.Qt.Horizontal, 'Модель')
        self.model_sql_device.setHeaderData(1, QtCore.Qt.Horizontal, 'IP')
        self.model_sql_device.setRelation(3, QtSql.QSqlRelation("Model", "id", "model_name"))
        self.model_sql_device.setJoinMode(
QtSql.QSqlRelationalTableModel.LeftJoin)
        self.model_sql_device.select()
        self.model_sql_device.dataChanged.connect(self.change_device)
        self.table_device = QtWidgets.QTableView(self.tab_devices)
        self.table_device.setObjectName("table_device")
        self.table_device.setModel(self.model_sql_device)
        self.table_device.setItemDelegate(
QtSql.QSqlRelationalDelegate(self.table_device))        
        self.table_device.horizontalHeader().setSectionResizeMode(
QtWidgets.QHeaderView.Stretch)
        self.table_device.setColumnHidden(0, True)

        self.gridLayout_21.addWidget(self.table_device, 1, 0, 1, 3)
        self.gridLayout_5.addLayout(self.gridLayout_21, 0, 0, 1, 1)

        self.tab_devices_oids.addTab(self.tab_devices, "")
        self.tab_oids = QtWidgets.QWidget()
        self.tab_oids.setObjectName("tab_oids")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_oids)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_tab22 = QtWidgets.QGridLayout()
        self.gridLayout_tab22.setObjectName("gridLayout_tab22")

        self.label_devices_device = QtWidgets.QLabel(self.tab_oids)
        self.label_devices_device.setObjectName("label_devices_device")
        self.gridLayout_tab22.addWidget(self.label_devices_device, 0, 0, 1, 1)
        
        self.combobox_devices_device = QtWidgets.QComboBox(self.tab_oids)
        self.combobox_devices_device.setObjectName("combobox_devices_device")
        self.gridLayout_tab22.addWidget(self.combobox_devices_device, 1, 0, 1, 1)
        self.combobox_devices_device.activated.connect(
self.signal_combobox_devices_device)

        self.model_sql_oid = TableModel()
        self.model_sql_oid.setTable('OIDs')
        self.model_sql_oid.select()
        self.model_sql_oid.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.model_sql_oid.setHeaderData(1, QtCore.Qt.Horizontal, 'Наименование')
        self.model_sql_oid.setHeaderData(2, QtCore.Qt.Horizontal, 'Значение')
        self.model_sql_oid.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.table_oids = QtWidgets.QTableView(self.tab_oids)
        self.table_oids.setObjectName("table_oids")
        
        self.table_oids.setModel(self.model_sql_oid)
        self.table_oids.horizontalHeader().setSectionResizeMode(
QtWidgets.QHeaderView.Stretch)
        self.table_oids.setColumnHidden(0, True)
        self.table_oids.setColumnHidden(1, True)
        self.table_oids.setColumnHidden(3, True)

        self.gridLayout_tab22.addWidget(self.table_oids, 2, 0, 1, 4)
        self.gridLayout.addLayout(self.gridLayout_tab22, 0, 0, 1, 1)
        self.tab_devices_oids.addTab(self.tab_oids, "")
        self.gridLayout_main.addWidget(self.tab_devices_oids, 2, 0, 1, 1)
        self.tab_ports = QtWidgets.QTabWidget(self.centralwidget)
        self.tab_ports.setObjectName("tab_ports")
        self.table_port_settings = QtWidgets.QWidget()
        self.table_port_settings.setObjectName("table_port_settings")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.table_port_settings)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_tab1 = QtWidgets.QGridLayout()
        self.gridLayout_tab1.setObjectName("gridLayout_tab1")        
        
        self.table_ports = QtWidgets.QTableWidget(self.table_port_settings)
        self.table_ports.setObjectName("table_ports")
        self.table_ports.setColumnCount(7)
        self.table_ports.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_ports.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_ports.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_ports.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_ports.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_ports.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_ports.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_ports.setHorizontalHeaderItem(6, item)
        self.table_ports.horizontalHeader().setSectionResizeMode(
QtWidgets.QHeaderView.Stretch)
        self.gridLayout_tab1.addWidget(self.table_ports, 4, 0, 1, 13)
        self.gridLayout_4.addLayout(self.gridLayout_tab1, 0, 0, 1, 1)
        self.tab_ports.addTab(self.table_port_settings, "")
        self.gridLayout_main.addWidget(self.tab_ports, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_main, 0, 0, 1, 1)
        self.setCentralWidget(self.centralwidget)

        self.button_delete_device = QtWidgets.QPushButton(self.tab_devices)
        self.button_delete_device.setObjectName("button_delete_device")
        self.gridLayout_21.addWidget(self.button_delete_device, 0, 1, 1, 1)
        self.button_delete_device.clicked.connect(self.delete_device)

        self.button_add_device = QtWidgets.QPushButton(self.tab_devices)
        self.button_add_device.setObjectName("button_add_device")
        self.gridLayout_21.addWidget(self.button_add_device, 0, 0, 1, 1)
        self.button_add_device.clicked.connect(self.add_device)

        self.button_apply = QtWidgets.QPushButton(self.table_port_settings)
        self.button_apply.setObjectName("button_apply")
        self.gridLayout_tab1.addWidget(self.button_apply, 2, 0, 1, 4)
        self.button_apply.clicked.connect(self.apply)

        self.button_refresh = QtWidgets.QPushButton(self.table_port_settings)
        self.button_refresh.setObjectName("button_refresh")
        self.gridLayout_tab1.addWidget(self.button_refresh, 2, 4, 1, 4)
        self.button_refresh.clicked.connect(self.refresh)

        self.label_ports_device = QtWidgets.QLabel(self.tab_ports)
        self.label_ports_device.setObjectName("label_deviceports_")
        self.gridLayout_tab1.addWidget(self.label_ports_device, 0, 0, 1, 1)
        
        self.combobox_ports_device = QtWidgets.QComboBox(self.tab_ports)
        self.combobox_ports_device.setObjectName("combobox_ports_device")
        self.combobox_ports_device.activated.connect(self.fill_ports)
        self.gridLayout_tab1.addWidget(self.combobox_ports_device, 1, 0, 1, 5)

        self.combobox_mdix = QtWidgets.QComboBox(self.table_port_settings)
        self.combobox_mdix.setObjectName("combobox_mdix")
        self.combobox_mdix.addItems(['auto', 'normal', 'cross'])
        self.gridLayout_tab1.addWidget(self.combobox_mdix, 1, 11, 1, 1)

        self.label_mdix = QtWidgets.QLabel(self.table_port_settings)
        self.label_mdix.setObjectName("label_mdix")
        self.gridLayout_tab1.addWidget(self.label_mdix, 0, 11, 1, 1)

        self.combobox_medium_type = QtWidgets.QComboBox(self.table_port_settings)
        self.combobox_medium_type.setObjectName("combobox_medium_type")
        self.gridLayout_tab1.addWidget(self.combobox_medium_type, 1, 12, 1, 1)
        self.combobox_medium_type.addItems(['copper'])

        self.label_mediu_type = QtWidgets.QLabel(self.table_port_settings)
        self.label_mediu_type.setObjectName("label_mediu_type")
        self.gridLayout_tab1.addWidget(self.label_mediu_type, 0, 12, 1, 1)

        self.combobox_from_port = QtWidgets.QComboBox(self.table_port_settings)
        self.combobox_from_port.setObjectName("combobox_from_port")
        self.combobox_from_port.activated.connect(self.settings_ports)
        self.gridLayout_tab1.addWidget(self.combobox_from_port, 1, 5, 1, 1)

        self.label_from_port = QtWidgets.QLabel(self.table_port_settings)
        self.label_from_port.setObjectName("label_from_port")
        self.gridLayout_tab1.addWidget(self.label_from_port, 0, 5, 1, 1)

        self.combobox_flow_control = QtWidgets.QComboBox(self.table_port_settings)
        self.combobox_flow_control.setObjectName("combobox_flow_control")
        self.gridLayout_tab1.addWidget(self.combobox_flow_control, 1, 9, 1, 1)
        self.combobox_flow_control.addItems(['Enabled', 'Disabled'])

        self.label_flow_control = QtWidgets.QLabel(self.table_port_settings)
        self.label_flow_control.setObjectName("label_flow_control")
        self.gridLayout_tab1.addWidget(self.label_flow_control, 0, 9, 1, 1)

        self.combobox_address_learning = QtWidgets.QComboBox(self.table_port_settings)

        self.combobox_address_learning.setObjectName(
"combobox_address_learning")
        self.gridLayout_tab1.addWidget(self.combobox_address_learning, 1, 10, 1, 1)
        self.combobox_address_learning.addItems(['Enabled', 'Disabled'])

        self.label_address_learning = QtWidgets.QLabel(self.table_port_settings)
        self.label_address_learning.setObjectName("label_address_learning")
        self.gridLayout_tab1.addWidget(self.label_address_learning, 0, 10, 1, 1)

        self.combobox_to_port = QtWidgets.QComboBox(self.table_port_settings)
        self.combobox_to_port.setObjectName("combobox_to_port")
        self.combobox_to_port.activated.connect(self.settings_ports)
        self.gridLayout_tab1.addWidget(self.combobox_to_port, 1, 6, 1, 1)

        self.label_to_port = QtWidgets.QLabel(self.table_port_settings)
        self.label_to_port.setObjectName("label_to_port")
        self.gridLayout_tab1.addWidget(self.label_to_port, 0, 6, 1, 1)

        self.combobox_speed = QtWidgets.QComboBox(self.table_port_settings)
        self.combobox_speed.setObjectName("combobox_speed")
        self.gridLayout_tab1.addWidget(self.combobox_speed, 1, 7, 1, 1)
        self.combobox_speed.addItems(['nway-enabled', 'nway-disabled-10Mbps-Half', 'nway-disabled-10Mbps-Full', 'nway-disabled-100Mbps-Half',
            'nway-disabled-100Mbps-Full', 'nway-disabled-1Gigabps-Half', ' nway-disabled-1Gigabps-Full', 'nway-disabled-1Gigabps-Full-master',
            'nway-disabled-1Gigabps-Full-slave'])

        self.label_speed = QtWidgets.QLabel(self.table_port_settings)
        self.label_speed.setObjectName("label_speed")
        self.gridLayout_tab1.addWidget(self.label_speed, 0, 7, 1, 1)

        self.combobox_state = QtWidgets.QComboBox(self.table_port_settings)
        self.combobox_state.setObjectName("combobox_state")
        self.gridLayout_tab1.addWidget(self.combobox_state, 1, 8, 1, 1)
        self.combobox_state.addItems(['Enabled', 'Disabled'])

        self.label_state = QtWidgets.QLabel(self.table_port_settings)
        self.label_state.setObjectName("label_state")
        self.gridLayout_tab1.addWidget(self.label_state, 0, 8, 1, 1)

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_2.clicked.connect(self.delete_model)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)

        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.add_model)
        self.gridLayout_2.addWidget(self.pushButton_3, 0, 0, 1, 1)

        self.model_sql_models = QtSql.QSqlTableModel(self)
        self.model_sql_models.setTable('Model')
        self.model_sql_models.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.model_sql_models.setHeaderData(1, QtCore.Qt.Horizontal, 'Наименование')
        self.model_sql_models.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.model_sql_models.dataChanged.connect(self.change_model)
        self.model_sql_models.select()
        self.table_models = QtWidgets.QTableView(self.tab)
        self.table_models.setObjectName("table_models")
        self.table_models.setModel(self.model_sql_models)
        
        self.gridLayout_2.addWidget(self.table_models, 1, 0, 1, 3)
        self.table_models.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_models.setColumnHidden(0, True)
        
        
        self.gridLayout_6.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.tab_devices_oids.addTab(self.tab, "")
        
        self.retranslateUi(MainWindow)
        self.tab_devices_oids.setCurrentIndex(0)
        self.tab_ports.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Управление коммутационным оборудованием"))
        self.label_ports_device.setText(_translate("MainWindow", "Устройство"))
        self.button_delete_device.setText(_translate("MainWindow", "-"))
        self.button_add_device.setText(_translate("MainWindow", "+"))

        self.tab_devices_oids.setTabText(self.tab_devices_oids.indexOf(self.tab_devices), _translate("MainWindow", "Список устройств"))
        self.label_devices_device.setText(_translate("MainWindow", "Модель"))
        self.tab_devices_oids.setTabText(self.tab_devices_oids.indexOf(
self.tab_oids), _translate("MainWindow", "oids"))
        self.label_address_learning.setText(_translate("MainWindow", "Address Learning"))
        self.label_state.setText(_translate("MainWindow", "State"))
        self.label_flow_control.setText(_translate("MainWindow", "Flow Control"))
        self.label_speed.setText(_translate("MainWindow", "Speed/Duplexl"))
        self.label_from_port.setText(_translate("MainWindow", "From Port"))
        self.label_to_port.setText(_translate("MainWindow", "To Port"))

        self.label_mediu_type.setText(_translate("MainWindow", "Medium Type"))
        self.label_mdix.setText(_translate("MainWindow", "MDIX"))
        self.button_apply.setText(_translate("MainWindow", "Apply"))
        self.button_refresh.setText(_translate("MainWindow", "Refresh"))
        item = self.table_ports.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Port"))
        item = self.table_ports.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "State"))
        item = self.table_ports.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Speed/Duplex"))
        item = self.table_ports.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Flow Control"))
        item = self.table_ports.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Connection"))
        item = self.table_ports.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "MDIX"))
        item = self.table_ports.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Address Learning"))
        self.pushButton_2.setText(_translate("MainWindow", "-"))
        self.pushButton_3.setText(_translate("MainWindow", "+"))
        self.tab_devices_oids.setTabText(self.tab_devices_oids.indexOf(self.tab), _translate("MainWindow", "Список моделей"))
        self.tab_ports.setTabText(self.tab_ports.indexOf(self.table_port_settings), _translate("MainWindow", "Port Settings"))

    def signal_combobox_devices_device(self):
        fil = self.get_id_combobox_devices_device()
        if (fil):
            self.model_sql_oid.setFilter("id_model = {}".format(fil))
        self.fill_oids()
     
if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()






                                            





