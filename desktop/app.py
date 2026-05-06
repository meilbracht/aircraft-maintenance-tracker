import sys
import os
import pandas as pd

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFileDialog, QTableWidget, QTableWidgetItem, QMessageBox,
    QLineEdit, QComboBox, QDialog, QFormLayout, QDialogButtonBox,
    QFrame
)

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


COLUMNS = [
    "date",
    "shift",
    "A/C",
    "location",
    "discrepancy",
    "maintenance action",
    "JCN / Document Number",
    "Log Entered By",
    "Shift Lead",
    "Technicians"
]

DATA_FILE = "../data/saved_data.csv"


class RecordDialog(QDialog):
    def __init__(self, existing_data=None):
        super().__init__()
        self.setWindowTitle("Maintenance Record")
        self.setMinimumWidth(500)

        self.fields = {
            "date": QLineEdit(),
            "shift": QComboBox(),
            "A/C": QLineEdit(),
            "location": QLineEdit(),
            "discrepancy": QLineEdit(),
            "maintenance action": QLineEdit(),
            "JCN / Document Number": QLineEdit(),
            "Log Entered By": QLineEdit(),
            "Shift Lead": QLineEdit(),
            "Technicians": QLineEdit(),
        }

        self.fields["shift"].addItems(["Day", "Night"])

        layout = QFormLayout()

        for label, widget in self.fields.items():
            layout.addRow(label, widget)

        if existing_data is not None:
            for key, value in existing_data.items():
                if key in self.fields:
                    widget = self.fields[key]
                    if isinstance(widget, QComboBox):
                        index = widget.findText(str(value))
                        if index >= 0:
                            widget.setCurrentIndex(index)
                    else:
                        widget.setText(str(value))

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_data(self):
        data = {}

        for key, widget in self.fields.items():
            if isinstance(widget, QComboBox):
                data[key] = widget.currentText()
            else:
                data[key] = widget.text()

        return data


class MaintenanceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aircraft Maintenance Tracking System")
        self.resize(1300, 750)

        self.dataframe = pd.DataFrame(columns=COLUMNS)
        self.filtered_df = self.dataframe.copy()

        self.load_saved_data()
        self.build_ui()
        self.apply_styles()
        self.apply_filters()
        self.update_dashboard()

    def load_saved_data(self):
        try:
            if os.path.exists(DATA_FILE):
                saved_df = pd.read_csv(DATA_FILE)

                for col in COLUMNS:
                    if col not in saved_df.columns:
                        saved_df[col] = ""

                self.dataframe = saved_df[COLUMNS]
                self.filtered_df = self.dataframe.copy()
        except Exception as e:
            print(f"Could not load saved data: {e}")

    def save_data(self):
        try:
            os.makedirs("../data", exist_ok=True)
            self.dataframe.to_csv(DATA_FILE, index=False)
        except Exception as e:
            QMessageBox.warning(self, "Save Error", f"Could not save data:\n{e}")

    def build_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(24, 24, 24, 24)
        self.setLayout(main_layout)

        title = QLabel("Aircraft Maintenance Tracking System")
        title.setObjectName("titleLabel")
        main_layout.addWidget(title)

        subtitle = QLabel("Maintenance log management, reporting, and operational visibility")
        subtitle.setObjectName("subtitleLabel")
        main_layout.addWidget(subtitle)

        dashboard_layout = QHBoxLayout()

        self.total_card = self.create_card("Total Logs", "0")
        self.day_card = self.create_card("Day Shift", "0")
        self.night_card = self.create_card("Night Shift", "0")
        self.filtered_card = self.create_card("Displayed Records", "0")

        dashboard_layout.addWidget(self.total_card)
        dashboard_layout.addWidget(self.day_card)
        dashboard_layout.addWidget(self.night_card)
        dashboard_layout.addWidget(self.filtered_card)

        main_layout.addLayout(dashboard_layout)

        tools_frame = QFrame()
        tools_frame.setObjectName("toolsFrame")
        tools_layout = QVBoxLayout()
        tools_layout.setSpacing(10)
        tools_frame.setLayout(tools_layout)

        search_filter_layout = QHBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "Search aircraft, discrepancy, location, technician, or JCN..."
        )
        self.search_box.textChanged.connect(self.apply_filters)
        search_filter_layout.addWidget(self.search_box, 3)

        self.shift_filter = QComboBox()
        self.shift_filter.addItems(["All Shifts", "Day", "Night"])
        self.shift_filter.currentTextChanged.connect(self.apply_filters)
        search_filter_layout.addWidget(self.shift_filter, 1)

        tools_layout.addLayout(search_filter_layout)

        button_layout = QHBoxLayout()

        self.import_button = QPushButton("Import Logs")
        self.import_button.clicked.connect(self.import_excel)
        button_layout.addWidget(self.import_button)

        self.add_button = QPushButton("Add Record")
        self.add_button.clicked.connect(self.add_record)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Edit Selected")
        self.edit_button.clicked.connect(self.edit_selected)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_selected)
        button_layout.addWidget(self.delete_button)

        self.export_csv_button = QPushButton("Export CSV")
        self.export_csv_button.clicked.connect(self.export_csv)
        button_layout.addWidget(self.export_csv_button)

        self.export_pdf_button = QPushButton("Export PDF")
        self.export_pdf_button.clicked.connect(self.export_pdf)
        button_layout.addWidget(self.export_pdf_button)

        tools_layout.addLayout(button_layout)
        main_layout.addWidget(tools_frame)

        self.status_label = QLabel("System Status: Ready")
        self.status_label.setObjectName("statusLabel")
        main_layout.addWidget(self.status_label)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setSortingEnabled(True)
        main_layout.addWidget(self.table)

        self.load_table(self.filtered_df)

    def create_card(self, title, value):
        frame = QFrame()
        frame.setObjectName("dashboardCard")

        layout = QVBoxLayout()
        frame.setLayout(layout)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        value_label = QLabel(value)
        value_label.setObjectName("cardValue")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        frame.value_label = value_label
        return frame

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #e5e7eb;
                font-family: Segoe UI;
                font-size: 13px;
            }

            #titleLabel {
                font-size: 28px;
                font-weight: 700;
                color: #f8fafc;
            }

            #subtitleLabel {
                font-size: 14px;
                color: #94a3b8;
                margin-bottom: 8px;
            }

            #dashboardCard {
                background-color: #1e293b;
                border: 1px solid #334155;
                border-radius: 14px;
                padding: 12px;
            }

            #cardTitle {
                color: #94a3b8;
                font-size: 13px;
            }

            #cardValue {
                color: #38bdf8;
                font-size: 26px;
                font-weight: 700;
            }

            #toolsFrame {
                background-color: #111827;
                border: 1px solid #334155;
                border-radius: 14px;
                padding: 12px;
            }

            QLineEdit, QComboBox {
                background-color: #020617;
                color: #e5e7eb;
                border: 1px solid #475569;
                border-radius: 8px;
                padding: 8px;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #38bdf8;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 9px 14px;
                font-weight: 600;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }

            QPushButton:pressed {
                background-color: #1e40af;
            }

            QTableWidget {
                background-color: #020617;
                alternate-background-color: #111827;
                color: #e5e7eb;
                border: 1px solid #334155;
                border-radius: 10px;
                gridline-color: #334155;
            }

            QHeaderView::section {
                background-color: #1e293b;
                color: #f8fafc;
                padding: 8px;
                border: 1px solid #334155;
                font-weight: bold;
            }

            QTableWidget::item:selected {
                background-color: #2563eb;
                color: white;
            }

            #statusLabel {
                color: #22c55e;
                font-weight: 600;
            }

            QDialog {
                background-color: #0f172a;
            }

            QLabel {
                color: #e5e7eb;
            }
        """)

    def import_excel(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Excel File",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if file_name:
            try:
                imported_df = pd.read_excel(file_name)

                for col in COLUMNS:
                    if col not in imported_df.columns:
                        imported_df[col] = ""

                self.dataframe = imported_df[COLUMNS]
                self.save_data()
                self.apply_filters()
                self.status_label.setText("System Status: Maintenance logs imported successfully")
                QMessageBox.information(self, "Success", "Maintenance logs imported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Import failed:\n{e}")

    def load_table(self, df):
        self.table.setSortingEnabled(False)

        self.table.setRowCount(len(df))
        self.table.setColumnCount(len(df.columns))
        self.table.setHorizontalHeaderLabels(df.columns.tolist())

        for row in range(len(df)):
            for col in range(len(df.columns)):
                item = QTableWidgetItem(str(df.iat[row, col]))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

    def update_dashboard(self):
        total_logs = len(self.dataframe)

        day_count = 0
        night_count = 0

        if "shift" in self.dataframe.columns:
            day_count = (
                self.dataframe["shift"].astype(str).str.lower() == "day"
            ).sum()
            night_count = (
                self.dataframe["shift"].astype(str).str.lower() == "night"
            ).sum()

        displayed_records = len(self.filtered_df)

        self.total_card.value_label.setText(str(total_logs))
        self.day_card.value_label.setText(str(day_count))
        self.night_card.value_label.setText(str(night_count))
        self.filtered_card.value_label.setText(str(displayed_records))

    def apply_filters(self):
        df = self.dataframe.copy()

        search_text = self.search_box.text().strip().lower()
        selected_shift = self.shift_filter.currentText()

        if selected_shift != "All Shifts":
            df = df[df["shift"].astype(str).str.lower() == selected_shift.lower()]

        if search_text:
            df = df[
                df.apply(
                    lambda row: search_text in " ".join(row.astype(str)).lower(),
                    axis=1
                )
            ]

        self.filtered_df = df
        self.load_table(self.filtered_df)
        self.update_dashboard()

    def add_record(self):
        dialog = RecordDialog()

        if dialog.exec():
            new_data = dialog.get_data()
            new_row = pd.DataFrame([new_data])

            self.dataframe = pd.concat([self.dataframe, new_row], ignore_index=True)

            self.save_data()
            self.apply_filters()
            self.status_label.setText("System Status: New maintenance record added")
            QMessageBox.information(self, "Success", "New maintenance record added.")

    def edit_selected(self):
        selected_row = self.table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a record to edit.")
            return

        if self.filtered_df.empty:
            QMessageBox.warning(self, "Warning", "No record available to edit.")
            return

        original_index = self.filtered_df.index[selected_row]
        existing_data = self.dataframe.loc[original_index].to_dict()

        dialog = RecordDialog(existing_data)

        if dialog.exec():
            updated_data = dialog.get_data()

            for key, value in updated_data.items():
                self.dataframe.at[original_index, key] = value

            self.save_data()
            self.apply_filters()
            self.status_label.setText("System Status: Selected maintenance record updated")
            QMessageBox.information(self, "Success", "Maintenance record updated successfully.")

    def delete_selected(self):
        selected_row = self.table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a record to delete.")
            return

        if self.filtered_df.empty:
            QMessageBox.warning(self, "Warning", "No record available to delete.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete the selected maintenance record?"
        )

        if confirm == QMessageBox.Yes:
            original_index = self.filtered_df.index[selected_row]
            self.dataframe = self.dataframe.drop(original_index).reset_index(drop=True)

            self.save_data()
            self.apply_filters()
            self.status_label.setText("System Status: Selected maintenance record deleted")
            QMessageBox.information(self, "Success", "Selected record deleted.")

    def export_csv(self):
        if self.filtered_df.empty:
            QMessageBox.warning(self, "Warning", "No data to export.")
            return

        os.makedirs("../exports", exist_ok=True)
        path = "../exports/maintenance_export.csv"

        self.filtered_df.to_csv(path, index=False)

        self.status_label.setText("System Status: CSV report exported")
        QMessageBox.information(self, "Success", f"CSV exported to:\n{path}")

    def export_pdf(self):
        if self.filtered_df.empty:
            QMessageBox.warning(self, "Warning", "No data to export.")
            return

        os.makedirs("../exports", exist_ok=True)
        path = "../exports/maintenance_report.pdf"

        c = canvas.Canvas(path, pagesize=letter)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "Aircraft Maintenance Report")

        c.setFont("Helvetica", 8)
        y = 720

        headers = list(self.filtered_df.columns)

        for i, col in enumerate(headers[:5]):
            c.drawString(50 + i * 100, y, str(col))

        y -= 20

        for _, row in self.filtered_df.head(15).iterrows():
            for i, value in enumerate(row[:5]):
                c.drawString(50 + i * 100, y, str(value)[:18])

            y -= 20

            if y < 50:
                c.showPage()
                y = 750

        c.save()

        self.status_label.setText("System Status: PDF report exported")
        QMessageBox.information(self, "Success", f"PDF exported to:\n{path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MaintenanceApp()
    window.show()
    sys.exit(app.exec())