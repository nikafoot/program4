import pandas as pd
import sys
import datetime

EXP_CSV_PATH ="./menu.csv"
RECEIPT_FOLDER = "./receipt"

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_master=item_master
        self.set_datetime()
    
    #日付の入力
    def set_datetime(self):
        self.datetime=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    #商品のコードから個数の確認
    def count_order(self, item_code):
        for s in self.item_master:
            if item_code == s.item_code:
                count = input("いくつほしいですか？")
                return s.item_name,s.price,int(count)
    
    #合計金額の計算、会計
    def calculate_price(self,order):
        sum = 0
        for sm in order:
            sum += sm[1]*sm[2]
        print(sum)
        self.write_receipt("合計金額:"+str(sum))
        while True:
            pay = input("支払う金額を記入してください：")
            change = int(pay) - sum
            self.write_receipt("おつり："+str(change))
            if change < 0:
                print("お金が足りません")
                continue
            else:
                print("お釣りは"+str(change)+"円です"+"\n"+"ご購入いただきありがとうございます")
                break

    # logフォルダの作成
    def write_receipt(self,text):
        print(text)
        with open(RECEIPT_FOLDER + "/" + self.receipt_name,mode="a",encoding="utf-8_sig") as f:
            f.write(text+"\n")
            f.close()
    
    #注文
    def enroll_order(self):
        print("いらっしゃいませ")
        m=[]
        while True:
            key = input("頼みたい商品のコードを教えて下さい：")
            k = self.count_order(key)
            m.append(k)
            key2 = input("他に注文したい商品はありますか？(Y or N):")
            if key2 == "Y":
                continue
            else:
                break
        self.receipt_name="receipt_{}.txt".format(self.datetime)
        self.write_receipt("-----------------------------------------------")
        self.write_receipt("オーダー登録された商品一覧\n")
        self.write_receipt(str(m))
        self.calculate_price(m)
        

#マスタ登録
def add_item_master_by_csv(csv_path):
    print("------- マスタ登録開始 ---------")
    item_master=[]
    count=0
    try:
        item_master_df=pd.read_csv(csv_path,dtype={"code":object}) # CSVでは先頭の0が削除されるためこれを保持するための設定
        for item_code,item_name,price in zip(list(item_master_df["code"]),list(item_master_df["name"]),list(item_master_df["price"])):
            item_master.append(Item(item_code,item_name,price))
            print("{}({}):{}円".format(item_name,item_code,price))
            count+=1
        print("{}品の登録を完了しました。".format(count))
        print("------- マスタ登録完了 ---------")
        return item_master
    except:
        print("マスタ登録が失敗しました")
        print("------- マスタ登録完了 ---------")
        sys.exit()

### メイン処理
def main():
    # マスタ登録
    item_master=add_item_master_by_csv(EXP_CSV_PATH)

    # オーダー登録,オーダー表示
    order=Order(item_master)

    #オーダー注文
    order.enroll_order()
    
if __name__ == "__main__":
    main()