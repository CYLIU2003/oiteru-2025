from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import os
import io
import mydb2025 as mydb

app = Flask(__name__)
app.secret_key = "toshidai_tokyu_secret_key_2025"  # Secret key for session management

# Ensure database is set up on server start
mydb.set_up()
mydb.make_user()
mydb.make_his()

@app.route("/")
def index():
    """Home page - show options for card registration and usage check."""
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new student IC card."""
    if request.method == "POST":
        # When form is submitted to register, trigger card reading
        data = mydb.do()
        if data is True:
            # Card read successfully
            if mydb.done_zero() is False:
                # New card registered
                # Fetch newly added user info to show (e.g., card ID or message)
                ci = mydb.call_info()
                msg = "登録が完了しました。"
                # Optionally get last entry (ci[6]) to display the new card ID
                if ci and len(ci) > 6:
                    new_entry = ci[6]  # e.g., "N:cardID"
                    msg += f" (新規ID: {new_entry})"
                flash(msg, "success")
            else:
                # Card was already registered
                flash("この学生証はすでに登録済みです。", "warning")
        else:
            # Card read failure
            flash("ICカードが読み取れませんでした。再試行してください。", "error")
        return redirect(url_for("register"))
    # GET request: show the registration page with instructions
    return render_template("register.html")

@app.route("/usage", methods=["GET", "POST"])
def usage():
    """Check usage status of a student via IC card."""
    if request.method == "POST":
        mydb.id_do()  # attempt to read card ID
        info = mydb.add_find()
        if info and info[0] != "":
            # Card recognized; info tuple structure from add_find:
            cardid, stock, allow_flag, entry_date, total, today, *history = info
            allow_text = "利用可能" if allow_flag == 1 else "利用停止中"
            # Compute days until next usage increment
            ci = mydb.call_info()
            days_until = None
            if ci:
                # next increment after (freq - updatecount) days
                try:
                    freq = ci[3]
                    updatecount = ci[2]
                    if freq is not None and updatecount is not None:
                        days_until = freq - updatecount
                except:
                    days_until = None
            return render_template("usage_status.html",
                                   cardid=cardid, allow_text=allow_text,
                                   entry_date=entry_date, stock=stock,
                                   days_until=days_until)
        else:
            flash("未登録のICカードです。", "warning")
            return redirect(url_for("usage"))
    return render_template("usage.html")

@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    """Admin login (password check)."""
    if request.method == "POST":
        entered_pass = request.form.get("password", "")
        ci = mydb.call_info()
        actual_pass = ci[0] if ci else ""  # info.pass is stored at index 0
        if entered_pass == actual_pass:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("パスワードが違います。", "error")
            return redirect(url_for("admin_login"))
    # GET: render login form
    return render_template("admin_login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    """Admin dashboard showing summary and navigation links (if logged in)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    # We can display counts of users, units, etc.
    users = mydb.member_call()   # list of users like "0:cardid..."
    units = mydb.units_call()    # list of units like "1:unitName..."
    history = mydb.his_call()    # list of history entries
    return render_template("admin_dashboard.html", users=users, units=units, history=history)

@app.route("/admin/users")
def admin_users():
    """List all users (admin view)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    users = mydb.call_user()  # get raw user data (list of tuples)
    return render_template("admin_users.html", users=users)

@app.route("/admin/user/<int:uid>", methods=["GET", "POST"])
def admin_user_detail(uid):
    """View or edit details of a specific user (admin)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    # Align user IDs to current ordering (ensures uid is correct index)
    mydb.alignment_user()
    if request.method == "POST":
        # Update or delete user based on form input
        cardid = request.form.get("cardid", "").strip()
        stock = request.form.get("stock", "").strip()
        allow = request.form.get("allow", "").strip()
        if cardid == "":
            # Delete user if cardid is emptied
            mydb.delete_user(uid)
            flash("ユーザーを削除しました。", "info")
            return redirect(url_for("admin_users"))
        # Otherwise, update the user's info
        if allow == "":
            allow = None
        if stock == "":
            stock = None
        mydb.update_user(uid, 1, cardid)
        mydb.update_user(uid, 4, stock)
        mydb.update_user(uid, 2, allow)
        flash("ユーザー情報を更新しました。", "success")
        return redirect(url_for("admin_user_detail", uid=uid))
    # GET: retrieve user info to display
    users = mydb.call_user()
    user = None
    for u in users:
        if u[0] == uid:
            user = u
            break
    if user is None:
        # If user not found (perhaps was deleted), redirect to list
        return redirect(url_for("admin_users"))
    # user tuple: (id, cardid, allow, entry, stock, today, total, last1...last10)
    return render_template("admin_user_detail.html", user=user)

@app.route("/admin/units")
def admin_units():
    """List all child units (admin view)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    units = mydb.call_units()  # raw units data (list of tuples)
    return render_template("admin_units.html", units=units)

@app.route("/admin/unit/<int:uid>", methods=["GET", "POST"])
def admin_unit_detail(uid):
    """View or edit details of a specific unit (admin)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        # Update unit stock/availability
        stock = request.form.get("stock", "").strip()
        avail = request.form.get("available", "").strip()
        if stock == "":
            stock = None
        if avail == "":
            avail = None
        mydb.update_unit(uid, 3, stock)
        mydb.update_unit(uid, 5, avail)
        flash("子機情報を更新しました。", "success")
        return redirect(url_for("admin_unit_detail", uid=uid))
    units = mydb.call_units()
    unit = None
    for u in units:
        if u[0] == uid:
            unit = u
            break
    if unit is None:
        return redirect(url_for("admin_units"))
    # unit tuple: (id, name, pass, stock, connect, available)
    return render_template("admin_unit_detail.html", unit=unit)

@app.route("/admin/unit/new", methods=["GET", "POST"])
def admin_new_unit():
    """Add a new child unit (admin)."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        pwd = request.form.get("password", "").strip()
        stock = request.form.get("stock", "").strip()
        avail = request.form.get("available", "").strip()
        if name and pwd and stock and avail:
            try:
                mydb.make_unit(name, pwd, int(stock), int(avail))
                flash("新規子機を登録しました。", "success")
                return redirect(url_for("admin_units"))
            except Exception as e:
                flash("子機登録中にエラーが発生しました。", "error")
        else:
            flash("全ての項目を入力してください。", "warning")
    return render_template("admin_new_unit.html")

@app.route("/admin/history")
def admin_history():
    """View usage history entries."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    history = mydb.call_his()  # raw history data (list of tuples)
    return render_template("admin_history.html", history=history)

@app.route("/admin/backup")
def admin_backup_download():
    """Trigger a data backup and send the backup Excel file to the user."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    mydb.make_backup()  # create backup Excel (likely named 'backup.xlsx')
    # Send the backup file to the client for download
    backup_path = os.path.join(os.getcwd(), "backup.xlsx")
    if os.path.exists(backup_path):
        return send_file(backup_path, as_attachment=True, download_name="backup.xlsx")
    else:
        flash("バックアップファイルが見つかりませんでした。", "error")
        return redirect(url_for("admin_dashboard"))

@app.route("/admin/restore", methods=["GET", "POST"])
def admin_restore():
    """Restore data from an uploaded backup Excel file."""
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        file = request.files.get("backup_file")
        if file:
            # Save uploaded file as 'backup.xlsx'
            file.save("backup.xlsx")
            try:
                mydb.copy_from_excel("backup")  # expects file named backup.xlsx
                flash("バックアップからデータを復元しました。", "success")
            except Exception as e:
                flash("データ復元に失敗しました。ファイル形式を確認してください。", "error")
        return redirect(url_for("admin_dashboard"))
    # GET: show upload form
    return render_template("admin_restore.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
