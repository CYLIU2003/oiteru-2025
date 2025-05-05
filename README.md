# オイテル登録システム (Oiteru Registration System)

This project provides two implementations of the *Oiteru Registration System* for managing student IC card registrations and usage tracking at Tokyo City University (都市大) in collaboration with the Tokyu Group:

1. **Desktop GUI Application** (`home20250506.py`) – A modernized Tkinter-based application with improved UI/UX.
2. **Web Application** (`app20250506.py` using Flask) – A web-based interface with equivalent functionality.

Both implementations connect to the same backend database (`mydb2025.py`) without modifications, ensuring consistent data management.

## Features

- **IC Card Registration:** Register a student’s IC card by tapping it on an NFC reader. The system adds new users to the database and prevents duplicate registrations.
- **Usage Status Check:** Quickly check a user's remaining usage count and status by tapping their IC card.
- **Admin Dashboard:** Accessible with a password, allows:
  - Viewing and managing all registered users (edit card IDs, adjust usage counts, enable/disable usage, or delete users).
  - Viewing and managing all child devices (edit stock and availability, register new devices).
  - Viewing the usage history log.
  - Changing system settings (admin password, usage count retention limits, frequency of usage increment).
  - Data backup to Excel and restoration from backup.
- **Design and Branding:** The UI incorporates **Tokyo City University** and **Tokyu Group** branding – including the university’s logo and its signature blue color – to create a modern, polished look.

## Installation

1. **Prerequisites:**
   - Python 3.x installed.
   - MySQL server running with a database named `userdb` (the app will create tables if not present). Update `mydb2025.py` connection details if necessary (currently uses user `root` with password `Hiramekigo@1` on `localhost`).
   - An NFC reader supported by [nfcpy](https://nfcpy.readthedocs.io/) for card operations.
   - Recommended: a virtual environment for Python.

2. **Install Python dependencies:**
pip install -r requirements.txt
This installs Flask, openpyxl, pandas, mysql-connector-python, nfcpy, etc.

3. **Database Setup:**
Ensure MySQL is running. The first run of the app will call `mydb.set_up()` to create required tables. You may manually run `mydb2025.py` or the applications to initialize the database. The default admin password is **`test1`** (set in the `info` table by `make_info()`).

4. **Static Files:**
- Place the Tokyo City University logo image in `static/img/logo20250506.png` (the image is provided in the repository). This is used by both applications (embedded in the GUI and referenced in the web UI).

## Running the Desktop Application

Run the Tkinter GUI by executing:

python home20250506.py
markdown
复制代码

**Usage:**
- A window will appear with the title “オイテル登録システム” and the Tokyo City University logo.
- **学生証を登録する:** Click this and then tap a student ID card on the NFC reader. A message will confirm registration, or alert if the card is already registered or if there was a read error.
- **利用状況の確認:** Click this and tap a card to view that card’s status (remaining uses, etc.). Information will display for a few seconds.
- **詳細設定を開く (管理者):** Click this to go to the admin login. Enter the admin password (default **test1**). On success, the detailed admin menu is shown:
  - **利用者一覧:** Shows all users. Select a user and click **選択ユーザー詳細** to edit that user’s info.
  - **子機一覧:** Shows all registered devices. Select one and click **選択子機詳細** to edit its info.
  - **新規子機の登録:** Opens a form to add a new device.
  - **利用履歴:** Displays logged usage events.
  - **システム設定:** Allows changing the admin password, the “保持上限” (max usage stock per user), and “増加日数” (days required to regain one usage). It also provides buttons for **データバックアップ** (export database to Excel `backup.xlsx`) and **バックアップから復元** (import from `backup.xlsx`).

- **Exit:** Close the window to exit the application. The app automatically performs periodic backups and resets daily usage counts every 24 hours.

## Running the Web Application

Start the Flask web server:

python app20250506.py
markdown


By default, it runs on `http://127.0.0.1:5000/`. Access this URL in a web browser.

**Usage:**
- **Home Page:** Presents two main actions:
  - *Register Student ID Card* – Navigates to the card registration page.
  - *Check Usage Status* – Navigates to the usage check page.
- **Card Registration (`/register`):** Click **ICカードを登録** and then tap the card. You will receive a success message or error on the same page.
- **Usage Check (`/usage`):** Click **利用状況を確認** and tap the card. The page will display the card’s status (ID, allowed/blocked, registration date, remaining uses, and days until next usage increment if applicable).
- **Admin Login (`/admin`):** Enter the admin password to log in.
- **Admin Dashboard (`/admin/dashboard`):** Provides navigation:
  - *利用者一覧* – List of users (`/admin/users`). Click a user ID to view/edit.
  - *子機一覧* – List of devices (`/admin/units`). Click a device ID to view/edit.
  - *利用履歴* – Complete history log (`/admin/history`).
  - *データバックアップ* – Triggers download of `backup.xlsx`.
  - *データ復元* – Upload an Excel file to restore data.
  - *ログアウト* – End admin session.
- **Edit User (`/admin/user/<id>`):** Change card ID, allow flag, or remaining uses. Submit to save. (Leaving the card ID blank and submitting will delete the user.)
- **Edit Unit (`/admin/unit/<id>`):** Change the stock or availability of a device. Submit to save.
- **Add Unit (`/admin/unit/new`):** Form to add a new device (name, password, initial stock, availability).
- **History (`/admin/history`):** Lists each history record (timestamp and event).
- **Restore (`/admin/restore`):** Upload a `backup.xlsx` file and submit to restore the database from it.

**Design:** The web UI features a header with the **Tokyo City University logo** and system title on every page. The primary color theme is a **bright sky blue** (`#26A8DF`) representing the university’s brand, used in buttons and highlights. The layout is responsive and minimalist:
- Buttons and links are styled for clarity and a modern look.
- Data tables for users and units have striped rows and colored headers.
- Flash messages provide feedback for user actions (e.g., success or error notifications).

## Repository Structure

├── home20250506.py # Desktop GUI application script
├── app20250506.py # Flask web application script
├── mydb2025.py # Database interface module (unchanged from original)
├── requirements.txt # Python dependencies
├── README.md # Documentation (this file)
├── static/
│ ├── css/
│ │ └── style20250506.css # CSS styling for the web app
│ └── img/
│ └── logo20250506.png # Tokyo City University logo image
└── templates/
├── base.html
├── index.html
├── register.html
├── usage.html
├── usage_status.html
├── admin_login.html
├── admin_dashboard.html
├── admin_users.html
├── admin_user_detail.html
├── admin_units.html
├── admin_unit_detail.html
├── admin_new_unit.html
├── admin_history.html
└── admin_restore.html
pgsql


## Notes

- Ensure the NFC reader is connected and recognized by nfcpy for card operations. If testing without hardware, you may need to simulate or stub the `mydb.do()` and `mydb.id_do()` functions.
- The system uses Japanese text for the UI labels and messages, consistent with the original application context.
- Before running the web app on a server, set an appropriate secret key and consider HTTPS for secure password transmission if deployed in production.
- Both applications maintain the same logical flow and constraints as the original system (for example, the admin password is stored in the database and the usage count auto-increments are governed by `dayupdate()` in `mydb2025.py`).

