import tkinter as tk  # Tkinterモジュールをインポート（GUI用）
import tkinter.ttk as ttk  # Tkinterのテーマ付きウィジェットをインポート
import openpyxl  # Excelファイルを操作するためのopenpyxlライブラリをインポート
import mydb2025 as mydb  # データベース操作を行うためのモジュールをインポート

# 毎日のチェックを行う関数
def daycheck():
    mydb.dayupdate()  # データベースの更新関数を呼び出す
    mydb.make_backup()  # バックアップを作成する関数を呼び出す
    #root.after(60000, daycheck)  # 1分後に再度重複処理を設定
    root.after(3600000, daycheck)  # 1時間後に再実行

# ユニットを作成する関数
def make_unit():
    unit_name = mu_unit_name.get()  # ユニット名を取得
    unit_pass = mu_unit_pass.get()  # ユニットのパスワードを取得
    unit_stock = mu_unit_stock.get()  # ユニットの在庫数を取得
    unit_available = mu_unit_available.get()  # ユニットの利用可能数を取得
    make = mydb.make_unit(unit_name, unit_pass, unit_stock, unit_available)  # ユニット作成をデータベースに依頼
    ci = mydb.call_info()  # 情報をデータベースから取得
    lb2.insert(tk.END, ci[6])  # Listboxにデータを追加
    change_st()  # 状態を変更する関数を呼び出す

# NFCが接続された時の呼び出し関数
def iccall():
    cu = mydb.call_user()  # ユーザーデータをデータベースから取得
    data = mydb.do()  # NFCの接続関数を呼び出す
    ci = mydb.call_info()  # 情報データを取得

    if data == True:  # NFC接続が成功した場合
        if mydb.done_zero() == False:  # 完了フラグのチェック
            lb.insert(tk.END, ci[6])  # Listboxにデータを追加
            entry_done.tkraise()  # 処理成功により、次の画面へ遷移
            entry_done.after(2000, change_main)  # 2秒後にメイン画面に戻る
        else:
            frame4.tkraise()  # 処理失敗により、指定した画面へ遷移
            frame4.after(2000, change_main)  # 2秒後にメイン画面に戻る
    else:
        frame3.tkraise()  # 処理失敗により、指定した画面へ遷移
        frame3.after(2500, change_main)  # 2.5秒後にメイン画面に戻る

# パスワードの確認関数
def pass_check():
    mydb.alignment_user()
    ci = mydb.call_info()  # 情報データを取得
    if ci[0] == txt.get():  # 入力パスワードとデータベース内のパスワードを比較
        new_pass1.delete(0, tk.END)  # 新しいパスワードフィールドをクリア
        new_pass2.delete(0, tk.END)  # 新しいパスワード確認フィールドをクリア
        keep.delete(0, tk.END)  # 保持数フィールドをクリア
        freq.delete(0, tk.END)  # 更新頻度フィールドをクリア
        setting_label4["text"] = text = ci[0]  # ラベルに現在のパスワードを表示
        keep.insert(0, ci[4])  # 保持数をフィールドに挿入
        freq.insert(0, ci[3])  # 更新頻度をフィールドに挿入
        new_pass1.insert(0, ci[0])  # 新しいパスワードフィールドに現在のパスワードを挿入
        new_pass2.insert(0, ci[0])  # 新しいパスワード確認フィールドに現在のパスワードを挿入
        '''
        global lbVar
        global lb
        global currencies
        currencies = mydb.member_call()  # メンバーのリストを取得
        print(currencies)
        lb.delete(0, tk.END)
        for item in currencies:
            lb.insert(tk.END, item)
        lbVar = tk.StringVar(value=currencies)  # Listbox用の制御変数を設定
        lb = tk.Listbox(setting_frame, listvariable=lbVar, selectmode=tk.SINGLE, activestyle=tk.NONE, width=20, height=15)  # Listboxを設定
        '''
        setting_frame.tkraise()  # 設定画面を表示

# メイン画面に変更する関数
def change_main():
    # メイン画面のラベルをクリア
    mydb.alignment_user()
    simple_user_info_label2["text"] = text = ''
    simple_user_info_label4["text"] = text = ''
    simple_user_info_label6["text"] = text = ''
    simple_user_info_label8["text"] = text = ''
    simple_user_info_label10["text"] = text = ''
    simple_user_info_label11["text"] = text = ''
    txt.delete(0, tk.END)  # テキストフィールドをクリア
    home_frame.tkraise()  # メイン画面を表示

# 各種画面に変更する関数
def change_entry_frame():
    mydb.alignment_user()
    entry_frame.tkraise()  # 入力画面を表示

def change_frame5():
    frame5.tkraise()  # フレーム5を表示

def change_simple_user_info_frame():
    simple_user_info_frame.tkraise()  # ユーザー情報フレームを表示

def change_mu():
    make_unit_frame.tkraise()  # ユニット作成フレームを表示

# 状態を変更する関数
def change_st():
    mydb.alignment_user()
    new_pass1.delete(0, tk.END)  # 新しいパスワードフィールドをクリア
    new_pass2.delete(0, tk.END)  # 新しいパスワード確認フィールドをクリア
    
    currencies = mydb.member_call()  # メンバーのリストを取得
    lbVar = tk.StringVar(value=currencies)  # Listbox用の制御変数を設定
    print(currencies)  # 取得したリストを表示
    lb = tk.Listbox(setting_frame, listvariable=lbVar, selectmode=tk.SINGLE, activestyle=tk.NONE, width=20, height=15)  # Listboxを設定
    setting_label4["text"] = text = mydb.call_info()[0]  # ラベルにデータを表示
    setting_frame.tkraise()  # 設定フレームを表示





# リストボックスの項目がダブルクリックされた時の処理
def lbfunc():
    add_member = lb.get(tk.ANCHOR)  # 選択されたアイテムを取得
    print('リストボックスで「{0}」が選択されました。'.format(add_member))  # 選択されたメンバーを表示
    target = ':'  # ターゲット文字列を指定
    idx = add_member.find(target)  # ターゲットのインデックスを取得
    r = add_member[:idx]  # IDを取得

    mydb.update_info(6, r)  # データベースを更新

    myid.delete(0, tk.END)  # IDフィールドをクリア
    mycount.delete(0, tk.END)  # カウントフィールドをクリア
    allow.delete(0, tk.END)  # 許可フィールドをクリア

    member_info = mydb.add_find()  # メンバーの情報を取得
    # 取得したメンバーの情報をフィールドに挿入
    myid.insert(0, member_info[0])  
    mycount.insert(0, member_info[1])  
    allow.insert(0, member_info[2])  
    user_info_label6["text"] = member_info[3]  
    user_info_label8["text"] = member_info[4]  
    user_info_label10["text"] = member_info[5]  
    user_info_label12["text"] = member_info[6]  
    user_info_label14["text"] = member_info[7]  
    user_info_label16["text"] = member_info[8]  
    user_info_label18["text"] = member_info[9]  
    user_info_label20["text"] = member_info[10]  
    user_info_label22["text"] = member_info[11]  
    user_info_label24["text"] = member_info[12]  
    user_info_label26["text"] = member_info[13]  
    user_info_label28["text"] = member_info[14]  
    user_info_label30["text"] = member_info[15]  
    user_info_frame.tkraise()  # ユーザー情報フレームに遷移

# リストボックスの項目がダブルクリックされた時の処理
def lbfunc2():
    add_member = lb2.get(tk.ANCHOR)  # 選択されたアイテムを取得
    print('リストボックスで「{0}」が選択されました。'.format(add_member))  # 選択されたユニットを表示
    target = ':'  # ターゲット文字列を指定
    idx = add_member.find(target)  # ターゲットのインデックスを取得
    r = add_member[:idx]  # IDを取得

    mydb.update_info(6, r)  # データベースを更新
    unit_stock.delete(0, tk.END)  # 在庫数フィールドをクリア
    unit_available.delete(0, tk.END)  # 利用可能数フィールドをクリア

    member_info = mydb.unit_find()  # ユニット情報を取得
    print(member_info)  # 取得した情報を表示
    # 取得したユニットの情報をフィールドに挿入
    unit_stock.insert(0, member_info[2])  
    unit_available.insert(0, member_info[4])  
    unit_name["text"] = member_info[0]  
    unit_pass["text"] = member_info[1]  
    unit_info_label17["text"] = member_info[3]  
    unit_info_frame.tkraise()  # ユニット情報フレームに遷移

# リストボックスの項目がダブルクリックされた時の処理
def lbfunc3():
    mydb.make_his_backup()  # ヒストリーのバックアップを作成
    pass  # 他の処理はなし

# メンバーを追加する関数
def add():
    mydb.alignment_user()
    add_member = lb.get(tk.ANCHOR)  # 選択されたアイテムを取得
    target = ':'  # ターゲット文字列を指定
    idx = add_member.find(target)  # ターゲットのインデックスを取得
    r = int(add_member[:idx])  # IDを取得
    get_myid = myid.get()  # IDフィールドの値を取得
    get_mycount = mycount.get()  # カウントフィールドの値を取得
    get_allow = allow.get()  # 許可フィールドの値を取得
   
    # 入力がNoneの場合はデフォルト値を設定
    if get_allow == None:
        get_allow = 1
    if get_mycount == None:
        get_mycount = 1

    if get_myid == "":  # IDが空の場合
        mydb.delete_user(r)  # ユーザーを削除
    else:
        mydb.update_user(r, 1, get_myid)  # ユーザーのIDを更新
        mydb.update_user(r, 4, get_mycount)  # ユーザーのカウントを更新
        mydb.update_user(r, 2, get_allow)  # ユーザーの許可状態を更新
        
    lb.delete(0,tk.END)  # Listboxから選択アイテムを削除
    cu =mydb.call_user()
    for i in range(len(cu)):
        lb.insert(r, f'{i}:{cu[i][1]}')  # Listboxに更新されたユーザーを追加
    '''
    lb.delete(r)  # Listboxから選択アイテムを削除
    mydb.alignment_user()
    if get_myid != "":  # IDが空でない場合
        lb.insert(r, f'{r}:{mydb.call_user()[r][1]}')  # Listboxに更新されたユーザーを追加
    '''
    mydb.make_backup()  # バックアップを作成

# ユニットを保存する関数
def unit_save():
    add_member = lb2.get(tk.ANCHOR)  # 選択されたアイテムを取得
    target = ':'  # ターゲット文字列を指定
    idx = add_member.find(target)  # ターゲットのインデックスを取得
    r = int(add_member[:idx])  # IDを取得

    # 在庫数フィールドを取得して更新
    get_unit_stock = unit_stock.get()
    get_unit_available = unit_available.get()
   
    if get_unit_stock == None:
        get_allow = 1
    if get_unit_available == None:
        get_mycount = 1

    mydb.update_unit(r, 3, get_unit_stock)  # ユニットの在庫数を更新
    mydb.update_unit(r, 5, get_unit_available)  # ユニットの利用可能数を更新
    
    lb2.delete(r - 1)  # Listboxからユニットを削除
    lb2.insert(r - 1, f'{r}:{mydb.call_units()[r - 1][1]}')  # 更新されたユニットをListboxに追加
    mydb.make_backup()  # バックアップを作成

# 新しいパスワードの処理
def new_pass():
    ci = mydb.call_info()[0]  # 現在のパスワードを取得
    pass1 = new_pass1.get()  # パスワードフィールドから入力値を取得
    pass2 = new_pass2.get()  # 確認パスワードフィールドから入力値を取得
    
    if (pass1 == '' and pass2 == ''):  # 両方のパスワードが空の場合
        pass1 = ci  # 現在のパスワードを使用
        pass2 = ci  # 確認パスワードも現在のパスワードを使用
        
    keepnum = keep.get()  # 保持数を取得
    freqnum = freq.get()  # 更新頻度を取得
    
    currencies = mydb.member_call()  # メンバーのリストを取得
    lbVar = tk.StringVar(value=currencies)  # Listbox用の制御変数を設定

    if pass1 == pass2:  # 新しいパスワードが一致する場合
        mydb.update_info(0, pass1)  # パスワードを更新
        mydb.update_info(4, keepnum)  # 保持数を更新
        mydb.update_info(3, freqnum)  # 更新頻度を更新

# ユーザーを検索する関数
def search_user():
    ci = mydb.call_info()  # 情報データを取得
    
    # 番号表示用ラベルをクリア
    simple_user_info_label2["text"] = text = ''
    simple_user_info_label4["text"] = text = ''
    simple_user_info_label6["text"] = text = ''
    simple_user_info_label8["text"] = text = ''
    simple_user_info_label10["text"] = text = ''
    simple_user_info_label11["text"] = text = ''

    mydb.id_do()  # NFC ID読み取り処理を実行
    member_info = mydb.add_find()  # メンバーの情報を取得
    keepnum = ci[4]  # 保持数を取得
    nextnum = ci[3] - ci[2]  # 次の利用可能日を計算
    
    if member_info[2] == 1:  # 許可されている場合
        allow = '利用可能'  # 状態を表示
    else:
        allow = '利用停止中'  # 停止中を表示
        
    # 情報を画面に表示
    simple_user_info_label2["text"] = text = member_info[0]  
    simple_user_info_label4["text"] = text = allow  
    simple_user_info_label6["text"] = text = member_info[3]  
    simple_user_info_label8["text"] = text = member_info[1]  
    simple_user_info_label10["text"] = text = (f'(最大保持数は{keepnum}):')  
    simple_user_info_label11["text"] = text = (f'{nextnum}日後')  # 次の利用日

# 上級検索を行う関数
def search_advanced():
    mydb.id_do()  # NFC ID読み取り処理を実行
    myid.delete(0, tk.END)  # IDフィールドをクリア
    mycount.delete(0, tk.END)  # 利用数フィールドをクリア
    allow.delete(0, tk.END)  # 許可フィールドをクリア
    member_info = mydb.add_find()  # メンバーの情報を取得
    print(member_info)  # メンバー情報を表示
    myid.insert(0, member_info[0])  # IDフィールドに値を挿入
    mycount.insert(0, member_info[1])  # 利用数フィールドに値を挿入
    allow.insert(0, member_info[2])  # 許可フィールドに値を挿入
    
    # 各種情報ラベルに情報を表示
    user_info_label6["text"] = member_info[3]
    user_info_label8["text"] = text = member_info[4]
    user_info_label10["text"] = text = member_info[5]
    user_info_label12["text"] = text = member_info[6]
    user_info_label14["text"] = text = member_info[7]
    user_info_label16["text"] = text = member_info[8]
    user_info_label18["text"] = text = member_info[9]
    user_info_label20["text"] = text = member_info[10]
    user_info_label22["text"] = text = member_info[11]
    user_info_label24["text"] = text = member_info[12]
    user_info_label26["text"] = text = member_info[13]
    user_info_label28["text"] = text = member_info[14]
    user_info_label30["text"] = text = member_info[15]
    
    user_info_frame.tkraise()  # ユーザー情報フレームに遷移

# バックアップからデータを復元する関数
def from_backup():
    txt = setting_label4.cget("text")  # ラベルからテキストを取得
    mydb.copy_from_excel(txt)  # Excelからデータを復元


mydb.set_up()  # データベースの初期設定を行う
root = tk.Tk()  # Tkinterのメインウィンドウを作成
root.title('ひらめきプロジェクト')  # ウィンドウのタイトルを設定
#root.geometry("1000x800")  # ウィンドウサイズを設定（コメントアウト中）



# フレーム0: カードリーダーの起動ボタン
home_frame = tk.Frame(root)  # ホーム画面のフレームを作成
home_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置
home_label0 = tk.Label(home_frame, text='オイテル登録マシン', font=("", 14))  # タイトルラベルを作成
home_label0.pack()  # ラベルをフレームに追加
home_button1 = tk.Button(home_frame, text='学生証を登録する', height=2, width=25, font=("", 14), command=change_entry_frame)  # 学生証登録ボタンを作成
home_button1.pack()  # ボタンをフレームに追加
home_button3 = tk.Button(home_frame, text='利用状況の確認', height=2, width=25, font=("", 14), command=change_simple_user_info_frame)  # 利用状況確認ボタンを作成
home_button3.pack()  # ボタンをフレームに追加
home_button2 = tk.Button(home_frame, text='詳細設定を開く', height=2, width=25, font=("", 14), command=change_frame5)  # 詳細設定ボタンを作成
home_button2.pack()  # ボタンをフレームに追加

# フレーム1: カードリーダーの起動ボタン
entry_frame = tk.Frame(root)  # エントリーフレームを作成
entry_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置
entry_label1 = tk.Label(entry_frame, text='ボタンを押した後学生証をタッチしてください', font=("", 14))  # 説明ラベルを作成
entry_label1.pack()  # ラベルをフレームに追加

entry_button1 = tk.Button(entry_frame, text='ICカードをおいた', font=("", 14), command=iccall)  # ICカードタッチボタンを作成
entry_button1.pack()  # ボタンをフレームに追加
entry_button2 = tk.Button(entry_frame, text='ホームに戻る', font=("", 14), command=change_main)  # ホームに戻るボタンを作成
entry_button2.pack()  # ボタンをフレームに追加

# フレーム2: 次の画面
entry_done = tk.Frame(root)  # 登録完了フレームを作成
entry_done.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置
entry_done_label1 = tk.Label(entry_done, text='登録が完了しました', font=("", 14))  # 完了メッセージラベルを作成
entry_done_label1.pack()  # ラベルをフレームに追加

# フレーム3: 失敗時の処理
frame3 = tk.Frame(root)  # 失敗フレームを作成
frame3.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置
lbl3 = tk.Label(frame3, text='ICカードが読み取れません！\nホーム画面に戻ります。', font=("", 14))  # 失敗メッセージを作成
lbl3.pack()  # ラベルをフレームに追加

# フレーム4: すでに登録済みの場合
frame4 = tk.Frame(root)  # 登録済みフレームを作成
frame4.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置
lbl4 = tk.Label(frame4, text='この学生証はもうすでに登録済みです！\nホーム画面に戻ります。', font=("", 14))  # 登録済みメッセージを作成
lbl4.pack()  # ラベルをフレームに追加

# フレーム5: 設定画面への移行確認
frame5 = tk.Frame(root)  # 設定確認画面を作成
frame5.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置
lbl5 = tk.Label(frame5, text='パスワードを入力してください', font=("", 14))  # パスワード入力要求ラベル
lbl5.grid(row=0, column=0)  # ラベルをフレームに配置
txt = tk.Entry(frame5, font=("", 14))  # パスワード入力フィールドを作成
txt.grid(row=1, column=0)  # 入力フィールドをフレームに配置
button5 = tk.Button(frame5, text='認証', command=pass_check, font=("", 14))  # 認証ボタンを作成
button5.grid(row=1, column=1)  # ボタンを配置
button5_2 = tk.Button(frame5, text="ホーム画面に戻る", font=("", 14), height=2, width=15, command=change_main)  # 戻るボタンを作成
button5_2.grid(row=2, column=0)  # ボタンを配置

# 設定画面
setting_frame = ttk.Frame(root)  # 設定画面を作成
setting_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置
setting_label1 = ttk.Label(setting_frame, text="メンバーリスト", font=("", 14))  # メンバーリストラベルを作成
setting_label1.grid(row=0, column=0)  # ラベルを配置
setting_button1 = tk.Button(setting_frame, text="選んだデータの確認 ", font=("", 14), height=2, width=15, command=lbfunc)  # 確認ボタンを作成
setting_button1.grid(row=8, column=0)  # ボタンを配置
setting_button2 = tk.Button(setting_frame, text="ホームに戻る", font=("", 14), height=2, width=15, command=change_main)  # ホームボタンを作成
setting_button2.grid(row=8, column=6)  # ボタンを配置

# 現在のパスワードラベルと設定
setting_label3 = ttk.Label(setting_frame, text="現在のパスワード:", font=("", 14))  # 現在のパスワードラベルを作成
setting_label3.grid(row=0, column=4)  # ラベルを配置
setting_label4 = ttk.Label(setting_frame, text='', font=("", 14))  # 現在のパスワード値を表示するラベルを作成
setting_label4.grid(row=0, column=6)  # ラベルを配置
setting_label5 = ttk.Label(setting_frame, text="パスワードを変更する", font=("", 14))  # パスワード変更ラベルを作成
setting_label5.grid(row=1, column=6)  # ラベルを配置
setting_label6 = ttk.Label(setting_frame, text="新しいパスワード:", font=("", 14))  # 新しいパスワードラベルを作成
setting_label6.grid(row=2, column=4)  # ラベルを配置
new_pass1 = tk.Entry(setting_frame, width=10, font=("", 14))  # 新しいパスワード入力フィールドを作成
new_pass1.grid(row=2, column=6)  # 入力フィールドを配置
setting_label6 = ttk.Label(setting_frame, text="　　　確認:", font=("", 14))  # 確認ラベルを作成
setting_label6.grid(row=3, column=4)  # ラベルを配置
new_pass2 = tk.Entry(setting_frame, width=10, font=("", 14))  # 確認用パスワード入力フィールドを作成
new_pass2.grid(row=3, column=6)  # 入力フィールドを配置
setting_button3 = tk.Button(setting_frame, text="設定を変更", font=("", 14), height=2, width=15, command=new_pass)  # 設定変更ボタンを作成
setting_button3.grid(row=4, column=6)  # ボタンを配置

# 操作ボタン
setting_button4 = tk.Button(setting_frame, text="カードをおいた", font=("", 14), height=2, width=15, command=search_advanced)  # カード押し込みボタンを作成
setting_button4.grid(row=9, column=0)  # ボタンを配置
setting_button5 = tk.Button(setting_frame, text="エクセルを作成", font=("", 14), height=2, width=15, command=mydb.make_backup)  # Excel作成ボタンを作成
setting_button5.grid(row=10, column=0)  # ボタンを配置
setting_button6 = tk.Button(setting_frame, text="エクセルから複製", font=("", 14), height=2, width=15, command=from_backup)  # Excel復元ボタンを作成
setting_button6.grid(row=11, column=0)  # ボタンを配置

# 利用回数保持の上限
setting_label8 = ttk.Label(setting_frame, text="　利用回数保持の上限:", font=("", 14))  # 上限ラベルを作成
setting_label8.grid(row=2, column=0)  # ラベルを配置
keep = tk.Entry(setting_frame, width=5, font=("", 14))  # 上限入力フィールドを作成
keep.grid(row=2, column=2)  # 入力フィールドを配置
setting_label9 = ttk.Label(setting_frame, text="１回増加にかかる日数:", font=("", 14))  # 増加日数ラベルを作成
setting_label9.grid(row=3, column=0)  # ラベルを配置
freq = tk.Entry(setting_frame, width=5, font=("", 14))  # 日数入力フィールドを作成
freq.grid(row=3, column=2)  # 入力フィールドを配置

# メンバーリスト
currencies = mydb.member_call()  # メンバーリストを取得
lbVar = tk.StringVar(value=currencies)  # Listbox用の制御変数を設定
lb = tk.Listbox(setting_frame, listvariable=lbVar, selectmode=tk.SINGLE, activestyle=tk.NONE, width=20, height=15, font=("", 14))  # メンバーリストのListboxを作成
lb.grid(row=7, column=0)  # Listboxを配置
setting_label10 = ttk.Label(setting_frame, text="利用者一覧", font=("", 14))  # 利用者一覧ラベルを作成
setting_label10.grid(row=6, column=0)  # ラベルを配置
scrollbar = ttk.Scrollbar(setting_frame, orient=tk.VERTICAL, command=lb.yview)  # Listbox用のスクロールバーを作成
lb['yscrollcommand'] = scrollbar.set  # Listboxとスクロールバーを連動
scrollbar.grid(row=7, column=1, stick="nsew")  # スクロールバーを配置
setting_button8=tk.Button(setting_frame,text="新規子機の登録 ",font=("",14),height = 2,width = 15,command = change_mu)
setting_button8.grid(row=9, column=2)

# ユニットリスト
currencies2 = mydb.units_call()  # ユニットリストを取得
lbVar2 = tk.StringVar(value=currencies2)  # Listbox用の制御変数を設定
lb2 = tk.Listbox(setting_frame, listvariable=lbVar2, selectmode=tk.SINGLE, activestyle=tk.NONE, width=20, height=15, font=("", 14))  # ユニットListboxを作成
lb2.grid(row=7, column=2)  # Listboxを配置
scrollbar2 = ttk.Scrollbar(setting_frame, orient=tk.VERTICAL, command=lb2.yview)  # ユニット用のスクロールバーを作成
lb2['yscrollcommand'] = scrollbar2.set  # Listboxとスクロールバーを連動
setting_label10 = ttk.Label(setting_frame, text="子機一覧", font=("", 14))  # 子機一覧ラベルを作成
setting_label10.grid(row=6, column=2)  # ラベルを配置
scrollbar2.grid(row=7, column=3, stick="nsew")  # スクロールバーを配置
setting_button7 = tk.Button(setting_frame, text="選んだデータの確認 ", font=("", 14), height=2, width=15, command=lbfunc2)  # 子機確認ボタンを作成
setting_button7.grid(row=8, column=2)  # ボタンを配置

# ヒストリーリスト
currencies3 = mydb.his_call()  # ヒストリーデータを取得
lbVar3 = tk.StringVar(value=currencies3)  # Listbox用の制御変数を設定
lb3 = tk.Listbox(setting_frame, listvariable=lbVar3, selectmode=tk.SINGLE, activestyle=tk.NONE, width=20, height=15, font=("", 14))  # ヒストリーListboxを作成
lb3.grid(row=7, column=4)  # Listboxを配置
setting_label10 = ttk.Label(setting_frame, text="利用履歴", font=("", 14))  # 利用履歴ラベルを作成
setting_label10.grid(row=6, column=4)  # ラベルを配置
scrollbar3 = ttk.Scrollbar(setting_frame, orient=tk.VERTICAL, command=lb3.yview)  # ヒストリー用のスクロールバーを作成
lb3['yscrollcommand'] = scrollbar3.set  # Listboxとスクロールバーを連動
scrollbar3.grid(row=7, column=5, stick="nsew")  # スクロールバーを配置
setting_button9 = tk.Button(setting_frame, text="履歴を出力 ", font=("", 14), height=2, width=15, command=lbfunc3)  # 履歴出力ボタンを作成
setting_button9.grid(row=8, column=4)  # ボタンを配置

# 簡易版利用状況確認画面
simple_user_info_frame = tk.Frame(root)  # 簡易版フレームを作成
simple_user_info_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置
simple_user_info_label0 = tk.Label(simple_user_info_frame, text='学生証をリーダーに置いてください', font=("", 14))  # メッセージラベルを作成
simple_user_info_label0.grid(row=0, column=0)  # ラベルを配置
simple_user_info_button = tk.Button(simple_user_info_frame, text='置いた', font=("", 14), command=search_user)  # リーダータッチボタンを作成
simple_user_info_button.grid(row=1, column=0)  # ボタンを配置

# ユーザー情報ラベルの作成
simple_user_info_label1 = ttk.Label(simple_user_info_frame, text="カードID:", font=("", 14))  # カードIDラベルを作成
simple_user_info_label1.grid(row=2, column=0)  # ラベルを配置
simple_user_info_label2 = ttk.Label(simple_user_info_frame, text="", font=("", 14))  # ID表示ラベルを作成
simple_user_info_label2.grid(row=2, column=1)  # ラベルを配置
simple_user_info_label3 = ttk.Label(simple_user_info_frame, text="利用状況:", font=("", 14))  # 利用状況ラベルを作成
simple_user_info_label3.grid(row=3, column=0)  # ラベルを配置
simple_user_info_label4 = ttk.Label(simple_user_info_frame, text="", font=("", 14))  # 状況表示ラベルを作成
simple_user_info_label4.grid(row=3, column=1)  # ラベルを配置
simple_user_info_label5 = ttk.Label(simple_user_info_frame, text="登録日:", font=("", 14))  # 登録日ラベルを作成
simple_user_info_label5.grid(row=4, column=0)  # ラベルを配置
simple_user_info_label6 = ttk.Label(simple_user_info_frame, text='', font=("", 14))  # 登録日表示ラベルを作成
simple_user_info_label6.grid(row=4, column=1)  # ラベルを配置

# 利用回数に関するラベルの作成
simple_user_info_label7 = ttk.Label(simple_user_info_frame, text="残りの利用回数:", font=("", 14))  # 利用回数ラベルを作成
simple_user_info_label7.grid(row=5, column=0)  # ラベルを配置
simple_user_info_label8 = ttk.Label(simple_user_info_frame, text="", font=("", 14))  # 残り回数表示ラベルを作成
simple_user_info_label8.grid(row=5, column=1)  # ラベルを配置
simple_user_info_label9 = ttk.Label(simple_user_info_frame, text="利用回数が１回分増えるまで", font=("", 14))  # 増加日数ラベル
simple_user_info_label9.grid(row=6, column=0)  # ラベルを配置
simple_user_info_label10 = ttk.Label(simple_user_info_frame, text="", font=("", 14))  # 増加日数表示ラベル
simple_user_info_label10.grid(row=6, column=1)  # ラベルを配置
simple_user_info_label11 = ttk.Label(simple_user_info_frame, text="", font=("", 14))  # その他の情報表示ラベル
simple_user_info_label11.grid(row=6, column=2)  # ラベルを配置
simple_user_info_button2 = tk.Button(simple_user_info_frame, text='戻る', font=("", 14), command=change_main)  # 戻るボタンを作成
simple_user_info_button2.grid(row=7, column=1)  # ボタンを配置

# メンバー追加フレーム
user_info_frame = ttk.Frame(root)  # メンバー追加フレームを作成
user_info_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置

# 各種ウィジェットの作成
user_info_label2 = ttk.Label(user_info_frame, text="カードID", font=("", 14))  # カードIDラベルを作成
user_info_label2.grid(row=1, column=1)  # ラベルを配置
user_info_label3 = ttk.Label(user_info_frame, text="利用回数ストック", font=("", 14))  # 使用回数ストックラベルを作成
user_info_label3.grid(row=2, column=1)  # ラベルを配置
user_info_label4 = ttk.Label(user_info_frame, text="1:許可0:不可", font=("", 14))  # 許可ラベルを作成
user_info_label4.grid(row=3, column=1)  # ラベルを配置
user_info_label5 = ttk.Label(user_info_frame, text="登録日", font=("", 14))  # 登録日ラベルを作成
user_info_label5.grid(row=4, column=1)  # ラベルを配置
user_info_label6 = ttk.Label(user_info_frame, text='', font=("", 14))  # 登録日表示ラベルを作成
user_info_label6.grid(row=4, column=2)  # ラベルを配置
user_info_label7 = ttk.Label(user_info_frame, text="累計利用回数", font=("", 14))  # 累計利用回数ラベルを作成
user_info_label7.grid(row=5, column=1)  # ラベルを配置
user_info_label8 = ttk.Label(user_info_frame, text='', font=("", 14))  # 累計回数表示ラベルを作成
user_info_label8.grid(row=5, column=2)  # ラベルを配置
user_info_label9 = ttk.Label(user_info_frame, text="今日の利用回数", font=("", 14))  # 今日の利用回数ラベルを作成
user_info_label9.grid(row=6, column=1)  # ラベルを配置
user_info_label10 = ttk.Label(user_info_frame, text='', font=("", 14))  # 今日の回数表示ラベルを作成
user_info_label10.grid(row=6, column=2)  # ラベルを配置

# 最近の利用履歴ラベルの作成
user_info_label111 = ttk.Label(user_info_frame, text="最近の利用履歴", font=("", 14))  # 履歴タイトルラベルを作成
user_info_label111.grid(row=7, column=1)  # ラベルを配置
user_info_label11 = ttk.Label(user_info_frame, text="1:", font=("", 14))  # 履歴1ラベルを作成
user_info_label11.grid(row=8, column=1)  # ラベルを配置
user_info_label12 = ttk.Label(user_info_frame, text='', font=("", 14))  # 履歴1表示ラベル
user_info_label12.grid(row=8, column=2)  # ラベルを配置

# 履歴ラベルの作成
user_info_label13 = ttk.Label(user_info_frame, text="2:", font=("", 14))  # 履歴2ラベルを作成
user_info_label13.grid(row=9, column=1)  # ラベルを配置
user_info_label14 = ttk.Label(user_info_frame, text='', font=("", 14))  # 履歴2表示ラベル
user_info_label14.grid(row=9, column=2)  # ラベルを配置
user_info_label15 = ttk.Label(user_info_frame, text="3:", font=("", 14))  # 履歴3ラベルを作成
user_info_label15.grid(row=10, column=1)  # ラベルを配置
user_info_label16 = ttk.Label(user_info_frame, text='', font=("", 14))  # 履歴3表示ラベル
user_info_label16.grid(row=10, column=2)  # ラベルを配置
user_info_label17 = ttk.Label(user_info_frame, text="4:", font=("", 14))  # 履歴4ラベルを作成
user_info_label17.grid(row=11, column=1)  # ラベルを配置
user_info_label18 = ttk.Label(user_info_frame, text='', font=("", 14))  # 履歴4表示ラベル
user_info_label18.grid(row=11, column=2)  # ラベルを配置
user_info_label19 = ttk.Label(user_info_frame, text="5:", font=("", 14))  # 履歴5ラベルを作成
user_info_label19.grid(row=12, column=1)  # ラベルを配置
user_info_label20 = ttk.Label(user_info_frame, text='', font=("", 14))  # 履歴5表示ラベル
user_info_label20.grid(row=12, column=2)  # ラベルを配置

# 利用回数に関するラベルの作成
user_info_label21 = ttk.Label(user_info_frame, text="6:", font=("", 14))  # 履歴6ラベルを作成
user_info_label21.grid(row=13, column=1)  # ラベルを配置
user_info_label22 = ttk.Label(user_info_frame, text='', font=("", 14))  # 履歴6表示ラベル
user_info_label22.grid(row=13, column=2)  # ラベルを配置
user_info_label23 = ttk.Label(user_info_frame, text="7:", font=("", 14))  # 履歴7ラベルを作成
user_info_label23.grid(row=14, column=1)  # ラベルを配置
user_info_label24 = ttk.Label(user_info_frame, text='', font=("", 14))  # 履歴7表示ラベル
user_info_label24.grid(row=14, column=2)  # ラベルを配置
user_info_label25 = ttk.Label(user_info_frame, text="8:", font=("", 14))  # 履歴8ラベルを作成
user_info_label25.grid(row=15, column=1)  # ラベルを配置
user_info_label26 = ttk.Label(user_info_frame, text='', font=("", 14))  # 履歴8表示ラベル
user_info_label26.grid(row=15, column=2)  # ラベルを配置
user_info_label27 = ttk.Label(user_info_frame, text="9:", font=("", 14))  # 履歴9ラベルを作成
user_info_label27.grid(row=16, column=1)  # ラベルを配置
user_info_label28 = ttk.Label(user_info_frame, text='', font=("", 14))  # 履歴9表示ラベル
user_info_label28.grid(row=16, column=2)  # ラベルを配置
user_info_label29 = ttk.Label(user_info_frame, text="10:", font=("", 14))  # 履歴10ラベルを作成
user_info_label29.grid(row=17, column=1)  # ラベルを配置
user_info_label30 = ttk.Label(user_info_frame, text='', font=("", 14))  # 履歴10表示ラベル
user_info_label30.grid(row=17, column=2)  # ラベルを配置

# ボタンの作成
user_info_button1 = tk.Button(user_info_frame, text="設定を変更する", font=("", 14), height=2, width=15, command=add)  # 設定変更ボタン
user_info_button1.grid(row=18, column=2)  # ボタンを配置
user_info_button3 = tk.Button(user_info_frame, text="戻る", font=("", 14), height=2, width=15, command=change_st)  # 戻るボタン
user_info_button3.grid(row=18, column=1)  # ボタンを配置
user_info_button2 = tk.Button(user_info_frame, text="ホーム画面に戻る", font=("", 14), height=2, width=15, command=change_main)  # ホームボタン
user_info_button2.grid(row=19, column=2)  # ボタンを配置

myid= tk.Entry(user_info_frame,font=("",14))
myid.grid(row=1, column=2)
mycount = tk.Entry(user_info_frame,font=("",14))
mycount.grid(row=2, column=2)
allow = tk.Entry(user_info_frame,font=("",14))
allow.grid(row=3, column=2)

# 新規子機の情報を設定する画面
make_unit_frame = ttk.Frame(root)  # 新規ユニット作成フレームを作成
make_unit_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置
make_unit_label2 = ttk.Label(make_unit_frame, text="子機の名前", font=("", 14))  # 子機名ラベルを作成
make_unit_label2.grid(row=1, column=1)  # ラベルを配置
make_unit_label3 = ttk.Label(make_unit_frame, text="パスワード", font=("", 14))  # パスワードラベルを作成
make_unit_label3.grid(row=2, column=1)  # ラベルを配置
make_unit_label4 = ttk.Label(make_unit_frame, text="残り用品枚数", font=("", 14))  # 在庫数ラベルを作成
make_unit_label4.grid(row=3, column=1)  # ラベルを配置
make_unit_label5 = ttk.Label(make_unit_frame, text="利用可能か（１：可０：不可）", font=("", 14))  # 利用可能性ラベルを作成
make_unit_label5.grid(row=4, column=1)  # ラベルを配置

make_unit_label16 = ttk.Label(make_unit_frame, text="接続（１：可０：不可）", font=("", 14))  # 接続可能性ラベルを作成
make_unit_label16.grid(row=5, column=1)  # ラベルを配置
make_unit_label17 = ttk.Label(make_unit_frame, text='', font=("", 14))  # 接続状態表示ラベルを作成
make_unit_label17.grid(row=5, column=2)  # ラベルを配置

# 子機の登録ボタンを作成
make_unit_button1 = tk.Button(make_unit_frame, text="子機を登録する", font=("", 14), height=2, width=15, command=make_unit)  # 子機登録ボタンを作成
make_unit_button1.grid(row=18, column=2)  # ボタンを配置
make_unit_button3 = tk.Button(make_unit_frame, text="戻る", font=("", 14), height=2, width=15, command=change_st)  # 戻るボタンを作成
make_unit_button3.grid(row=18, column=1)  # ボタンを配置
make_unit_button2 = tk.Button(make_unit_frame, text="ホーム画面に戻る", font=("", 14), height=2, width=15, command=change_main)  # ホームボタンを作成
make_unit_button2.grid(row=19, column=2)  # ボタンを配置

# 新規子機情報の入力フィールドを作成
mu_unit_name = tk.Entry(make_unit_frame, font=("", 14))  # 子機名入力フィールドを作成
mu_unit_name.grid(row=1, column=2)  # 入力フィールドを配置
mu_unit_pass = tk.Entry(make_unit_frame, font=("", 14))  # パスワード入力フィールドを作成
mu_unit_pass.grid(row=2, column=2)  # 入力フィールドを配置
mu_unit_stock = tk.Entry(make_unit_frame, font=("", 14))  # 在庫数入力フィールドを作成
mu_unit_stock.grid(row=3, column=2)  # 入力フィールドを配置
mu_unit_available = tk.Entry(make_unit_frame, font=("", 14))  # 利用可能数入力フィールドを作成
mu_unit_available.grid(row=4, column=2)  # 入力フィールドを配置

# 子機設定画面
unit_info_frame = ttk.Frame(root)  # 子機情報編集フレームを作成
unit_info_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)  # フレーム配置

# 各種ウィジェットの作成
unit_info_label2 = ttk.Label(unit_info_frame, text="子機の名前", font=("", 14))  # 子機名ラベルを作成
unit_info_label2.grid(row=1, column=1)  # ラベルを配置
unit_info_label3 = ttk.Label(unit_info_frame, text="パスワード", font=("", 14))  # パスワードラベルを作成
unit_info_label3.grid(row=2, column=1)  # ラベルを配置
unit_info_label4 = ttk.Label(unit_info_frame, text="残り用品枚数", font=("", 14))  # 在庫数ラベルを作成
unit_info_label4.grid(row=3, column=1)  # ラベルを配置
unit_info_label5 = ttk.Label(unit_info_frame, text="利用可能か（１：可０：不可）", font=("", 14))  # 利用可能性ラベルを作成
unit_info_label5.grid(row=4, column=1)  # ラベルを配置
unit_info_label16 = ttk.Label(unit_info_frame, text="接続（１：可０：不可）", font=("", 14))  # 接続可能性ラベルを作成
unit_info_label16.grid(row=5, column=1)  # ラベルを配置
unit_info_label17 = ttk.Label(unit_info_frame, text='', font=("", 14))  # 接続状態表示ラベルを作成
unit_info_label17.grid(row=5, column=2)  # ラベルを配置

# 子機情報を表示するラベルを作成
unit_name = ttk.Label(unit_info_frame, text='', font=("", 14))  # 子機名表示ラベルを作成
unit_name.grid(row=1, column=2)  # ラベルを配置
unit_pass = ttk.Label(unit_info_frame, text='', font=("", 14))  # パスワード表示ラベルを作成
unit_pass.grid(row=2, column=2)  # ラベルを配置

# 子機情報保存ボタンを作成
unit_info_button1 = tk.Button(unit_info_frame, text="設定を変更する", font=("", 14), height=2, width=15, command=unit_save)  # 設定変更ボタンを作成
unit_info_button1.grid(row=18, column=2)  # ボタンを配置
unit_info_button3 = tk.Button(unit_info_frame, text="戻る", font=("", 14), height=2, width=15, command=change_st)  # 戻るボタンを作成
unit_info_button3.grid(row=18, column=1)  # ボタンを配置
unit_info_button2 = tk.Button(unit_info_frame, text="ホーム画面に戻る", font=("", 14), height=2, width=15, command=change_main)  # ホームボタンを作成
unit_info_button2.grid(row=19, column=2)  # ボタンを配置

# 新規子機の在庫数と利用可能数フィールドを作成
unit_stock = tk.Entry(unit_info_frame, font=("", 14))  # 在庫数入力フィールドを作成
unit_stock.grid(row=3, column=2)  # 入力フィールドを配置
unit_available = tk.Entry(unit_info_frame, font=("", 14))  # 利用可能数入力フィールドを作成
unit_available.grid(row=4, column=2)  # 入力フィールドを配置

# 自分の情報を設定する画面
mydb.make_user()
mydb.make_his()  # ヒストリーデータを準備
daycheck()  # 日次チェックを開始
home_frame.tkraise()  # 最初に表示するフレームを設定
root.mainloop()  # Tkinterのメインループを開始
