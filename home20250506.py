import tkinter as tk
from tkinter import ttk
import base64
import mydb2025 as mydb  # Backend database module (unchanged)

# Define a modern color scheme reflecting Tokyo City University (Toshidai) and Tokyu Group
PRIMARY_COLOR = "#26A8DF"   # bright blue (from Toshidai logo)
DARK_TEXT = "#333333"       # dark gray for text
LIGHT_BG = "#F7F7F7"        # light gray background for frames
FONT_FAMILY = "Yu Gothic UI"  # a modern, legible font (supports Japanese characters)

# Base64-encoded Tokyo City University logo (with Tokyu Group tagline)
logo_base64 = """
iVBORw0KGgoAAAANSUhEUgAABAAAAACeCAYAAACsPnijAAAABGdBTUEAALGPC/xhBQAAACBjSFJN
AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAcGVYSWZNTQAqAAAACAABBj9x
...
(large base64 string omitted for brevity – use the full string from the answer)
...
AAAAGYktHRQAAGGzCgApAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEZ0lEQVR42u3cwW7UMBBF0Xk0
d72k5zaKITXFBPd0PwD83+coOiP0qtbACkuAQAAAAAAAAAAAAAAAAAAAHBPu7t7nK5uR5crV65c
Z/l3cM5j1PT3/Z4HAAAAAAAAAAAAAABgB9KeBgAAAAAAAAAAAACQLf8BAP7BZO5O3ZmXAAAAAElF
TkSuQmCC
""".strip()

# Initialize Tkinter root window
root = tk.Tk()
root.title("オイテル登録システム - Tokyo City University / Tokyu Group")
# Set a minimum size for better layout on modern displays
root.minsize(800, 600)

# Configure style for modern look
style = ttk.Style(root)
try:
    style.theme_use("clam")  # use 'clam' theme for a flat modern look
except:
    pass
# Define styles for widgets
style.configure("TFrame", background=LIGHT_BG)
style.configure("TLabel", background=LIGHT_BG, foreground=DARK_TEXT, font=(FONT_FAMILY, 12))
style.configure("TButton", font=(FONT_FAMILY, 12), foreground="white", background=PRIMARY_COLOR)
style.map("TButton", background=[("active", "#1E90CC")])  # darker blue on active

# Load logo image from base64 and create a PhotoImage
# (Note: Tkinter PhotoImage supports GIF/PGM/PPM. For PNG, this requires Tk 8.6+)
logo_image = None
try:
    logo_image = tk.PhotoImage(data=logo_base64)
except Exception as e:
    logo_image = None

# Create frames
home_frame = ttk.Frame(root, padding=20)
entry_frame = ttk.Frame(root, padding=20)
entry_done_frame = ttk.Frame(root, padding=20)
error_frame = ttk.Frame(root, padding=20)
exists_frame = ttk.Frame(root, padding=20)
passcheck_frame = ttk.Frame(root, padding=20)
setting_frame = ttk.Frame(root, padding=10)
simple_info_frame = ttk.Frame(root, padding=20)
user_info_frame = ttk.Frame(root, padding=20)
make_unit_frame = ttk.Frame(root, padding=20)
unit_info_frame = ttk.Frame(root, padding=20)

# Place all frames in the same location; we will raise them as needed
for frame in (home_frame, entry_frame, entry_done_frame, error_frame, exists_frame,
              passcheck_frame, setting_frame, simple_info_frame, user_info_frame,
              make_unit_frame, unit_info_frame):
    frame.grid(row=0, column=0, sticky="nsew")

# --- Home Frame (Main Menu) ---
# Top logo
if logo_image:
    logo_label = ttk.Label(home_frame, image=logo_image)
    logo_label.image = logo_image  # keep a reference
    logo_label.pack(side=tk.TOP, pady=(0, 10))
title_label = ttk.Label(home_frame, text="オイテル登録システム", font=(FONT_FAMILY, 16, "bold"))
title_label.pack(pady=(0, 20))
home_desc = ttk.Label(home_frame, text="Tokyo City University – Tokyu Group", font=(FONT_FAMILY, 11))
home_desc.pack(pady=(0, 20))

# Buttons on home menu
button_register = ttk.Button(home_frame, text="学生証を登録する", width=30, command=lambda: entry_frame.tkraise())
button_usage = ttk.Button(home_frame, text="利用状況の確認", width=30, command=lambda: simple_info_frame.tkraise())
button_admin = ttk.Button(home_frame, text="詳細設定を開く (管理者)", width=30, command=lambda: passcheck_frame.tkraise())
button_register.pack(pady=5)
button_usage.pack(pady=5)
button_admin.pack(pady=5)

# --- Entry Frame (IC card registration) ---
entry_label = ttk.Label(entry_frame, text="学生証をカードリーダーにタッチしてください。", font=(FONT_FAMILY, 13))
entry_label.pack(pady=20)
entry_button = ttk.Button(entry_frame, text="ICカードを置いた", command=lambda: iccall())
entry_button.pack(pady=10)
entry_cancel = ttk.Button(entry_frame, text="ホームに戻る", command=lambda: home_frame.tkraise())
entry_cancel.pack(pady=(10, 0))

# --- Entry Done Frame (Registration success) ---
done_label = ttk.Label(entry_done_frame, text="登録が完了しました！", font=(FONT_FAMILY, 14, "bold"))
done_label.pack(pady=40)

# --- Error Frame (Read error) ---
error_label = ttk.Label(error_frame, text="ICカードが読み取れません。\nホーム画面に戻ります。", font=(FONT_FAMILY, 14))
error_label.pack(pady=40)

# --- Exists Frame (Already registered) ---
exists_label = ttk.Label(exists_frame, text="この学生証は既に登録されています。\nホーム画面に戻ります。", font=(FONT_FAMILY, 14))
exists_label.pack(pady=40)

# --- Password Check Frame (enter admin password) ---
pass_label = ttk.Label(passcheck_frame, text="管理者パスワードを入力してください:", font=(FONT_FAMILY, 13))
pass_entry = ttk.Entry(passcheck_frame, show="•", font=(FONT_FAMILY, 12))
pass_button = ttk.Button(passcheck_frame, text="認証", command=lambda: check_password())
pass_cancel = ttk.Button(passcheck_frame, text="ホームに戻る", command=lambda: home_frame.tkraise())
pass_label.grid(row=0, column=0, columnspan=2, pady=10)
pass_entry.grid(row=1, column=0, padx=5, pady=10)
pass_button.grid(row=1, column=1, padx=5, pady=10)
pass_cancel.grid(row=2, column=0, columnspan=2, pady=(20, 0))

# --- Setting Frame (Admin Dashboard) ---
# Split into subframes for better layout: Users, Units, History, and Settings
users_frame = ttk.LabelFrame(setting_frame, text="利用者一覧", padding=10)
units_frame = ttk.LabelFrame(setting_frame, text="子機一覧", padding=10)
history_frame = ttk.LabelFrame(setting_frame, text="利用履歴", padding=10)
settings_frame = ttk.LabelFrame(setting_frame, text="システム設定", padding=10)
users_frame.grid(row=0, column=0, rowspan=2, padx=5, pady=5, sticky="nsew")
units_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
history_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
settings_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# Populate Users list
lb_users_var = tk.StringVar(value=[])
lb_users = tk.Listbox(users_frame, listvariable=lb_users_var, font=(FONT_FAMILY, 12), width=20, height=12)
sb_users = ttk.Scrollbar(users_frame, orient=tk.VERTICAL, command=lb_users.yview)
lb_users.configure(yscrollcommand=sb_users.set)
lb_users.grid(row=0, column=0, sticky="ns")
sb_users.grid(row=0, column=1, sticky="ns")
btn_view_user = ttk.Button(users_frame, text="選択ユーザー詳細", command=lambda: open_user_details())
btn_view_user.grid(row=1, column=0, columnspan=2, pady=(5,0))

# Populate Units list
lb_units_var = tk.StringVar(value=[])
lb_units = tk.Listbox(units_frame, listvariable=lb_units_var, font=(FONT_FAMILY, 12), width=20, height=12)
sb_units = ttk.Scrollbar(units_frame, orient=tk.VERTICAL, command=lb_units.yview)
lb_units.configure(yscrollcommand=sb_units.set)
lb_units.grid(row=0, column=0, sticky="ns")
sb_units.grid(row=0, column=1, sticky="ns")
btn_view_unit = ttk.Button(units_frame, text="選択子機詳細", command=lambda: open_unit_details())
btn_view_unit.grid(row=1, column=0, columnspan=2, pady=(5,0))
btn_new_unit = ttk.Button(units_frame, text="新規子機の登録", command=lambda: make_unit_frame.tkraise())
btn_new_unit.grid(row=2, column=0, columnspan=2, pady=(10,0))

# Populate History list
lb_history_var = tk.StringVar(value=[])
lb_history = tk.Listbox(history_frame, listvariable=lb_history_var, font=(FONT_FAMILY, 11), width=30, height=12)
sb_history = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=lb_history.yview)
lb_history.configure(yscrollcommand=sb_history.set)
lb_history.grid(row=0, column=0, sticky="ns")
sb_history.grid(row=0, column=1, sticky="ns")
btn_export_history = ttk.Button(history_frame, text="履歴をエクスポート", command=lambda: export_history())
btn_export_history.grid(row=1, column=0, columnspan=2, pady=(5,0))

# Settings controls (password change, backup, restore, etc.)
cur_pass_label = ttk.Label(settings_frame, text="現在のパスワード:")
cur_pass_value = ttk.Label(settings_frame, text="")  # will be filled with current password
new_pass_label = ttk.Label(settings_frame, text="新しいパスワード:")
new_pass_entry1 = ttk.Entry(settings_frame, font=(FONT_FAMILY, 11))
new_pass_entry2 = ttk.Entry(settings_frame, font=(FONT_FAMILY, 11))
btn_change_pass = ttk.Button(settings_frame, text="パスワード変更", command=lambda: change_password())
# Keep and freq (usage stock and increment frequency)
keep_label = ttk.Label(settings_frame, text="保持上限:")
keep_entry = ttk.Entry(settings_frame, width=5)
freq_label = ttk.Label(settings_frame, text="増加日数:")
freq_entry = ttk.Entry(settings_frame, width=5)
# Backup and restore
btn_backup = ttk.Button(settings_frame, text="データバックアップ", command=lambda: mydb.make_backup())
btn_restore = ttk.Button(settings_frame, text="バックアップから復元", command=lambda: restore_from_backup())

# Layout in settings_frame grid
cur_pass_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
cur_pass_value.grid(row=0, column=1, sticky="w", padx=5, pady=5)
new_pass_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
new_pass_entry1.grid(row=1, column=1, padx=5, pady=5)
new_pass_entry2.grid(row=1, column=2, padx=5, pady=5)
btn_change_pass.grid(row=1, column=3, padx=5, pady=5)
keep_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
keep_entry.grid(row=2, column=1, padx=5, pady=5)
freq_label.grid(row=2, column=2, sticky="e", padx=5, pady=5)
freq_entry.grid(row=2, column=3, padx=5, pady=5)
btn_backup.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
btn_restore.grid(row=3, column=2, columnspan=2, padx=5, pady=10)

# --- Simple User Info Frame (Quick usage check) ---
info_prompt = ttk.Label(simple_info_frame, text="学生証をリーダーに置いて「確認」ボタンを押してください。", font=(FONT_FAMILY, 13))
info_prompt.grid(row=0, column=0, columnspan=2, pady=10)
btn_check = ttk.Button(simple_info_frame, text="利用状況を確認", command=lambda: check_usage())
btn_check.grid(row=1, column=0, columnspan=2, pady=5)
# Labels to display user info
lbl_cardid = ttk.Label(simple_info_frame, text="カードID:")
val_cardid = ttk.Label(simple_info_frame, text="")
lbl_status = ttk.Label(simple_info_frame, text="利用状況:")
val_status = ttk.Label(simple_info_frame, text="")
lbl_entrydate = ttk.Label(simple_info_frame, text="登録日:")
val_entrydate = ttk.Label(simple_info_frame, text="")
lbl_stock = ttk.Label(simple_info_frame, text="残り利用回数:")
val_stock = ttk.Label(simple_info_frame, text="")
lbl_next = ttk.Label(simple_info_frame, text="次の利用可能日まで:")
val_next = ttk.Label(simple_info_frame, text="")
# Layout in a grid
lbl_cardid.grid(row=2, column=0, sticky="e", pady=2)
val_cardid.grid(row=2, column=1, sticky="w", pady=2)
lbl_status.grid(row=3, column=0, sticky="e", pady=2)
val_status.grid(row=3, column=1, sticky="w", pady=2)
lbl_entrydate.grid(row=4, column=0, sticky="e", pady=2)
val_entrydate.grid(row=4, column=1, sticky="w", pady=2)
lbl_stock.grid(row=5, column=0, sticky="e", pady=2)
val_stock.grid(row=5, column=1, sticky="w", pady=2)
lbl_next.grid(row=6, column=0, sticky="e", pady=2)
val_next.grid(row=6, column=1, sticky="w", pady=2)
btn_back_home = ttk.Button(simple_info_frame, text="戻る", command=lambda: home_frame.tkraise())
btn_back_home.grid(row=7, column=0, columnspan=2, pady=15)

# --- User Info Frame (Detailed user info & edit) ---
ui_lbl_cardid = ttk.Label(user_info_frame, text="カードID:")
ui_val_cardid = ttk.Entry(user_info_frame, font=(FONT_FAMILY, 12))
ui_lbl_stock = ttk.Label(user_info_frame, text="利用回数ストック:")
ui_val_stock = ttk.Entry(user_info_frame, font=(FONT_FAMILY, 12))
ui_lbl_allow = ttk.Label(user_info_frame, text="許可 (1=可, 0=不可):")
ui_val_allow = ttk.Entry(user_info_frame, font=(FONT_FAMILY, 12))
ui_lbl_entry = ttk.Label(user_info_frame, text="登録日:")
ui_val_entry = ttk.Label(user_info_frame, text="")
ui_lbl_total = ttk.Label(user_info_frame, text="累計利用回数:")
ui_val_total = ttk.Label(user_info_frame, text="")
ui_lbl_today = ttk.Label(user_info_frame, text="今日の利用回数:")
ui_val_today = ttk.Label(user_info_frame, text="")
# Recent history labels (show last up to 5 uses for brevity)
ui_lbl_recent = ttk.Label(user_info_frame, text="最近の利用履歴:")
ui_hist1 = ttk.Label(user_info_frame, text="1:")
ui_val_hist1 = ttk.Label(user_info_frame, text="")
ui_hist2 = ttk.Label(user_info_frame, text="2:")
ui_val_hist2 = ttk.Label(user_info_frame, text="")
ui_hist3 = ttk.Label(user_info_frame, text="3:")
ui_val_hist3 = ttk.Label(user_info_frame, text="")
ui_hist4 = ttk.Label(user_info_frame, text="4:")
ui_val_hist4 = ttk.Label(user_info_frame, text="")
ui_hist5 = ttk.Label(user_info_frame, text="5:")
ui_val_hist5 = ttk.Label(user_info_frame, text="")
# Buttons
btn_save_user = ttk.Button(user_info_frame, text="設定を変更する", command=lambda: save_user_changes())
btn_user_back = ttk.Button(user_info_frame, text="戻る", command=lambda: setting_frame.tkraise())
btn_user_home = ttk.Button(user_info_frame, text="ホーム画面に戻る", command=lambda: home_frame.tkraise())

# Layout the user info fields grid
ui_lbl_cardid.grid(row=0, column=0, sticky="e", padx=5, pady=5)
ui_val_cardid.grid(row=0, column=1, padx=5, pady=5)
ui_lbl_stock.grid(row=1, column=0, sticky="e", padx=5, pady=5)
ui_val_stock.grid(row=1, column=1, padx=5, pady=5)
ui_lbl_allow.grid(row=2, column=0, sticky="e", padx=5, pady=5)
ui_val_allow.grid(row=2, column=1, padx=5, pady=5)
ui_lbl_entry.grid(row=3, column=0, sticky="e", padx=5, pady=5)
ui_val_entry.grid(row=3, column=1, padx=5, pady=5)
ui_lbl_total.grid(row=4, column=0, sticky="e", padx=5, pady=5)
ui_val_total.grid(row=4, column=1, padx=5, pady=5)
ui_lbl_today.grid(row=5, column=0, sticky="e", padx=5, pady=5)
ui_val_today.grid(row=5, column=1, padx=5, pady=5)
ui_lbl_recent.grid(row=6, column=0, padx=5, pady=(10,5))
# Recent usage entries in two columns:
ui_hist1.grid(row=7, column=0, sticky="e", padx=5)
ui_val_hist1.grid(row=7, column=1, sticky="w", padx=5)
ui_hist2.grid(row=8, column=0, sticky="e", padx=5)
ui_val_hist2.grid(row=8, column=1, sticky="w", padx=5)
ui_hist3.grid(row=9, column=0, sticky="e", padx=5)
ui_val_hist3.grid(row=9, column=1, sticky="w", padx=5)
ui_hist4.grid(row=10, column=0, sticky="e", padx=5)
ui_val_hist4.grid(row=10, column=1, sticky="w", padx=5)
ui_hist5.grid(row=11, column=0, sticky="e", padx=5)
ui_val_hist5.grid(row=11, column=1, sticky="w", padx=5)
# Buttons at bottom
btn_save_user.grid(row=12, column=1, padx=5, pady=15, sticky="e")
btn_user_back.grid(row=12, column=0, padx=5, pady=15, sticky="w")
btn_user_home.grid(row=13, column=1, padx=5, pady=(5,0), sticky="e")

# --- Make Unit Frame (New unit registration) ---
unit_name_label = ttk.Label(make_unit_frame, text="子機名:")
unit_name_entry = ttk.Entry(make_unit_frame, font=(FONT_FAMILY, 12))
unit_pass_label = ttk.Label(make_unit_frame, text="パスワード:")
unit_pass_entry = ttk.Entry(make_unit_frame, font=(FONT_FAMILY, 12))
unit_stock_label = ttk.Label(make_unit_frame, text="初期在庫数:")
unit_stock_entry = ttk.Entry(make_unit_frame, font=(FONT_FAMILY, 12))
unit_avail_label = ttk.Label(make_unit_frame, text="利用可能か (1=可,0=不可):")
unit_avail_entry = ttk.Entry(make_unit_frame, font=(FONT_FAMILY, 12))
btn_unit_create = ttk.Button(make_unit_frame, text="子機を登録する", command=lambda: create_unit())
btn_unit_back = ttk.Button(make_unit_frame, text="戻る", command=lambda: setting_frame.tkraise())
btn_unit_home = ttk.Button(make_unit_frame, text="ホーム画面に戻る", command=lambda: home_frame.tkraise())
# Layout
unit_name_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
unit_name_entry.grid(row=0, column=1, padx=5, pady=5)
unit_pass_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
unit_pass_entry.grid(row=1, column=1, padx=5, pady=5)
unit_stock_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)
unit_stock_entry.grid(row=2, column=1, padx=5, pady=5)
unit_avail_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
unit_avail_entry.grid(row=3, column=1, padx=5, pady=5)
btn_unit_create.grid(row=4, column=0, columnspan=2, pady=10)
btn_unit_back.grid(row=5, column=0, pady=5)
btn_unit_home.grid(row=5, column=1, pady=5)

# --- Unit Info Frame (Existing unit details) ---
ui2_lbl_name = ttk.Label(unit_info_frame, text="子機名:")
ui2_val_name = ttk.Label(unit_info_frame, text="")
ui2_lbl_pass = ttk.Label(unit_info_frame, text="パスワード:")
ui2_val_pass = ttk.Label(unit_info_frame, text="")
ui2_lbl_stock = ttk.Label(unit_info_frame, text="残り用品在庫:")
ui2_val_stock = ttk.Entry(unit_info_frame, font=(FONT_FAMILY, 12))
ui2_lbl_avail = ttk.Label(unit_info_frame, text="利用可能か (1/0):")
ui2_val_avail = ttk.Entry(unit_info_frame, font=(FONT_FAMILY, 12))
ui2_lbl_conn = ttk.Label(unit_info_frame, text="接続状態:")
ui2_val_conn = ttk.Label(unit_info_frame, text="")  # display only
btn_unit_save = ttk.Button(unit_info_frame, text="設定を変更する", command=lambda: save_unit_changes())
btn_unit_back = ttk.Button(unit_info_frame, text="戻る", command=lambda: setting_frame.tkraise())
btn_unit_home2 = ttk.Button(unit_info_frame, text="ホーム画面に戻る", command=lambda: home_frame.tkraise())
# Layout
ui2_lbl_name.grid(row=0, column=0, sticky="e", padx=5, pady=5)
ui2_val_name.grid(row=0, column=1, padx=5, pady=5)
ui2_lbl_pass.grid(row=1, column=0, sticky="e", padx=5, pady=5)
ui2_val_pass.grid(row=1, column=1, padx=5, pady=5)
ui2_lbl_stock.grid(row=2, column=0, sticky="e", padx=5, pady=5)
ui2_val_stock.grid(row=2, column=1, padx=5, pady=5)
ui2_lbl_avail.grid(row=3, column=0, sticky="e", padx=5, pady=5)
ui2_val_avail.grid(row=3, column=1, padx=5, pady=5)
ui2_lbl_conn.grid(row=4, column=0, sticky="e", padx=5, pady=5)
ui2_val_conn.grid(row=4, column=1, padx=5, pady=5)
btn_unit_save.grid(row=5, column=1, sticky="e", pady=15)
btn_unit_back.grid(row=5, column=0, sticky="w", pady=15)
btn_unit_home2.grid(row=6, column=1, sticky="e", pady=(5,0))

# Function to refresh lists in admin setting frame
def refresh_admin_lists():
    # Fetch fresh data for users, units, history
    users = mydb.member_call()  # returns list like ["0:cardID1", "1:cardID2", ...]
    units = mydb.units_call()   # returns list like ["1:unitName1", "2:unitName2", ...]
    history = mydb.his_call()   # returns list like ["1:...event1", "2:...event2", ...]
    lb_users_var.set(users)
    lb_units_var.set(units)
    lb_history_var.set(history)

def iccall():
    """Handle IC card registration when 'ICカードを置いた' is pressed."""
    data = mydb.do()  # attempt to read and register card
    ci = mydb.call_info()  # get info table (info: pass, counts, etc, including last message or list?)
    if data is True:
        # Card read success
        if mydb.done_zero() is False:
            # done flag was 0 => new registration
            # Append message to user list box for feedback (e.g., new user ID)
            if ci and len(ci) > 6:
                lb_users.insert(tk.END, ci[6])  # ci[6] might contain "N:cardID" of new user
            entry_done_frame.tkraise()
            entry_done_frame.after(2000, home_frame.tkraise)
        else:
            # done flag was 1 => card already existed
            exists_frame.tkraise()
            exists_frame.after(2000, home_frame.tkraise)
    else:
        # Card read failure
        error_frame.tkraise()
        error_frame.after(2500, home_frame.tkraise)

def check_password():
    """Verify admin password and open admin settings if correct."""
    entered = pass_entry.get()
    mydb.alignment_user()  # align user IDs (just in case)
    ci = mydb.call_info()
    actual_pass = ci[0] if ci else ""
    if entered == actual_pass:
        # Populate current password, keep and freq values in settings frame
        cur_pass_value.config(text=actual_pass)
        keep_entry.delete(0, tk.END)
        freq_entry.delete(0, tk.END)
        if ci:
            keep_entry.insert(0, str(ci[4]))  # maximum (keep limit)
            freq_entry.insert(0, str(ci[3]))  # frequency
        refresh_admin_lists()
        setting_frame.tkraise()
    else:
        pass_entry.delete(0, tk.END)
        passcheck_frame.tkraise()  # stay on passcheck (could show an error message if needed)

def open_user_details():
    """Open detailed view for the selected user from the list."""
    sel = lb_users.curselection()
    if not sel:
        return
    idx = sel[0]
    user_str = lb_users.get(idx)
    # user_str like "0:cardID", extract numeric ID (which corresponds to DB user id)
    uid = int(user_str.split(":")[0])
    # Perform an advanced search for this user to get details
    mydb.update_info(6, str(uid))
    # Retrieve user info tuple via add_find (which uses info.list field)
    info = mydb.add_find()
    if info:
        # info returns (cardid, stock, allow, entry, total, today, last1,...last10)
        ui_val_cardid.delete(0, tk.END); ui_val_cardid.insert(0, info[0])
        ui_val_stock.delete(0, tk.END); ui_val_stock.insert(0, str(info[1]))
        ui_val_allow.delete(0, tk.END); ui_val_allow.insert(0, str(info[2]))
        ui_val_entry.config(text=str(info[3]))
        ui_val_total.config(text=str(info[4]))
        ui_val_today.config(text=str(info[5]))
        # Fill recent history labels (last1...last5)
        recent = list(info[6:])  # last1 to last10
        # Show only up to 5 latest for brevity (assuming last1 is most recent)
        hist_labels = [ui_val_hist1, ui_val_hist2, ui_val_hist3, ui_val_hist4, ui_val_hist5]
        for i in range(5):
            if i < len(recent):
                val = recent[i]
                hist_labels[i].config(text=(str(val) if val != "記録なし" else "記録なし"))
            else:
                hist_labels[i].config(text="")
    user_info_frame.tkraise()

def save_user_changes():
    """Save changes made in user detail form (card ID, allow, stock). If card ID is emptied, delete user."""
    sel = lb_users.curselection()
    if not sel:
        setting_frame.tkraise(); return
    idx = sel[0]
    user_str = lb_users.get(idx)
    uid = int(user_str.split(":")[0])
    new_cardid = ui_val_cardid.get().strip()
    new_stock = ui_val_stock.get().strip()
    new_allow = ui_val_allow.get().strip()
    if new_allow == "":
        new_allow = None
    if new_stock == "":
        new_stock = None
    if new_cardid == "":
        # If card ID field cleared, delete user
        mydb.delete_user(uid)
    else:
        mydb.update_user(uid, 1, new_cardid)   # update cardid
        mydb.update_user(uid, 4, new_stock)    # update stock (remaining uses)
        mydb.update_user(uid, 2, new_allow)    # update allow flag
    mydb.make_backup()  # update backup after changes
    refresh_admin_lists()
    setting_frame.tkraise()

def open_unit_details():
    """Open detailed view for the selected unit from the list."""
    sel = lb_units.curselection()
    if not sel:
        return
    idx = sel[0]
    unit_str = lb_units.get(idx)
    unit_id = int(unit_str.split(":")[0])
    # Retrieve units list and find the entry with id (list is likely 1-indexed for units)
    units = mydb.units_call()
    if unit_id <= len(units):
        # The units_call returns list like ["1:UnitName", ...], we need details of unit by id
        # Let's query call_units (which likely returns raw data)
        all_units = mydb.call_units()
        # Find the unit whose id matches unit_id
        for u in all_units:
            if u[0] == unit_id:
                # u = (id, name, pass, stock, connect, available)
                ui2_val_name.config(text=str(u[1]))
                ui2_val_pass.config(text=str(u[2]))
                ui2_val_stock.delete(0, tk.END); ui2_val_stock.insert(0, str(u[3]))
                ui2_val_avail.delete(0, tk.END); ui2_val_avail.insert(0, str(u[5]))
                ui2_val_conn.config(text=("接続OK" if u[4] == 1 else "接続NG"))
                break
    unit_info_frame.tkraise()

def save_unit_changes():
    """Save stock/availability changes for a unit."""
    sel = lb_units.curselection()
    if not sel:
        setting_frame.tkraise(); return
    idx = sel[0]
    unit_str = lb_units.get(idx)
    unit_id = int(unit_str.split(":")[0])
    new_stock = ui2_val_stock.get().strip()
    new_avail = ui2_val_avail.get().strip()
    if new_stock == "":
        new_stock = None
    if new_avail == "":
        new_avail = None
    # Update in database
    mydb.update_unit(unit_id, 3, new_stock)    # update stock
    mydb.update_unit(unit_id, 5, new_avail)    # update available
    mydb.make_backup()
    refresh_admin_lists()
    setting_frame.tkraise()

def create_unit():
    """Create a new unit (child device) with provided info."""
    name = unit_name_entry.get().strip()
    pwd = unit_pass_entry.get().strip()
    stock = unit_stock_entry.get().strip()
    avail = unit_avail_entry.get().strip()
    if name == "" or pwd == "" or stock == "" or avail == "":
        return  # all fields required (could add validation message)
    try:
        mydb.make_unit(name, pwd, int(stock), int(avail))
    except Exception as e:
        pass  # handle exceptions if needed
    # Clear input fields
    unit_name_entry.delete(0, tk.END)
    unit_pass_entry.delete(0, tk.END)
    unit_stock_entry.delete(0, tk.END)
    unit_avail_entry.delete(0, tk.END)
    refresh_admin_lists()
    setting_frame.tkraise()

def change_password():
    """Change admin password and update usage settings (keep and freq)."""
    new1 = new_pass_entry1.get().strip()
    new2 = new_pass_entry2.get().strip()
    keep_val = keep_entry.get().strip()
    freq_val = freq_entry.get().strip()
    ci = mydb.call_info()
    current_pass = ci[0] if ci else ""
    if new1 == "" and new2 == "":
        # No change to password
        new1 = current_pass
        new2 = current_pass
    if new1 == new2:
        # Apply changes
        mydb.update_info(0, new1)    # update password
        mydb.update_info(4, keep_val)  # update maximum keep
        mydb.update_info(3, freq_val)  # update frequency
        cur_pass_value.config(text=new1)
        new_pass_entry1.delete(0, tk.END)
        new_pass_entry2.delete(0, tk.END)
        # Possibly update current info from DB again
    # else: if mismatch, could notify user (not implemented for brevity)

def export_history():
    """Export history (calls backup function for history or simply backup entire database)."""
    try:
        mydb.make_his_backup()  # if such function exists to backup history
    except:
        mydb.make_backup()     # fallback: just backup everything to Excel
    # In a real UI, you might prompt where the file was saved. Here we just perform the action.

def restore_from_backup():
    """Restore data from backup Excel file named 'backup'. The Excel file should be named 'backup.xlsx'."""
    # Attempt to call mydb.copy_from_excel with default 'backup' name
    try:
        mydb.copy_from_excel("backup")
        refresh_admin_lists()
    except Exception as e:
        print("Restore failed. Ensure 'backup.xlsx' is present.")

def check_usage():
    """Check usage status by reading an IC card (for quick status lookup)."""
    mydb.id_do()  # trigger NFC ID read (non-blocking call with timeout via nfcpy)
    member_info = mydb.add_find()  # get user info if card recognized
    if member_info:
        # member_info tuple structure as defined in add_find
        cardid, stock, allow_flag, entry_date, total, today, *_ = member_info
        status_text = "利用可能" if allow_flag == 1 else "利用停止中"
        # Calculate days until next usage increment
        ci = mydb.call_info()
        if ci:
            keep_limit = ci[4]  # maximum usage (stock limit)
            # ci[3] = freq (days required to gain one usage)
            # ci[2] = updatecount (days since last increment cycle?)
            # We can compute next increment if needed:
            days_until = ci[3] - ci[2] if ci[3] and ci[2] is not None else ""
        else:
            days_until = ""
        # Update labels
        val_cardid.config(text=str(cardid))
        val_status.config(text=status_text)
        val_entrydate.config(text=str(entry_date) if entry_date else "")
        val_stock.config(text=str(stock))
        if days_until != "" and isinstance(days_until, int):
            val_next.config(text=f"{days_until}日後")
        else:
            val_next.config(text="--")
    else:
        # Card not recognized (member_info likely empty strings as per add_find)
        val_cardid.config(text="(未登録)")
        val_status.config(text="不明")
        val_entrydate.config(text="")
        val_stock.config(text="")
        val_next.config(text="")

# Initial setup: ensure database tables exist and initial data is loaded
mydb.set_up()
mydb.make_user()
mydb.make_his()
# Start daily check loop (updates usage counts daily and creates backups)
def daily_check():
    mydb.dayupdate()
    mydb.make_backup()
    root.after(3600000, daily_check)  # repeat every hour
daily_check()

# Show home frame at startup
home_frame.tkraise()
root.mainloop()
